<div>
<img align="left" src="./images/afit-logo.png" height="100" title="HILICS"><img align="right" src="./images/ccr-logo.png" height="100" title="HILICS">  
</div>

<br clear="all" />
<br>

# Install Raspbian

* Assemble your Raspberry Pi and touchscreen.

* Download the latest [Raspbian distro with desktop](https://www.raspberrypi.org/downloads/raspbian/) and follow the [installation guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) for a default setup. NOTE: HILICS has only been tested using Raspbian Buster, but should work on other versions as well. 

* After Raspbian is installed, follow the instructions to configure keyboard and time settings, install updates, and reboot.

* Once finished, you will need to connect a mouse and keyboard or [enable SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/) to continue.


# Download python files

* Run the following commands in a terminal to install HILICS.

```
cd /tmp/
git clone https://github.com/sdunlap-afit/hilics.git

chmod +x ./hilics/src/scripts/install.sh
./hilics/src/scripts/install.sh

rm -r /tmp/hilics
```


<br><br><br>

Return: [Build a kit](./README.md)

Next: [Hardware assembly](./Hardware_Assembly.md)