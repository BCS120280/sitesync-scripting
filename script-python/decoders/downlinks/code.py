import json
def downlinkModel():
	##returns empty downlink model
	downlink = {
	"id":0, 
	"name":"", 
	"description":"", 
	"hexCommand":"",
	"port":0, 
	"deviceProfileID":1
	}
	return downlink
	
def saveDownlink(downlinkID, deviceProfileID, hexCommand, port, description, name):
	downlink = json.dumps({
		"id":downlinkID, 
		"name":name, 
		"description":description, 
		"hexCommand":hexCommand,
		"port":port, 
		"deviceProfileID":deviceProfileID
		})
	results = json.loads(system.sitesync.createDownlink(downlink))
	return results

def getDonwlinkByID(downlinkID):
	results = json.loads(system.sitesync.getDownlink(int(downlinkID)))
	return results
	
def listDownlinks(deviceProfileID):
	results = system.sitesync.getDownlinks(deviceProfileID)
	if results != None:
		return json.loads(results)
	else:
		return None
	
	
def deleteDownlink(downlinkID):
	results = json.loads(system.sitesync.deleteDownlink(downlinkID))
	return results
	
	
def getDownlinkFromList(downlinkID, listOfDownlinks):
	for d in listOfDownlinks:
		if d['id'] == downlinkID:
			return d
	return downlinkModel()
	
def sendDownlink(hexCode, port, devEUI, tenantID):
	results = system.sitesync.executeDownlink(devEUI, hexCode, port, tenantID);
	if results != None:
		return json.loads(results)
	
def processAnyInputs(downlink, inputText):
	##do hex validation
	if "{0}" in downlink:
		##convert inputtext to hex
		return downlink.format(inputText)
	else:
		return downlink