#!/bin/bash

# This script should be run on a default install of Raspbian: https://www.raspberrypi.org/downloads/raspbian/

#####----- CHECK ROOT -----#####

# credit: https://askubuntu.com/questions/15853/how-can-a-script-check-if-its-being-run-as-root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root - uses 'sudo' when necessary."
   exit 1
fi

#####----- CD TO src/ -----#####

cd "$(dirname "$0")"/..


#####----- INSTALL UPDATES -----#####

sudo apt update
sudo apt upgrade -y


#####----- INSTALL VNC SERVER -----#####

sudo apt install -y tightvncserver screen novnc xfonts-base


#####----- Auto-launch VNC server -----#####

sudo cp ./scripts/novnc.service /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable novnc


