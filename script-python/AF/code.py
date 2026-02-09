import json
def getAFSettings():
	s = system.piAdapter.getSettings("webAPI")
	if s != "null":
		return json.loads(s)
	return {}
	
def doesPITagExist(tagPath):
	##checks if in data selection
	creds = settings.getSettings()
	AFsettings = getAFSettings()
	path = pathFormatter(AFsettings['repository'], tagPath, creds['prefix'], creds['sourceFolder'])
	system.perspective.print(path)
	exists = system.piAdapter.doesTagExtistInPI(AFsettings['url'], AFsettings['token'], path, "AF")
	if exists != None:
		return json.loads(exists)
	else:
		return {"status":False, "message":"Did not find PITag"}
		
		
def createPITag(tagPath):
	creds = getPICredentials()
	requestBody = tagOperations.formatRequest(tagPath)
	
	createResult = system.piAdapter.createAFTag(creds['url'], json.dumps(requestBody), creds['token'])
	if createResult != None:
		return json.loads(createResult)
	else:
		return {"status":False, "message":"Did not get a response for creating a PI tag"}

	
def updatePITag(tagPath):
	creds = getPICredentials()
	requestBody = tagOperations.formatRequest(tagPath)
	createResult = system.piAdapter.updateAFAttributes(creds['url'], json.dumps(requestBody), creds['token'])
	
	if createResult != None:
		return json.loads(createResult)
	else:
		return {"status":False, "message":"Did not get a response for updating a PI tag"}
	
def getPICredentials():
	return getAFSettings()
	##return {"url":"", "token":"", "repo":"", "prefix":"", "sourceFolder":""}
	
def pathFormatter(repo, tagPath, prefix, sourceFolder):
	p = tagPath.replace(sourceFolder + '/', "")
	parts = p.rsplit("/", 1)
	ss = ".$.".join(parts)
	endpoint = "{0}\{1}/{2}".format(repo, prefix,ss) ##tagPath.replace(sourceFolder + '/', ""))
	return endpoint
	
def getPiTagPath(tagPath):
	return tagPath
	
def saveAFSettings(jsonObject):
	r = system.piAdapter.updateSettings(json.dumps(dict(jsonObject)), "webAPI")
	return json.loads(r)