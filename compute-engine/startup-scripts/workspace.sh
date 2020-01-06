#!/bin/sh

# Add node repo
#sudo su $LDAP 
curl -sL https://deb.nodesource.com/setup_11.x | sudo bash -
# Add docker repo
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# Add GCP repo
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update -q

# Install base dependencies
sudo apt-get install -y -q      curl \
                        gcc \
                        python-dev \
                        python-setuptools \
                        apt-transport-https \
                        lsb-release \
                        openssh-client \
                        git \
                        gnupg \
                        tmux \
                        vim \
                        python-virtualenv \
                        nginx \
                        cron

sudo easy_install -U pip && pip install -U crcmod

# Install node.js
sudo apt-get install -y software-properties-common nodejs

# install Docker dependencies and Docker afterwards
sudo apt-get install -y         ca-certificates \
                        curl \
                        gnupg2

sudo sudo apt-get install -y docker-ce \
                        docker-ce-cli \
                        containerd.io

# Install Cloud SDK via apt-get
sudo apt-get install -y google-cloud-sdk \
                        google-cloud-sdk-app-engine-python \
                        google-cloud-sdk-app-engine-python-extras \
                        google-cloud-sdk-app-engine-java \
                        google-cloud-sdk-app-engine-go \
                        google-cloud-sdk-datalab \
                        google-cloud-sdk-datastore-emulator \
                        google-cloud-sdk-pubsub-emulator \
                        google-cloud-sdk-cbt \
                        google-cloud-sdk-cloud-build-local \
                        google-cloud-sdk-bigtable-emulator \
                        kubectl

export LDAP=$(gcloud compute instances describe workspace --flatten="metadata[LDAP]" --zone europe-west2-a | sed -n 2p | tr -d ' ')
echo $LDAP > /home/$LDAP/log

# Install golang
sudo apt-get install -y golang-go
export GOROOT=/usr/bin/go 
mkdir /home/$LDAP/go /home/$LDAP/go/src /home/$LDAP/go/bin
export GOPATH=/home/$LDAP/go

# Set up some aliases and bash profiles
sudo cat <<EOF >> /etc/profile
alias ll='ls -lFa'
EOF

sudo cat <<EOF > /etc/profile/.bashrc
export PATH=$PATH:$GOROOT/bin
if [ -f .bash_aliases ];then
        . ~/.bash_aliases
else
        touch /etc/bash_aliases
fi

if [ -x /usr/bin/dircolors ]; then
        test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
        alias ls='ls --color=auto'
fi
docker-credential-gcr configure-docker
EOF

sudo cat <<EOF >> /home/$LDAP/.bashrc
# Create firewall rule each time the instance is accessed
echo "Creating firewall rule in the background: Allowing HTTP traffic in port 80"
echo "Note: This process is executed each 10 minutes, due to the Firewall policies in Google projects"
echo -e "\n" | gcloud compute firewall-rules create p80 --allow tcp:80 2>/dev/null &
EOF
 
sudo mkdir /home/$LDAP/.bashusr
sudo cat <<EOF > /home/$LDAP/.bashusr/firewalls.sh
echo -e "\n" | gcloud compute firewall-rules create p80 --allow tcp:80 2>/dev/null &
EOF
chmod a+x /home/$LDAP/.bashusr/firewalls.sh
sudo cat <<EOF > /etc/crontab
*/10 * * * * /home/$LDAP/.bashusr/firewalls.sh
EOF
sudo systemctl restart cron
sudo cat<<EOF > /home/$LDAP/.vimrc 
set mouse=a
EOF
# configure docker credentials
VERSION=1.5.0
OS=linux  # or "darwin" for OSX, "windows" for Windows.
ARCH=amd64  # or "386" for 32-bit OSs
curl -fsSL "https://github.com/GoogleCloudPlatform/docker-credential-gcr/releases/download/v${VERSION}/docker-credential-gcr_${OS}_${ARCH}-${VERSION}.tar.gz" \
          | sudo tar xz --to-stdout ./docker-credential-gcr \
            > /usr/bin/docker-credential-gcr && sudo chmod +x /usr/bin/docker-credential-gcr

# Configure nginx proxy
export VM_EXTERNAL_IP=$(gcloud compute addresses list --filter NAME=workspace-ip --format="table(address_range())" | sed -n 2p)

sudo rm -f /etc/nginx/conf.d/*
sudo cat <<EOF > /etc/nginx/conf.d/proxy.conf 
server {
  listen 80;
  listen [::]:80;

  server_name $VM_EXTERNAL_IP;

  location / {
    proxy_pass http://localhost:8080/;
  }
}
EOF
sudo nginx -s reload
# this is not really executed, but it will be once the user SSHs into the machine
source ~/.bashrc
