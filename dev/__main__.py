"""
Creating a Kubernetes Deployment for Lit Republic web services DEV environment
"""

# Import required Pulumi modules
import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service

# Minikube does not implement services of type `LoadBalancer`; require the user to specify if we're
# running on minikube, and if so, create only services of type ClusterIP.
config = pulumi.Config()
is_minikube = config.require_bool("isMinikube")

app_name = "nginx"
app_labels = { "app": "nginx" }

# Define an Nginx deployment for ingress control
deployment = Deployment(
    "nginx",
    spec={
        "selector": { "match_labels": app_labels },
        "replicas": 1,
        "template": {
            "metadata": { "labels": app_labels },
            "spec": { "containers": [{ "name": "nginx", "image": "nginx" }] }
        }
    })

# Allocate an IP to the Deployment.
frontend = Service(
    app_name,
    metadata={
        "labels": deployment.spec["template"]["metadata"]["labels"],
    },
    spec={
        "type": "ClusterIP" if is_minikube else "LoadBalancer",
        "ports": [{ "port": 80, "target_port": 80, "protocol": "TCP" }],
        "selector": app_labels,
    })

# When "done", this will print the public IP.
result = None
if is_minikube:
    result = frontend.spec.apply(lambda v: v["cluster_ip"] if "cluster_ip" in v else None)
else:
    ingress = frontend.status.apply(lambda v: v["load_balancer"]["ingress"][0] if "load_balancer" in v else None)
    if ingress is not None:
        result = ingress.apply(lambda v: v["ip"] if "ip" in v else v["hostname"])

# Output public IP and deployment name
pulumi.export("name", deployment.metadata["name"])
pulumi.export("ip", result)