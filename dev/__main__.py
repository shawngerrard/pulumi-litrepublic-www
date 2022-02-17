"""
Creating a Kubernetes Deployment for Lit Republic web services DEV environment
"""

# Import required Pulumi modules
import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service
from pulumi_kubernetes.helm.v3 import Chart, LocalChartOpts

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

nginx_ingress = Chart(
    "nginx-ingress",
    LocalChartOpts(
        path="~/Documents/helm-charts/charts/nginx-ingress-controller",
    ),
)


# # Define an Nginx deployment for ingress control
# deployment = Deployment(
#     app_name,
#     spec={
#         "selector": { "match_labels": app_labels },
#         "replicas": 1,
#         "template": {
#             "metadata": { "labels": app_labels },
#             "spec": { "containers": [{ "name": app_name, "image": app_name }] }
#         }
#     })

# # Allocate an IP to the Deployment
# frontend = Service(
#     app_name,
#     metadata={
#         "labels": deployment.spec["template"]["metadata"]["labels"],
#     },
#     spec={
#         "type": "ClusterIP" if is_minikube else "LoadBalancer",
#         "ports": [{ "port": 80, "target_port": 80, "protocol": "TCP" }],
#         "selector": app_labels,
#     }
# )

# Get the public IP of the deployment
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