# pulumi-litrepublic-www-dev
This project is intended as a guide to setting up and deploying web stacks through Pulumi using Kubernetes and locally provisioned resources.


- Remote access
    - Enable SSH authentication 
        - Create SSH key
            ```ssh-keygen -t rsa -b 4096 -C "<username>@hostname" -f ~/.ssh/<keyname>```
        - Copy SSH public key to server and install into authorized_keys
            ```ssh-copy-id -i ~/.ssh/<key/filename> <server username>@<server hostname/ext. ip>```
    - Secure SSH config in RPI
        > **Reference:** https://webdock.io/en/docs/how-guides/security-guides/ssh-security-configuration-settings and access the file using the snippet below.
        ```sudo nano /etc/ssh/sshd_config```
        1. open SSH config and follow the guide to tweak settings as above
    - Enable SSH remote access on a specific port at the internet gateway.
        1. log in to router
        2. open external port <PORT NUMBER> on RPI external IP 124.248.134.230.
        3. forward to internal port 22.
        4. 
    - Test connection
        - Connect to the host by specifying the port at which the host accepts SSH traffic.
            ```ssh -p <external port number> <server username>@<server hostname/ext. ip>```
    - Monitor logs on the server for any dodgy port knocks
        ```sudo cat /var/log/auth.log```
    