import re

def processFile(rows, deviceProfileList, selectedTenant, selectedApp, selectedUseCase, selectedTenantID, selectedDeviceProfileID, selectedAppID, tagProvider ):
	#sample row
	#{
#  "deviceType": "TE-Vibration",
#  "join_eui": "BCAF91C1D1000008",
#  "app_key": "39A0A543496C0B85A1227B588C007103",
#  "tagPath": "",
#  "tagExists": "",
#  "name": "",
#  "description": "",
#  "firmware_version": "",
#  "hardware_version": "",
#  "app_id": "",
#  "dev_eui": "BCAF91C1D100001D"
#}
	
	devices = []
	for row in rows:
		device = {}
		deviceType = getDeviceModel(selectedDeviceProfileID, row, deviceProfileList)
		deviceTypeID = getDeviceModelID(selectedDeviceProfileID, row, deviceProfileList)
		device['deviceType'] = deviceType
		device['deviceTypeID'] = deviceTypeID
		device['tagProvider'] = tagProvider
		device['tenantID'] = selectedTenantID
		device['app_key_valid'] = validator(row.get("app_key", ""), 32)
		device['app_key'] =  validatorReturnValue(row.get("app_key", ""), 32, "app_key")
		device['join_eui_valid'] =  validator(row.get("join_eui", ""), 16)
		device['join_eui'] =  validatorReturnValue(row.get("join_eui", ""),16, "join_eui")
		device['dev_eui_valid'] =  validator(row.get("dev_eui", ""), 16)
		device['dev_eui'] =  validatorReturnValue(row.get("dev_eui", ""),16, "dev_eui")
		device['name'] = formatName(row)
		device['description'] = row.get('description', "")
		device['firmware_version'] = row.get('firmware_version', "")
		device['hardware_version'] = row.get('hardware_version', "")
		device['location'] = row.get('location', "")
		device['tagPath'] = selectedUseCase
		device['metaData'] = formatMetaData(row)
		device['serial_number'] = row.get('serial_number', None)
		device['uploadMessage'] = deviceParserStatus(device)
		device['uploadStatus'] = canUpload(device['uploadMessage'])
		device['appID'] = selectedAppID
		devices.append(device)
	return devices
	
	
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
	return True

def deviceParserStatus(device):
	message = ""
	if not device['dev_eui_valid']:
		message += device['dev_eui']
	if not device['app_key_valid']:
		message += device['app_key']
	if not device['join_eui_valid']:
		message += device['join_eui']
	if not pathValidator(device['tagPath']):
		message += "Error in tag path, illegal characters"
	if not pathValidator(device['name']):
		message += "Error in device name, illegal characters"
	if message == "":
		message = "Device can be uploaded"
	return message
	
def canUpload(deviceStatus):
	if deviceStatus == "Device can be uploaded":
		return True
	else:
		return False

def deviceChecker(row, deviceName):
	deviceType = row.get('deviceType', '')
	if deviceType != '':
		return deviceType
	else:
		return deviceName
		
def deviceIDChecker(row, deviceTypeID, deviceProfiles):
	
	deviceType = row.get('deviceType', '')
	if deviceType != '':
		modelID = decoders.model.findModelIDByName(deviceProfiles, modelName)
		return modelID
	else:
		return deviceName
	

def validator(string, stringLength):
	string = string.replace("-", "").replace(" ", "").strip()
	if len(string) == stringLength:
		return True
	else:
		return False

def validatorReturnValue(string, stringLength, fieldName):
	string = string.replace("-", "").replace(" ", "").strip()
	if len(string) == stringLength:
		return string.lower()
	else:
		message = fieldName + " must be " + str(stringLength) + " characters long, is " + str(len(string)) + " characters long."
		return message

def getSpecialColumns():
	requiredColumns = ["dev_eui", "join_eui", "app_key", 'name', 'description', 'device_type','deviceType', "firmware_version","hardware_version", 'location' ]
	return requiredColumns
	
	
def formatMetaData(row):
	requiredColumns = getSpecialColumns()
	meta = {}
	for k, v in row.items():
		if k not in requiredColumns:
			if v != "":
				meta[k] = v

	return meta
	
	
