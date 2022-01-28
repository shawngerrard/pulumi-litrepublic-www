# pulumi-litrepublic-www-dev
This project is intended as a guide to setting up and deploying web stacks through Pulumi using Kubernetes and locally provisioned resources.


## Remote access


### Enable SSH authentication 
1. Create SSH key
    ```ssh-keygen -t rsa -b 4096 -C "<username>@hostname" -f ~/.ssh/<keyname>```
2. Copy SSH public key to server and install into authorized_keys.
    ```ssh-copy-id -i ~/.ssh/<key/filename>.pub <server username>@<server hostname/ext. ip> -p <external port number>```
> Log into the host and use the following code to remove **a single** public key from the host that may have erroneously been added:
    ```sed -i.bak '/REGEX_MATCHING_KEY/d' ~/.ssh/authorized_keys```

> Log into the host and use the following code to remove **multiple** public keys from the host that may have erroneously been added:
    ```sed -i.bak '/REGEX1/d; /REGEX2/d' ~/.ssh/authorized_keys```

<hr />

### Secure SSH config in RPI
> **Reference:** https://webdock.io/en/docs/how-guides/security-guides/ssh-security-configuration-settings and access the file using the snippet below.
```sudo nano /etc/ssh/sshd_config```

1. Open SSH config and follow the referenced link above to tweak settings.

<hr />

### Enable SSH remote access on a specific port at the internet gateway.
1. Log in to router
2. Open external port <PORT NUMBER> on RPI external IP 124.248.134.230.
3. Forward to internal port 22.
4. 

<hr />

### Test connection
1. Connect to the host by specifying the port at which the host accepts SSH traffic.
```ssh -p <external port number> <server username>@<server hostname/ext. ip>```

<hr />

### Monitor logs on the server for any dodgy port knocks
```sudo cat /var/log/auth.log```

<hr />