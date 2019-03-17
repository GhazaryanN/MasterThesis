import json
import os
import datetime

# Definition to use shell command
def run_cmd(cmd):
	return subprocess.check_output(cmd, shell=True).decode('utf-8')

def updateJsonWifi(fileNameJson, lastWifiScan, currentTime):

	if not(os.path.isfile(fileNameJson)):
		f= open(fileNameJson,"w+")
		f.write("{\"bluetooth\":[],\"wifi\":[]}")
		f.close()

	with open(fileNameJson) as json_file:
		data = json.load(json_file)

		for macScan in lastWifiScan:
			newMac = 1
			for d in data['wifi']:
				if d['mac'] == macScan[3]:
					newMac = 0;
					if d['active'] == "false":
						d['active'] = 'true'
						d['sawAt'] += (currentTime.strftime(" - from %d-%m-%Y_%H:%M:%S")) + " with ip " + macScan[1]
					else:
						if d['currentIP'] != macScan[1]:
							d['sawAt'] += " change ip to " + macScan[1]
			
			if(newMac):
				sawAt = currentTime.strftime("from %d-%m-%Y_%H:%M:%S") + " with ip " + macScan[1]
				data['wifi'].append({'mac': macScan[3],'macName': macScan[4],'name': macScan[0],'active':'true','currentIP':macScan[1],'sawAt':sawAt})

				#run_cmd("sudo nmap -O --osscan-guess " + macScan + " -oN temp.txt")

				#run_cmd("rm temp.txt")


		for d in data['wifi']:
			seen = 0
			if(d['active'] == 'true'):
				for macScan in lastWifiScan:
					if d['mac'] == macScan[3]:
						seen = 1
						break
				if not seen:
					d['active'] = 'false'
					d['sawAt'] += (currentTime.strftime(" - to %d-%m-%Y_%H:%M:%S"))


	with open(fileNameJson, 'w') as outfile:  
	    json.dump(data, outfile, indent=4)

def updateJsonBluetooth(fileNameJson, lastBluetoothFile, currentTime):

	if not(os.path.isfile(fileNameJson)):
		f= open(fileNameJson,"w+")
		f.write("{\"bluetooth\":[],\"wifi\":[]}")
		f.close()

	with open(fileNameJson) as json_file:
		data = json.load(json_file)

		fileToRead = open(lastBluetoothFile + ".txt", "r")

		macName = []
		for line in fileToRead:
			if line.startswith(" "):
				line = line.strip()
				line = line.split(" - ")
				macName.append([line[1],line[0]])

		fileToRead.close()


		for macScan in macName:
			newMac = 1
			for d in data['bluetooth']:
				if d['mac'] == macScan[0]:
					newMac = 0;
					if d['active'] == "false":
						d['active'] = 'true'
						d['sawAt'] += (currentTime.strftime(" - from %d-%m-%Y_%H:%M:%S"))
			
			if(newMac):
				sawAt = currentTime.strftime("from %d-%m-%Y_%H:%M:%S")
				data['bluetooth'].append({'mac': macScan[0],'name': macScan[1],'active':'true','sawAt':sawAt})


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


	with open(fileNameJson, 'w') as outfile:  
	    json.dump(data, outfile, indent=4)

def closeProgram(fileNameJson):
	with open(fileNameJson) as json_file:
		data = json.load(json_file)

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