def formatName(d):
	##generate a name if missing
	name = d.get('name', '0')
	if name == '0' or name == "":
		modelName = d.get('deviceType', '0').strip()
		devEUI = d.get("dev_eui", "0").strip()
		if devEUI != "0" and len(devEUI) > 4:
			
			name = modelName + devEUI[-4:]
			return name
		else:
			return modelName + devEUI
	else:
		#use uploaded name
		return name.strip()
		
		

	
	
def getDeviceModelID(selectedDeviceProfileID, row, profileList):
	deviceModelName = row.get("deviceType", "")
	system.perspective.print("Sheet loaded device model:" + deviceModelName)
	if deviceModelName == "":
		##device type not uploaded in sheet, use form selected device profile
		return selectedDeviceProfileID
	else:
		
		for m in profileList:
			if m['label'] == deviceModelName:
				return m['value']
		#if not found in the device profile array
		return -1 #"Profile ID for deviceProfile {0} not found".format(selectedDeviceProfileID)
		
		
def getDeviceModel(selectedDeviceProfileID, row, profileList):
	deviceModelName = row.get("deviceType", "")
	if deviceModelName == "":
		##device type not uploaded in sheet, use form selected device profile
		for m in profileList:
			if m['value'] == selectedDeviceProfileID:
				return m['label']
		#if not found in the device profile array
		return "Profile name for deviceProfileID {0} not found".format(selectedDeviceProfileID)
	else:
		return deviceModelName
		
		
		
##=====actual upload =======#
	
def bulk_upload(deviceRequest, tagPath, row, tagProvider):
		##uploads device, creates tag
	try:
		system.perspective.print("uploading device")
		system.perspective.print(row)
		results = device.createDevice.createDevice(deviceRequest)
		system.perspective.print(results)
		if utils.resultParser.isResultSuccess(results):
			system.perspective.print("device upload was successful")
			#deviceRequest = json.loads(deviceRequest)
			system.perspective.print("creating tag: " + tagPath)
			tagCreationResults = device.tagOperations.saveTagPathForDevice(row['dev_eui'], tagProvider, tagPath, row['name'])
			system.perspective.print("tag creation status: ")
			meta = row['metaData'] #formatMetaData(row)
			#system.perspective.print(meta)
			if len(meta.keys()) > 0:
				try:
					system.perspective.print("uploading meta")
					#if metadata exists, upload it into the db and onto a tag
	
					tagPathBase = device.tagOperations.assembleFullPath(tagProvider, tagPath, row['name'])
					#j = json.dumps(meta)
					system.perspective.print("tag path:" + tagPathBase)
					updateMetaData = device.tagOperations.updateMetaData(tagPathBase, meta)
					system.perspective.print(updateMetaData)
					device.updateDevice.updateDeviceMetaData(meta, deviceRequest['devEUI'].lower())
					system.perspective.print(updateMetaData)
				except Exception as e:
					system.perspective.print(str(e))
			if utils.resultParser.isResultSuccess(tagCreationResults):
			
				return tagCreationResults
			else:
				return results
			#else:
				#return tagCreationResults
		else:
			return results
	except Exception as e:
		return 	 {"message":str(e), "status":"error", "deviceName":"", "devEUI":deviceRequest['devEUI']}
		
		
def doUpload(d):
	#formatAddDeviceRequest(devEUI, appEUI, appKey, name, serialNumber, tenantID, modelID, lat, lon,  description, appID=None)
	status = device.createDevice.saveDevice(d['dev_eui'], d['join_eui'], d['app_key'], d['name'], d['serial_number'], d['deviceTypeID'], 0,0, d['description'], d['tagProvider'], d['tagPath'], None, "Bulk Upload", d['appID'], d['tenantID'])
#	formattedDevice = device.createDevice.formatAddDeviceRequest(d['dev_eui'], d['join_eui'], d['app_key'], d['name'], d['serial_number'], 
#	
#	d['tenantID'], d['deviceTypeID'], 0 , 0, d['description'], d['appID'])					
#	status = bulk_upload(formattedDevice, d['tagPath'], d,  'default')
	return status
	
	
def createFileForDownload():
	headers = ["dev_eui", "join_eui", "app_key", "name"]
	 
	# Then create an empty list, this will house our data.
	data = []
	 
	# Finally, both the headers and data lists are used in the function to create a Dataset object
	data = system.dataset.toDataSet(headers, data)
	csv = system.dataset.toCSV(data)
	return csv