import subprocess
import time
import datetime
from bluetooth import *
import os
import errno
import sys
import select

import jsonUpdate

FILE_NAME_CURRENT_WIFI_DEVICES = "currentWifiDevices"
FILE_NAME_CURRENT_BLUETOOTH_DEVICES = "currentBluetoothDevices"
FOLDER_NAME_LOGS = "logs"
FILE_NAME_JSON = "jsonData.json"

# Command to get my ip
GET_IP_CMD = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"

# Definition to use shell command
def run_cmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8') 


# Definition to update the file of the current WiFi devices in the network
def refreshCurrentWifiDevices(fileNameToRead, fileNameToWrite, currentTime):
	ip = []
	latency = []
	mac = []

	# By reading the last scan report, extract only the important information and format them into a javascript file readable for the html file

	fileToRead = open(fileNameToRead + ".txt", "r")
	# Prepare the data in different lists
	for line in fileToRead:
		if line.startswith("Nmap scan report for "):
			lineSplit = line.strip()
			lineSplit = lineSplit.split(" ")
			ip.append(" ".join(str(x) for x in lineSplit[4:]))
		if line.startswith("Host is up ("):
			lineSplit = line.strip()
			lineSplit = lineSplit.split(" ")
			latency.append(" ".join(str(x) for x in lineSplit[3:]))
		if line.startswith("MAC Address: "):
			lineSplit = line.strip()
			lineSplit = lineSplit.split(" ")
			mac.append(" ".join(str(x) for x in lineSplit[2:]))


	fileToWrite = open(fileNameToWrite + ".js", "w+")
	fileToWrite.write("wifiDevices = [")

	wifiDevices = []

	# Write into the javascript file, and in the mean time prepare a list to give to the definition updateJsonWifi in order to later on update the json file
	for i in range(len(ip)):
		if i > 0:
			fileToWrite.write(", \"")
		else:
			fileToWrite.write("\"")

		fileToWrite.write(str(ip[i]))


		if(len(latency)-1 >= i):
			fileToWrite.write(str(latency[i]) + str(mac[i]) + "\"")
			
			wifiDevices.append(ip[i].split())
			wifiDevices[i].append(latency[i])
			macSplit = mac[i].split()
			wifiDevices[i].append(macSplit[0])
			wifiDevices[i].append((" ".join(str(x) for x in macSplit[1:])))
		else:
			fileToWrite.write("\"")

	fileToWrite.write("];\n")

	fileToRead.close()
	fileToWrite.close()

	jsonUpdate.updateJsonWifi(FILE_NAME_JSON, wifiDevices, currentTime)


# Definition to update the file of the current Bluetooth devices in the network
def refreshCurrentBluetoothDevices(fileNameToRead, fileNameToWrite):
	devices = []

	# By reading the last scan report, extract only the important information and format them into a javascript file readable for the html file

	fileToRead = open(fileNameToRead + ".txt", "r")
	# Prepare the data in a list
	for line in fileToRead:
		if line.startswith(" "):
			devices.append(line.strip())

	fileToWrite = open(fileNameToWrite + ".js", "w+")
	fileToWrite.write("bluetoothDevices = [")

	# Write into the javascript file
	for i in range(len(devices)):
		if i > 0:
			fileToWrite.write(", \"")
		else:
			fileToWrite.write("\"")

		fileToWrite.write(str(devices[i])+"\"")

	fileToWrite.write("];")

	fileToRead.close()
	fileToWrite.close()


# Definition to scan WiFi devices
def scanWifi():
	
	# Get time and prepare nmap command
	currentTime = datetime.datetime.now()
	fileName = currentTime.strftime("logs/WiFi-%d-%m-%Y_%H:%M:%S")
	NMAP_CMD = "sudo nmap -sn " + myIp + "/24 -oN "  + fileName + ".txt --exclude " + run_cmd(GET_IP_CMD)

	# Execute nmap and output the result in a file name with the corresponding time
	print ("Performing WiFi inquiry...")
	run_cmd(NMAP_CMD)

	# Call the definition to update the javascript file containing the current WiFi devices detected and update the json file
	refreshCurrentWifiDevices(fileName, FILE_NAME_CURRENT_WIFI_DEVICES, currentTime)


# Definition to scan Bluetooth devices
def scanBluetooth():

	# Prepare filename
	currentTime = datetime.datetime.now()
	fileName = currentTime.strftime("logs/Bluetooth-%d-%m-%Y_%H:%M:%S")

	# Search bluetooth devices
	print ("Performing bluetooth inquiry...")
	nearby_devices = discover_devices(lookup_names = True, flush_cache = True)

	# Print the result in a file
	file = open(fileName + ".txt", "w+")
	file.write("Found " + str(len(nearby_devices)) + " devices\n")

	for name, addr in nearby_devices:
		file.write(" " + addr + " - " + name + "\n")
	file.close()

	# Call the definition to update the javascript file containing the current WiFi devices detected and update the json file
	refreshCurrentBluetoothDevices(fileName, FILE_NAME_CURRENT_BLUETOOTH_DEVICES)
	jsonUpdate.updateJsonBluetooth(FILE_NAME_JSON, fileName, currentTime)




# MAIN ALGORITHM START HERE

# Create a folder logs
try:
    os.makedirs(FOLDER_NAME_LOGS)
except OSError as exc: 
    if exc.errno == errno.EEXIST and os.path.isdir(FOLDER_NAME_LOGS):
        pass


# Get my ip, change the last 8 bit of host id to 0
myIp = run_cmd(GET_IP_CMD)
myIp = myIp.split(".")
myIp[len(myIp)-1] = 0
myIp = ".".join(str(x) for x in myIp)


# Start the scanning process
while(1):

	scanWifi()

	scanBluetooth()

	# Wait before scanning again
	print("Pause...")
	time.sleep(5)

	# Close the program by entering 'q'
	if(select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])):
		if(sys.stdin.read(1) == "q"):
			jsonUpdate.closeProgram(FILE_NAME_JSON)
			sys.exit()
