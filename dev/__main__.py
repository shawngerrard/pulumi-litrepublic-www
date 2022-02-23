"""
Creating a Kubernetes Deployment for Lit Republic web services DEV environment
"""

# Import required Pulumi modules
import pulumi
import kubeconfig from "~/.kube/config"
import pulumi_random as random
from pulumi_kubernetes import Provider
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import ConfigMap, PersistentVolumeClaim, Secret, Service 
#from pulumi_kubernetes.helm.v3 import Chart, LocalChartOpts

# --
# Minikube does not implement services of type `LoadBalancer` and so requires the 
# user to specify if we're running on minikube, and if so, create a ClusterIP service
#--

# Get the Minikube user setting from the Pulumi configuration
# TO DO: Implement writing the isMinikube setting to the config file so that it can be centrally managed here.
config = pulumi.Config()
is_minikube = config.require_bool("isMinikube")

# Set the deployment name 
app_name = "nginx"
app_labels = { "app": app_name }

# Helm Deployment -- Not Active
# nginx_ingress = Chart(
#     "nginx-ingress",
#     LocalChartOpts(
#         path="/home/asterion/Documents/helm-charts/charts/nginx-ingress-controller",
#     ),
# )

# Define an Nginx deployment for ingress control
nginx_deployment = Deployment(
    app_name,
    spec={
        "selector": { "match_labels": app_labels },
        "replicas": 1,
        "template": {
            "metadata": { "labels": app_labels },
            "spec": { "containers": [{ "name": app_name, "image": app_name }] }
        }
    }
)

# Allocate an IP to the Nginx deployment
nginx_frontend = Service(
    app_name,
    metadata={
        "labels": nginx_deployment.spec["template"]["metadata"]["labels"],
    },
    spec={
        "type": "ClusterIP" if is_minikube else "LoadBalancer",
        "ports": [{ "port": 80, "target_port": 80, "protocol": "TCP" }],
        "selector": app_labels,
    }
)

# Define a Kubernetes provider
kubernetes_provider = Provider("kubernetes_provider", { "kubeconfig": kubeconfig.kubeconfig, "namespace": kubeconfig.appsNamespaceName })

# Create a database secret for MariaDB
mariadbSecret = Secret(
    "mariadb", {
        "stringData": {
            "mariadb-root-password": random.RandomPassword("mariadb-root-pw", {
                "length": 12}).result,
            "mariadb-password": random.RandomPassword("mariadb-pw", {
                "length": 12}).result
            }
        }, { 
        "provider": provider
    }
)

# Create a database secret for the Wordpress admin
wordpressSecret = Secret(
    "wordpress", {
        "stringData": {
            "wordpress-password": random.RandomPassword("wordpress-pw", {
                "length": 12}).result,
            }
        }, { 
        "provider": provider
    }
)

# Create a configmap for the mariadb settings
mariadbCM = ConfigMap("mariadb", {
    "data": {
        "my.cnf": `
[mysqld]
skip-name-resolve
explicit_defaults_for_timestamp
basedir=/opt/litrepublic/mariadb
port=3306
socket=/opt/litrepublic/mariadb/tmp/mysql.sock
tmpdir=/opt/litrepublic/mariadb/tmp
max_allowed_packet=16M
bind-address=0.0.0.0
pid-file=/opt/litrepublic/mariadb/tmp/mysqld.pid
log-error=/opt/litrepublic/mariadb/logs/mysqld.log
character-set-server=UTF8
collation-server=utf8_general_ci

[client]
port=3306
socket=/opt/litrepublic/mariadb/tmp/mysql.sock
default-character-set=UTF8

[manager]
port=3306
socket=/opt/litrepublic/mariadb/tmp/mysql.sock
pid-file=/opt/litrepublic/mariadb/tmp/mysqld.pid
`
    }
}, { "provider": provider })

# Create a persistent volume claim for wordpress on the mariadb volume
wordpressPVC = PersistentVolumeClaim("wordpress", {
    "spec": {
        "accessModes": ["ReadWriteOnce"],
        "resources": {
            "requests": {
                "storage": "10Gi"
            }
        }
    }
}, { "provider": provider })

# Create a service for mariadb
mariadbSvc = Service("mariadb", {
    "metadata": {
        "name": "mariadb",
    },
    "spec": {
        "type": "ClusterIP",
        "ports": [
            {
                "name": "mysql",
                "port": 3306,
                "targetPort": "mysql"
            }
        ],
        "selector": {
            "app": "mariadb",
            "component": "master",
            "release": "example"
        }
    }
}, { "provider": provider })

# Create a service for wordpress
wordpressSvc = Service("wordpress", {
    "spec": {
        "type": "LoadBalancer",
        "externalTrafficPolicy": "Cluster",
        "ports": [
            {
                "name": "http",
                "port": 80,
                "targetPort": "http"
            },
            {
                "name": "https",
                "port": 443,
                "targetPort": "https"
            }
        ],
        "selector": {
            "app": "wordpress"
        }
    }
}, { "provider": provider })

# Define a Wordpress deployment
wordpress_deployment = Deployment(
    "wordpress",
    spec={
        "selector": { "match_labels": { "app": "wordpress" }},
        "replicas": 1,
        "template": {
            "metadata": {
                "labels": "wordpress"
            },
            "spec": {
                "hostAliases": [{ "ip": "127.0.0.1", "hostnames": [ "status.localhost" ]}],
                "containers": [
                    { 
                        "name": "wordpress",
                        "image": "wordpress:5.9.0-php8.1-fpm-alpine",
                        "imagePullPolicy": "IfNotPresent",
                        "env": [
                            { "name": "MARIADB_HOST", "value": "mariadb" },
                            { "name": "WORDPRESS_DATABASE_NAME", "value": "litrepublic-dev-wordpress" },
                            { "name": "WORDPRESS_DATABASE_USER", "value": "wordpress-db-admin" },
                            { "name": "WORDPRESS_DATABASE_PASSWORD", "value": "!@#test123" }
                            # "valueFrom": 
                            #     {
                            #         "secretKeyRef": {
                            #             "name": mariadbSecret.metadata.name,
                            #             "key": "mariadb-password"
                            #         }
                            #     }
                            # }
                        ],
                        "ports": [
                            { "name": "http", "containerPort": 80 },
                            { "name": "https", "containerPort": 443 }
                        ],
                        "volumeMounts": [
                            {
                                "mountPath": "/litrepublic/wordpress",
                                "name": "lirepublic-wordpress-data",
                                "subPath": "wordpress"
                            }
                        ],
                        "resources": { 
                            "requests": { 
                                "cpu": "300m", 
                                "memory": "512Mi" 
                            }
                        }
                    }
                ]
            }
        }
    }
)

# Get the public IP of the deployment
result = None
if is_minikube:
    result = nginx_frontend.spec.apply(lambda v: v["cluster_ip"] if "cluster_ip" in v else None)
else:
    ingress = nginx_frontend.status.apply(lambda v: v["load_balancer"]["ingress"][0] if "load_balancer" in v else None)
    if ingress is not None:
        result = ingress.apply(lambda v: v["ip"] if "ip" in v else v["hostname"])

# Output public IP and deployment name
pulumi.export("name", nginx_deployment.metadata["name"])
pulumi.export("ip", result)