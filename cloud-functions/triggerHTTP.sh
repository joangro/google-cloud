#!/bin/bash
ARGUMENTS=()
while [[ $# -gt 0 ]]
do
key="$1"
	case $key in
		-n|--name)
		C_F_NAME=$2
		shift
		shift
		;;
		-f|--file)
		FILE=$2
		shift
		shift
		;;

	esac
done

echo "Updating system components..."
sudo apt-get -qq update
sudo apt-get install -qq git -y

echo "Updating gcloud components..."
gcloud components update
gcloud components install beta

if [[ -z $FILE ]];then
	echo "Downloading default HTTP request file..."
	wget https://raw.githubusercontent.com/GoogleCloudPlatform/python-docs-samples/master/functions/helloworld/main.py	
fi
