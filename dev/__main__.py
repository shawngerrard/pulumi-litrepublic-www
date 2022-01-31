"""
Creating a Kubernetes Deployment for Lit Republic web services DEV environment
"""

# Import required Pulumi modules
import pulumi
from pulumi_kubernetes.apps.v1 import Deployment

app_labels = { "app": "nginx" }

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

pulumi.export("name", deployment.metadata["name"])