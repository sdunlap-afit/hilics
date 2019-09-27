#!/bin/bash


# This script should be run on a default install of Raspbian: https://www.raspberrypi.org/downloads/raspbian/

#####----- CHECK ROOT -----#####

# credit: https://askubuntu.com/questions/15853/how-can-a-script-check-if-its-being-run-as-root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root - uses 'sudo' when necessary."
   exit 1
fi


#####----- CHECK RPI HARDWARE -----#####

# credit: https://www.raspberrypi.org/forums/viewtopic.php?t=34678
R_PI=$(python -c "import platform; print 'raspberrypi' in platform.uname()")

if [ "$R_PI" != "True" ] ; then
    echo "ERROR: Raspberry pi hardware not detected. Edit this script to continue anyway."
    exit 1
fi


#####----- CD TO src/ -----#####

cd "$(dirname "$0")"/..


#####----- INSTALL UPDATES -----#####

sudo apt update
sudo apt upgrade -y


#####----- ENABLE SPI -----#####

# credit: https://raspberrypi.stackexchange.com/questions/96670/find-out-whether-spi-is-enabled-or-not
RET=$(raspi-config nonint get_spi)

if [ "$RET" -ne 0 ] ; then
    echo "Enabling SPI interface"
    sudo raspi-config nonint do_spi 0
else
    echo "SPI is already enabled"
fi



#####----- INSTALL DEPENDENCIES -----#####

sudo apt -y install python3-pil.imagetk




#####----- COPY SRC DIR -----#####


echo "Copying src files to ~/hilics"

mkdir ~/hilics
cp -r ./* ~/hilics
cp ./scripts/start.sh ~/
chmod +x ~/start.sh

echo "Setting up auto start"
mkdir -p ~/.config/lxsession/LXDE-pi
cp -f ./scripts/autostart ~/.config/lxsession/LXDE-pi/autostart



#####----- REBOOT -----#####
echo "Rebooting in 5 seconds"
sleep 5
sudo reboot

