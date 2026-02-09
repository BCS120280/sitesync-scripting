import json

def formatMetaData(row):
	requiredColumns = ["dev_eui", "join_eui", "app_key", 'deviceType', 'tagPath', 'description', 'name', 'serialNumber']
	meta = {}
	for k, v in row.items():
		if k not in requiredColumns:
			if v != "":
				meta[k] = v

	return meta
	
def formatName(d):
	name = d.get('name', "0")
	if name == "0":
	
		modelName = d.get('deviceType', '0').strip()
		devEUI = d.get("dev_eui", "0").strip()
		if devEUI != "0" and len(devEUI) > 4:
			
			name = modelName + devEUI[-4:]
			return name
		else:
			return modelName + devEUI
	else:
		return name
	
	
def generateTagPath(model, tenant, profileList):
	return model
	
	
def bulk_upload(deviceRequest, tagPath, row, tagProvider):
		##uploads device, creates tag
	results = device.createDevice.createDevice(deviceRequest)
	if utils.resultParser.isResultSuccess(results):

		deviceRequest = json.loads(deviceRequest)
		tagCreationResults = device.tagOperations.saveTagPathForDevice(deviceRequest['devEUI'], tagProvider, tagPath, deviceRequest['name'])

		if utils.resultParser.isResultSuccess(tagCreationResults):
		
			meta = formatMetaData(row)
			if len(meta.keys()) > 0:
				tagPathBase = device.tagOperations.assembleFullPath(tagProvider, tagPath, deviceRequest['name'])
				j = json.dumps(meta)
				updateMetaData = device.tagOperations.updateMetaData(tagPathBase, j)
				device.updateDevice.updateDeviceMetaData(meta, deviceRequest['devEUI'])
				system.perspective.print(updateMetaData)
				return tagCreationResults
			else:
				return results
		else:
		
		
			return tagCreationResults
	else:
		return results
		
		
def charCheck(string, stringLength):
	if len(string) == stringLength:
		return True
	else:
		return False

def uploadLine(row, deviceProfiles, tenantID, tagProvider):
	##outputs status message
	
	devEUI = row.get("dev_eui", "0").strip()
	name = formatName(row)
	if charCheck(devEUI, 16):
		joinEUI = row.get("join_eui", "0000000000000000").strip()
		if charCheck(joinEUI, 16):
			appKey = row.get("app_key", '0').strip()
			if charCheck(appKey, 32) > 0:
				modelName = row.get('deviceType', '0').strip()
				if len(modelName) > 1: 
					modelID = decoders.model.findModelIDByName(deviceProfiles, modelName)
					if modelID > 0:
						serialNumber = row.get('serialNumber', None)
						description = row.get('description', '') 
						tagPath = row.get('tagPath', '') 
						formattedDevice = device.createDevice.formatAddDeviceRequest(devEUI, joinEUI, appKey, name, serialNumber, tenantID, modelID, 0 , 0, description)
					
						status = bulk_upload(formattedDevice, tagPath, row,  tagProvider)
				
				
						if utils.resultParser.getResultMessage(status) == "Error creating tag. Tag may already exist and cannot be overwritten.":
							status["status"] = "Warning"
						else:
							status['status'] = status['messageType'].upper()
					else:
						status = {"message":"Sensor type uploaded not recognised, please create a device profile with the name: " +  modelName, "status":"error", "deviceName":name, "devEUI":devEUI}
						
				else:
					status = {"message":"No Sensor Type found, not uploaded", "status":"error", "deviceName":name, "devEUI":devEUI}
				
			else:
				status = {"message":"appkey is not 32 characters, upload not attempted", "status":"error", "deviceName":name, "devEUI":devEUI}
				
		else:
			status = {"message":"joinEUI is not 16 characters, upload not attempted", "status":"error", "deviceName":name, "devEUI":devEUI}
			
	else:
		status = {"message":"DevEUI is not 16 characters, upload not attempted", "status":"error", "deviceName":name, "devEUI":devEUI}

	return status
	
	