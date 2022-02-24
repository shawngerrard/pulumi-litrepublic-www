# Obtain Pulumi config
import pulumi as pulumi
config = pulumi.Config()

# Existing Pulumi stack reference in the format:
# <organization>/<project>/<stack> e.g. "myUser/myProject/dev"
infraStackRef = pulumi.StackReference(config.require("infraStackRef"));
clusterStackRef = pulumi.StackReference(config.require("clusterStackRef"));

export config = {
    # Infra
    "privateSubnetIds": infraStackRef.getOutput("privateSubnetIds"),
    "publicSubnetIds": infraStackRef.getOutput("publicSubnetIds"),

    # Cluster
    "kubeconfig": clusterStackRef.getOutput("kubeconfig"),
    "clusterName": clusterStackRef.getOutput("clusterName"),
    "securityGroupIds": clusterStackRef.getOutput("securityGroupIds"),
    "clusterSvcsNamespaceName": clusterStackRef.getOutput("clusterSvcsNamespaceName"),
    "appSvcsNamespaceName": clusterStackRef.getOutput("appSvcsNamespaceName"),
    "appsNamespaceName": clusterStackRef.getOutput("appsNamespaceName"),
}