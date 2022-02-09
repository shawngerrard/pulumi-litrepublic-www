# pulumi-litrepublic-www
This project is intended as a guide to setting up and deploying web stacks through Pulumi using Kubernetes and locally provisioned resources.


## Preparing the Raspberry Pi
Our primary node/computer for our project will be a Raspberry Pi 4b, and we'll install a USB-bootable ARM64 Linux Operating System into it.

### Pre-requisites
Aside from physical hardware, you'll need to prepare the following:
1. Download and install the official [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
2. Write an Operating System image to both an SD card and a USB flash drive.
    > **Note:** For RPI 4B models older purchased during or after 2021, you should only need to write the image to a USB drive as USB boot is enabled in the RPI 4b EEPROM boot order by default.
    - The Raspberry Pi OS is the recommended general purpose OS built specifically for use with Raspberry Pi hardware specifications. However, we will use the *"Other general-purpose OS"* option to select a 64-bit Ubuntu Desktop (currently 21.10).
    > **Note:** I recommend [downloading the image](https://ubuntu.com/download/raspberry-pi) first and using the *"Use custom"* option in the RPI Imager to select the downloaded image. This will significantly increase performance during image writing.
3. When the image has been written to the SD card, put it into the SD reader on the RPI and power it up!

<hr />

### Ubuntu Desktop Installation and Configuration
1. The Ubuntu bootstrapper will take you through the normal installation options and steps - be sure to make note of the username and password you've set! The installation will take several minutes to complete. 
2. Once installed, log in and open your applications. Make sure to mark the *Terminal* application as a favourite, which will add it to your quick-access toolbar.
3. Open up *Terminal* and use the following commands to configure your OS environment:
    - Install net tools to obtain and/or verify network interface configurations:
    ```sudo apt install net-tools```
    - Hi
    ```Hi```

<hr />

## Remote access
We'll need to enable remote SSH access to provide 

### Enable SSH authentication 
1. Create SSH key
    ```ssh-keygen -t rsa -b 4096 -C "<username>@hostname" -f ~/.ssh/<keyname>```
2. Copy SSH public key to server and install into authorized_keys.
    ```ssh-copy-id -i ~/.ssh/<key/filename>.pub <server username>@<server hostname/ext. ip> -p <external port number>```
> **Note:** Log into the host and use the following code to remove **a single** public key from the host that may have erroneously been added:
    ```sed -i.bak '/REGEX_MATCHING_KEY/d' ~/.ssh/authorized_keys```

> **Note:** Log into the host and use the following code to remove **multiple** public keys from the host that may have erroneously been added:
    ```sed -i.bak '/REGEX1/d; /REGEX2/d' ~/.ssh/authorized_keys```

<hr />

### Secure SSH config in RPI
> **Reference:** [https://webdock.io/en/docs/how-guides/security-guides/ssh-security-configuration-settings](https://webdock.io/en/docs/how-guides/security-guides/ssh-security-configuration-settings) and access the file using the snippet below.
```sudo nano /etc/ssh/sshd_config```

1. Open SSH config and follow the referenced link above to tweak settings.

<hr />

### Enable SSH remote access on a specific port at the internet gateway.
1. Log in to router.
2. Open an external port <PORT NUMBER> on RPI external IP 124.248.134.230.
3. Forward to internal port 22.
4. Apply changes.

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
