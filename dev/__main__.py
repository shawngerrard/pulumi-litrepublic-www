"""
Creating a Kubernetes Deployment for Lit Republic web services DEV environment
"""

# Import required Pulumi modules
import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service
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

# Define a Wordpress deployment
wordpress_deployment = Deployment(
    "wordpress",
    spec={
        "selector": { "match_labels": { "app": "wordpress", "release":"www-dev-arm64"} },
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
                            { "name": "WORDPRESS_DATABASE_PASSWORD", "value": "!@#test123"
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