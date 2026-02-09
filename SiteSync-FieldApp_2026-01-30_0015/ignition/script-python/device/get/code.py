import json

def listDevices(tenantID):
	devices = json.loads(system.sitesync.listDevices(tenantID))
	return devices
	
def getDevice(devEUI):
	device = system.sitesync.getDevice(devEUI)
	if device != None:
		return json.loads(device)
	else:
		return {"status":"ERROR", "message":"Device " + devEUI + " not found"}
		
		
def getMetaData(devEUI):
	thisDevice = device.get.getDevice(devEUI)
	
	if 'metaData' in thisDevice.keys():
		if thisDevice['metaData'] != "":
			m = json.loads(thisDevice['metaData'])
			if type(m) == unicode:
				return json.loads(m)
			else:
				return m
		else:
			return {}
	else:
		return {}