import json
import re

def saveDevice(devEUI, appEUI, appKey, name, serialNumber, modelID, lat, lon,  description, provider, tagPath, image, user, appID = 0, tenantID = 1 ):
	appID = enterprise.tenant.getDefaultApp()
	deviceJSON = formatAddDeviceRequest(devEUI, appEUI, appKey, name, serialNumber, tenantID, modelID, description, appID)
	
	validationResults = validateDevice(deviceJSON, tagPath)
	if utils.resultParser.isResultSuccess(validationResults):
		system.perspective.print("pre-create device")
		deviceCreateResult = createDevice(deviceJSON)

		if utils.resultParser.isResultSuccess(deviceCreateResult):
			system.perspective.print("pre-create tag")
			tagPathSaveResult = saveTagPathForDevice(devEUI, provider, tagPath, name, tenantID)
			system.perspective.print("post-create tag {0}".format(tagPathSaveResult))
			if utils.resultParser.isResultSuccess(tagPathSaveResult):
				system.perspective.print("creating PI instance")
				
				message = "Successfully added device {0}".format(devEUI)
				fullTagPath = device.tagOperations.assembleFullPath(provider, tagPath, name)
				createPITemplate.createInstance(fullTagPath, name)
				system.perspective.print("post-create device")
				system.perspective.print(image)
				if image != None and len(image) > 1:
					imageSaveResult = device.images.saveImage(image, devEUI)
					if not utils.resultParser.isResultSuccess(imageSaveResult):
						message += ", but there was an error saving the image {0}".format(utils.resultParser.getResultMessage(imageSaveResult))
					tagSaveImage = device.tagOperations.updateImageTag(fullTagPath, image)
					if "Good" not in str(tagSaveImage[0]):
						message +=  ", but there was an error saving the image {0}".format(tagSaveImage[0])
				
				
				device.tagOperations.updateDescriptionTag(fullTagPath, description)
				device.tagOperations.updateInstallLocationTag(fullTagPath, lat, lon)
				device.tagOperations.installedBy(fullTagPath, user)
			
				
				return utils.resultParser.createResults(True, message)
			else:
				return tagPathSaveResult
			
		else:
			return deviceCreateResult
	else:
		return validationResults

def pathValidator(path):

	# Pattern explanation:
	# ^                 : Start of string
	# [A-Za-z0-9_]+     : The first character must be a letter, number, or underscore
	# [A-Za-z0-9_ ':-()] * : The second character and onward can be letters, numbers, underscores, spaces, or specific special characters
	# $                 : End of string
	# returns true for valid, False for invalid
	if path != None and path != "":
		pattern = r"^[A-Za-z0-9_][A-Za-z0-9_ /'':()-]*$"
		
		# Example usage
		return bool(re.match(pattern, path))
	else:
		return True

def charCheck(string, stringLength):
	if len(string) == stringLength:
		return True
	else:
		return False

def validateDevice(device, tagPath):
	isValid = True
	message = "Validation Error: "
	if not charCheck(device['devEUI'], 16):
		message += "devEUI not 16 characters, please review {0}; ".format(device['devEUI'])
		isValid = False
	if  not charCheck(device['applicationKey'], 32):
		message += "appKey not 32 characters, please review {0}; ".format(device['applicationKey'])
		isValid = False
	if  not charCheck(device['joinEUI'], 16):
		message += "joinEUI not 16 characters, please review {0}; ".format(device['joinEUI'])
		isValid = False
	if not pathValidator(tagPath):
		message += "Illegal characters found in tagPath {0}; ".format(tagPath)
		isValid = False
	if not pathValidator(device['name']) or '/' in device['name']:
		message += "Illegal characters found in device name {0}; ".format(device['name'])
		isValid = False
	if device["deviceModelID"] == -1:
		message += "Sensor type not selected; "
		isValid = False
	if isValid:
		message = "all checks passed"
	results = utils.resultParser.createResults(isValid, message)
	return results

	
def formatAddDeviceRequest(devEUI, appEUI, appKey, name, serialNumber, tenantID, modelID,  description, appID):
	j = {
	    "devEUI": devEUI.replace('-', '').lower().strip(),
	    "applicationKey": appKey.replace('-', '').lower().strip(),
	    "name": name,
	    "serialNumber": serialNumber,
	    "tenantID": tenantID,
	    "deviceModelID": modelID,
	    "joinEUI": appEUI.replace('-', '').lower().strip(), 
	    "description":description, 
	    "appID":appID
	}
	return j 
	
	
def createDevice(deviceRequest):
	try:
		d =json.dumps(dict(deviceRequest))
		system.perspective.print(type(d))
		results = system.sitesync.saveDevice(d)
	
		if results != None:
			
			result = json.loads(results)
			return result
		else:
			return utils.resultParser.createResults(False, "No response")
	except Exception as e:
		return utils.resultParser.createResults(False, str(e))

def preventNullBasePath(baseTagPath):
	if baseTagPath == None:
		return ""
	else:
		return baseTagPath			
			
def saveTagPathForDevice(devEUI, provider, path, name, tenantID=1):
	tagPathObject = {
			"devEUI":devEUI,
	        "tagProvider": provider,
	        "tagPathBase": preventNullBasePath(path),
	        "tagName": name, 
	        "tenantID":tenantID
	    }
	t = json.dumps(tagPathObject)
	system.perspective.print(t)
	results = system.sitesync.createTag(t)
	system.perspective.print(type(results))
	result = json.loads(results)
#	if utils.resultParser.isResultSuccess(result):
#		result = json.loads(device.tagOperations.saveTagPathForDevice(devEUI, provider, path, name))
	return result
	
