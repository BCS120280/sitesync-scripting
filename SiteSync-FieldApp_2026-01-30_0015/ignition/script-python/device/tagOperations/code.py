import json
def regenerateTag(tagPath, devEUI):
	return False
	
	
def editExistingTag(devEUI, provider, path, name):
	tagPathObject = json.dumps({
				"devEUI":devEUI,
		        "tagProvider": provider,
		        "tagPathBase": preventNullBasePath(path),
		        "tagName": name
		    })
	
	results = system.sitesync.updateTag(tagPathObject)
	result = json.loads(results)
	return result
	
	
def saveTagPathForDevice(devEUI, provider, path, name, tenantID=1):
	##saves tag and creates instance in tag provider
	tagPathObject = {
			"devEUI":devEUI,
	        "tagProvider": provider,
	        "tagPathBase": preventNullBasePath(path),
	        "tagName": name, 
	        "tenantID":tenantID
	    }

	results = system.sitesync.createTag(json.dumps(tagPathObject))
	result = json.loads(results)
	return result
	
def preventNullBasePath(baseTagPath):
	if baseTagPath == None:
		return ""
	else:
		return baseTagPath	
		
def assembleFullPath(provider, basePath, name):
	if basePath == None or basePath == "":
		return "[" + provider + "]" + name
	else:
		return "[" + provider + "]" + basePath + "/" + name
	
def assembleBasePath(basePath, name):
	if basePath == None or basePath == "":
		return name
	else:
		return basePath + "/" + name
	
def updateTagValues(listOfTagPaths, listOfTagValues):
	
	results = system.tag.writeBlocking(listOfTagPaths, listOfTagValues)
	return results

			
def moveTag(originalTag, newTagLocation):
	results = system.tag.move([originalTag], newTagLocation)
	return results[0]
	
def renameTag(tagPath, newName):
	results = system.tag.rename(tagPath, newName, 'a')
	return results
	
	
def updateDescriptionTag(tagPathBase, description):
	tags = [tagPathBase + "/metaData/locationDescription"]
	values = [description]
	return updateTagValues(tags, values)

def installedBy(tagPathBase, description):
	tags = [tagPathBase + "/metaData/installed_by"]
	values = [description]
	return updateTagValues(tags, values)
	

	
def updateImageTag(tagPathBase, image):
	tags = [tagPathBase + "/metaData/image"]
	if 'data:image/png;base64,' not in image:
		image = "data:image/png;base64,{0}".format(image)
	values = [image]
	return updateTagValues(tags, values)
	
def updateInstallLocationTag(tagPathBase, lat, lon):
	tags = [tagPathBase + "/metaData/install_longitude", tagPathBase + "/metaData/install_latitude"]
	values = [lon, lat]
	return updateTagValues(tags, values)
	
def updateMetaData(tagPathBase, metaData):
	tags = [tagPathBase + "/metaData/customAttributes"]
	values = [metaData]
	return updateTagValues(tags, values)