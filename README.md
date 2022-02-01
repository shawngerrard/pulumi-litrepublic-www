# pulumi-litrepublic-www
This project is intended as a guide to setting up and deploying web stacks through Pulumi using Kubernetes and locally provisioned resources.


## Remote access
We'll need to enable remote SSH access to provide 

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

### Enable SSH remote Git access from server

1. Create an SSH key on the server (see above example).
2. Copy the public key contents, log in to your Github account, and enter the key data into a new PGP key entry under your Github account in _Settings/Encryption Keys/Add New Key_
```cat ~/.ssh/<public keyname>.pub | xclip```
3. Ensure the SSH-Agent has started and the key has been added to your agent.
```eval `ssh-agent` && ssh-add ~/.ssh/<key/filename>```
3. Test the connection.
```ssh -T git@github.com```
4. Update git config with identity values.
```git config --global user.email "<email address>" && git config --global user.name "<user>@<hostname>"```
5. Clone this repository.
```git clone git@github.com:shawngerrard/pulumi-litrepublic-www-dev.git```

<hr />


## Install Kubectl on Server


### Instructions for installing Kubectl

<hr />


## Install Helm on Server


### Instructions for installing Helm

<hr />


## Install and Configure Pulumi CLI on Server


### Download and install Pulumi CLI
1. Run the following command on the server to install Pulumi CLI.
```curl -fsSL https://get.pulumi.com | sh```

### Create a Pulumi Kubernetes provider project environment

> **Note:** If you've just cloned a Pulumi project, or wish to switch between stacks, use the following command to initialize the Pulumi stack you want. You'll then be asked for the fully-qualified name of the stack.
```pulumi stack init```

> **Note:** You can avoid prompts to indicate which stack you want to work on my setting the workspace to the stack
```pulumi stack select <stack name>```

1. Create a new Pulumi project and scaffold in the Kubernetes provider modules.
```mkdir dev && cd dev```
```pulumi new kubernetes-python```

2. Initialize a Python virtual environment to isolate project resources.
```python3 -m venv venv```

3. Install and update wheel so that we can install dependent Pulumi modules into our virtual environments.
```pip3 install wheel --upgrade```

4. Activate the virtual environment.
```source venv/bin/activate```

5. Install project dependencies into the virtual environment.
```pip install -r requirements.txt```

<hr />



### Instructions for uninstalling Pulumi
From the official [Pulumi documentation](https://www.pulumi.com/docs/get-started/install/):

> To uninstall Pulumi, remove the .pulumi folder from your home directory. If you installed Pulumi manually, you should also remove the pulumi folder that was created.

<hr />
