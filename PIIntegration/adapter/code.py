import json
def getAdapterSettings():
	s = system.piAdapter.getSettings("adapter")
	if s != "null":
		return json.loads(s)
	return {}
	
def updateAdapterSettings(jsonObject):
	r = system.piAdapter.updateSettings(json.dumps(dict(jsonObject)), "adapter")
	return json.loads(r)
	
def getAdapterMQTTSettings():
	return {}
	
	
def existsInAdapterDataSelection(tagPath):
	##checks if in data selection
	creds = getPICredentials()
	sett = PIIntegration.settings.getSettings()
	path = pathFormatter(creds['datasourceID'], tagPath, sett['prefix'], sett['sourceFolder'])
	print path
	exists = system.piAdapter.doesTagExtistInPI(creds['apiURL'], creds['datasourceID'], path, "adapter")
	if exists != None:
		return json.loads(exists)
	else:
		return {"status":False, "message":"Did not find PITag"}

def getPICredentials():
	return getAdapterSettings()
	#return {"url":"",  "componentID":"", "prefix":"", "sourceFolder":"", "type":""}
		
def pathFormatter(repo, tagPath, prefix, sourceFolder):
	endpoint = "{0}/{1}".format( prefix, tagPath.replace(sourceFolder + '/', ""))
	return endpoint
	
	
def addToDataSelection(tagPathArray):
	##accepts tagPaths, adds to adapter data selection to allow for dataflow
	items = []
	creds = getPICredentials()
	for t in tagPathArray:
		requestBody = PIIntegration.tagOperations.formatRequest(t)
		items.append(requestBody)
	system.perspective.print(items)
	exists = system.piAdapter.createDataSelection(creds['datasourceID'], json.dumps(items), creds['apiURL'], creds['format'])
	system.perspective.print(exists)
	if exists != None:
		return json.loads(exists)
	else:
		return {"status":False, "message":"Did not find PITag"}
	
	return False

def removeFromDataSelection(specificStreamID):
	##accepts user inputted streamID, removes from adapter
	creds = getPICredentials()
	

	exists = system.piAdapter.createDataSelection(creds['datasourceID'],  creds['apiURL'], specificStreamID, creds['format'])
	if exists != None:
		return json.loads(exists)
	else:
		return {"status":False, "message":"Did not find PITag"}