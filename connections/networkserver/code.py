import json 

def loadNetworkSettings(tenantID):
	js = system.sitesync.getJoinServerSettings(tenantID)
	if js != None and js != "null" and "error" not in js.lower():
		settings = json.loads(js)
		return settings
	else:
		return {}
	
	
def saveNetworkSettings(tenantID, networkType, joinServerUN, joinServerPW,
						apiToken, serverURL, nwsID, appID, defaultProfileID):
	nws = json.dumps({'apiToken':apiToken.strip(), 
	'serverUrl': serverURL.strip(), 
	"userName":joinServerUN.strip(), 
	"password":joinServerPW.strip(),
	'id': nwsID, 
	"tenantID":tenantID,
	'applicationID': appID.strip(), 
	'serverType':networkType.strip(),
	"defaultDeviceProfileID":defaultProfileID.strip()
	})
	results = json.loads(system.sitesync.updateJoinServerImpl(nws))
	return results
	
	
def testAPI(tenantID):
	results = json.loads(system.sitesync.testJoinAPIImpl(tenantID))
	return results
	
	
def showAppropriateOptions(networkType, controlType):
	##accepts network type, returns boolean if control type should be shown
	controlType = controlType.upper()
	networkType = networkType.upper()
	if networkType == "CHIRPSTACK" or networkType == "TTN" or networkType == "LORIOT":
		if controlType == "TOKEN":
			return True
		elif controlType == "OAUTH":
			return False
		elif controlType == "DEVICEPROFILE" and networkType == "CHIRPSTACK":
			return True
		else:
			return False
			
	else:
		if controlType == "TOKEN":
			return False
		elif controlType == "OAUTH":
			return True
		else:
			return False
		