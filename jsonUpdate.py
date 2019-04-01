import json
import os
import datetime

# Definition to use shell command
def run_cmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8')

# Definition to update the json file (WiFi part only)
def updateJsonWifi(fileNameJson, lastWifiScan, currentTime):

	# Check is the json file exists, if not it is created
	if not(os.path.isfile(fileNameJson)):
		f= open(fileNameJson,"w+")
		f.write("{\"bluetooth\":[],\"wifi\":[]}")
		f.close()

	with open(fileNameJson) as json_file:

		# Load the existing data in the json file
		data = json.load(json_file)

		# the last WiFi scan is compare to the json data
		for macScan in lastWifiScan:
			newMac = 1

			for d in data['wifi']:

				# the device scanned during the last scan has already been met before
				if d['mac'] == macScan[2]:
					newMac = 0;

					# if it was not currently active, then it is now active and a new time of meeting is created
					if d['active'] == "false":
						d['active'] = 'true'
						d['sawAt'] += (currentTime.strftime(" - from %d-%m-%Y_%H:%M:%S")) + " with ip " + macScan[0]
					# if it was currently active, then its current ip is compare to the ip it has the previous time, if it changed, it is updated in the data
					else:
						if d['currentIP'] != macScan[0]:
							d['sawAt'] += " change ip to " + macScan[0]
			
			# the device scanned during the last scan has never been met before, it is consequently added
			if(newMac):
				sawAt = currentTime.strftime("from %d-%m-%Y_%H:%M:%S") + " with ip " + macScan[0]
				data['wifi'].append({'mac': macScan[2],'active':'true','currentIP':macScan[0],'sawAt':sawAt,'name':macScan[3]})

		# look at all the wifi data to put inactive the wifi that was active but did not meet this time
		for d in data['wifi']:
			seen = 0
			if(d['active'] == 'true'):
				for macScan in lastWifiScan:
					if d['mac'] == macScan[2]:
						seen = 1
						break
				if not seen:
					d['active'] = 'false'
					d['sawAt'] += (currentTime.strftime(" - to %d-%m-%Y_%H:%M:%S"))

	# update the json file
	with open(fileNameJson, 'w') as outfile:  
	    json.dump(data, outfile, indent=4)

# Definition to update the json file (Bluetooth part only)
def updateJsonBluetooth(fileNameJson, lastBluetoothFile, currentTime):

	# Check is the json file exists, if not it is created
	if not(os.path.isfile(fileNameJson)):
		f= open(fileNameJson,"w+")
		f.write("{\"bluetooth\":[],\"wifi\":[]}")
		f.close()

	with open(fileNameJson) as json_file:

		# Load the existing data in the json file
		data = json.load(json_file)

		# Get only the mac address and the name of the device from the bluetooth log
		fileToRead = open(lastBluetoothFile + ".txt", "r")
		macName = []
		for line in fileToRead:
			if line.startswith(" "):
				line = line.strip()
				line = line.split(" - ")
				macName.append([line[1],line[0]])
		fileToRead.close()


		# the last Bluetooth scan is compare to the json data
		for macScan in macName:
			newMac = 1
			for d in data['bluetooth']:

				# the device scanned during the last scan has already been met before
				if d['mac'] == macScan[0]:
					newMac = 0;

					# if it was not currently active, then it is now active and a new time of meeting is created
					if d['active'] == "false":
						d['active'] = 'true'
						d['sawAt'] += (currentTime.strftime(" - from %d-%m-%Y_%H:%M:%S"))
			
			# the device scanned during the last scan has never been met before, it is consequently added
			if(newMac):
				sawAt = currentTime.strftime("from %d-%m-%Y_%H:%M:%S")
				data['bluetooth'].append({'mac': macScan[0],'name': macScan[1],'active':'true','sawAt':sawAt})

		# look at all the bluetooth data to put inactive the bluetooth that was active but did not meet this time
		for d in data['bluetooth']:
			seen = 0
			if(d['active'] == 'true'):
				for macScan in macName:
					if d['mac'] == macScan[0]:
						seen = 1
						break
				if not seen:
					d['active'] = 'false'
					d['sawAt'] += (currentTime.strftime(" - to %d-%m-%Y_%H:%M:%S"))


	# update the json file
	with open(fileNameJson, 'w') as outfile:  
	    json.dump(data, outfile, indent=4)

# Definition to write correctly the json file when the application exit
def closeProgram(fileNameJson):
	with open(fileNameJson) as json_file:
		data = json.load(json_file)

		# Set all the devices to inactive and write the last time they have been see

		for d in data['bluetooth']:
			if(d['active'] == 'true'):
				d['active'] = 'false'
				d['sawAt'] += (datetime.datetime.now().strftime(" - to %d-%m-%Y_%H:%M:%S"))

		for d in data['wifi']:
			if(d['active'] == 'true'):
				d['active'] = 'false'
				d['sawAt'] += (datetime.datetime.now().strftime(" - to %d-%m-%Y_%H:%M:%S"))

	with open(fileNameJson, 'w') as outfile:  
	    json.dump(data, outfile, indent=4)