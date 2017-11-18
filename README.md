# Home Automation

### This is a simple home automation project.

I'm using the Message Queue Telemetry Transport (MQTT) protocol to control my IoT devices.

The project has two parts:
- **MQTT Server:** Need a machine with IP open on the internet to control on the house remotely, like Digital Ocean.
- **MQTT Devices:** Need a machine only with internet access, like a Raspberrt PI. This one will receive commands to control stuffs like your TV, lights or another devices.

You can control devices who already implement MQTT protocal only using the MQTT Server, the second part (MQTT Devices) is not necessary in this case.

## MQTT Server
I have a MQTT server and a HTTP bridge for this server. The bridge is for use [IFTTT](https://ifttt.com) with Google Assistente and be able to control home devices with voice command on Android ou Google Home.

I'm using Mosquito, it is a MQQT Server for Python.

On Linux machines follows the steps:

sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients

For more details and other OS, please follow [this](http://www.steves-internet-guide.com/install-mosquitto-broker/) tutorial.