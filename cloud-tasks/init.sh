#!/bin/bash
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
	-n|--name)
	VIRTUALENV_NAME="$2"
	shift
	shift
	;;
esac
done

echo "Configuring machine for cloud tasks..."
echo "Updating repository..."
sudo apt-get -qq update
sudo apt-get -qq install python-setuptools python-dev build-essential
sudo apt-get -qq install --upgrade pip
sudo pip install -q virtualenv
	
if [ -n "$VIRTUALENV_NAME" ]; then
	echo "Creating virtualenv with name ${VIRTUALENV_NAME}..."
	virtualenv ${VIRTUALENV_NAME}
	echo -e "\nPlease activate the environment by running\n\t
		source ${VIRTUALENV_NAME}/bin/activate"
fi

echo -e "\nPlease use the following commands to set up the environment\n\t 
	pip install -r requirements.txt"
