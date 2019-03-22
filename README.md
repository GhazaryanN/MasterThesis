# MasterThesis
Here is the repository of the work I have done during my Master Thesis in the University Paul Sabatier in Toulouse. It is about Security Supervision for IoT.

## Getting Started
One part consist in scanning the network environment by WiFi and Bluetooth.
Another part is a code written in the Arduino IDE for a NodeMCU, it consists to connect the NodeMCU to a network and to send on a web server the data it receives from a temperature/humidity sensor DHT22.

### Prerequisites
For the first part, you need a Linux environment, with Python 3, the command nmap and pybluez installed. You also need to have the security privileges. In this part, an HTML page is available and will be updated, it is recommanded to open it with Firefox (it is for sure working with it, and not with Google Chrome, the other web browser have not been tested). Be sure to download the 3 files (jsonUpdate.py, main.html, scanWifiBluetooth.py) and to keep them in the same directory.
For the second part, you will need a NodeMCU in order to be able to upload the code, and a sensor DHT22. To upload the code you need the Arduino IDE with the library ESP8266 installed.

## Run
For the first part, once all the prerequisites are owned, run

```
python3 scanWifiBluetooth.py
```

Logs files will be created in a repository /logs, where a file will be created for each WiFi scan and for each Bluetooth scan, giving the date, the hour, and what has been scan. The HTML page will be updated and you will be able to see in real time what is currently in the network, and an history of all the devices that have been found once, at what time and with what mac/ip address. The scan is repeated every 5 seconds, it is for demonstration purpose only. The program can be quit by typing 'q' and enter in the terminal. The program will automatically close after the break of 5 seconds. (Please be aware that you will not be able to type 'q' during the WiFi scan, the nmap command is blocking the input at this moment)


For the second part, once you upload the code in your NodeMCU, connect it with the DHT22 sensor, and the NodeMCU should connect and the network given in the code automatically. Then, with a device connected on the same network, you can enter the ip address of the NodeMCU in a web browser and you will be able to see in live the temperature and the humidity detected by the sensor.

## Author
* **Nune Ghazaryan**
