<div>
<img align="left" src="./images/afit-logo.png" height="100" title="HILICS"><img align="right" src="./images/ccr-logo.png" height="100" title="HILICS">  
</div>
<br clear="all" />
<br>

# RSLinx setup 

RSLinx is a utility that facilitates communication between RSLogix Micro and Rockwell PLCs. In order for RSLogix to talk to the PLC, RSLinx must first be configured.

**Before you begin this guide, make sure that [RSLinx is installed](./Rockwell_Tools.md) and that you can ping the MicroLogix 1100.**


1. Open RSLinx and click the RSWho icon.

<img src="./images/plc_init/01_rslinx_config.png"  width="500">

2. Click "Communications >> Configure Drivers..."

<img src="./images/plc_init/02_rslinx_config.png"  width="500">

3. In the Configure Drivers window, select "EtherNet/IP Driver" from the dropdown menu.

<img src="./images/plc_init/03_rslinx_config.png"  width="500">

4. Click "Add New".

<img src="./images/plc_init/04_rslinx_config.png"  width="500">

5. You can rename the driver if you like, but the default name is fine. Click "OK".

<img src="./images/plc_init/05_rslinx_config.png"  width="500">

6. In the new window, choose "Browse Local Subnet" and select the network interface that is connected to the PLC or the PLC network. 

	Click "OK".

<img src="./images/plc_init/06_rslinx_config.png"  width="500">


7. If all goes well, RSLinx should automatically find your PLC and add it to the device list under the driver. This process may take some time depending on your subnet configuration.

	Note: As long as this window is open, RSLinx will browse your subnet looking for new PLCs.

<img src="./images/plc_init/07_rslinx_config.png"  width="500">










<br><br><br>

Previous: [Configure PLC network settings](./PLC_Net_Config.md)

Return: [Build a kit](./README.md)

Next: [Configure RSLogix project](./RSLogix_Net_Config.md)
