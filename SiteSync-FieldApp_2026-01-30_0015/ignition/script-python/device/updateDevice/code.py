import json

def updateLocation(devEUI, lat, lon):
	results = system.sitesync.updateDeviceLocation(devEUI, lat, lon)
	
	result = json.loads(results)
	
	
	return result

def updateDevice(device):
	try:
		#system.perspective.print("sending device for update:")
		#system.perspective.print(json.dumps(device))
	#	system.print(device)
		results = system.sitesync.updateDeviceForm(device)
		
		result = json.loads(results)
		return result
	except Exception as e:
		#system.perspective.print("Error updating device: " + str(e))
		return "Error updating device: " + str(e)
		
def updateDeviceMetaData(metaDataJSON, devEUI):
	try:

		meta = json.dumps(metaDataJSON)
		results = system.sitesync.updateDeviceMetaData(meta, devEUI)
		if results != None:
			return json.loads(results)
		else:
			return {"status":"ERROR", "message":"nothing returned"}
	except Exception as e:

		return {"status":"ERROR", "message":"Error updating device: " + str(e)}
		
		
		
	
def formatUpdateDeviceRequest(devEUI, name,  description ):
	j = {
	   
	    "name": name,
	    "description":description, 
	    "devEUI":devEUI
	  
	}
	return json.dumps(j)