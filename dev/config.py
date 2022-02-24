# Obtain Pulumi config
import pulumi as pulumi
config = pulumi.Config()

# Existing Pulumi stack reference in the format:
# <organization>/<project>/<stack> e.g. "myUser/myProject/dev"
infraStackRef = pulumi.StackReference(config.require("infraStackRef"))
#clusterStackRef = pulumi.StackReference(config.require("clusterStackRef"))

config = {
    # Obtain Pulumi infra attributes
    "privateSubnetIds": infraStackRef.get_output("privateSubnetIds"),
    "publicSubnetIds": infraStackRef.get_output("publicSubnetIds"),

    # Obtain Kubernetes cluster attributes
    "kubeconfig": infraStackRef.get_output("kubeConfig"),
    "clusterName": infraStackRef.get_output("clusterName"),
    "securityGroupIds": infraStackRef.get_output("securityGroupIds"),
    "clusterSvcsNamespaceName": infraStackRef.get_output("clusterSvcsNamespaceName"),
    "appSvcsNamespaceName": infraStackRef.get_output("appSvcsNamespaceName"),
    "appsNamespaceName": infraStackRef.get_output("appsNamespaceName"),
}