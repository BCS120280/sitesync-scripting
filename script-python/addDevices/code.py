null = None
false = False
true = True
import json
PIAddress = "https://pgwgen002923.mgroupnet.com:5590/api/v1/configuration"
componentID = "MQTT1"

# Cache for PI data selection to avoid re-fetching for every device during bulk upload.
# Call clearDataSelectionCache() before a bulk operation, then flushDataSelectionCache() after.
_dataSelectionCache = None
_dataSelectionDirty = False

def clearDataSelectionCache():
	"""Call before a bulk upload to initialize the cache."""
	global _dataSelectionCache, _dataSelectionDirty
	_dataSelectionCache = None
	_dataSelectionDirty = False

def flushDataSelectionCache():
	"""Call after a bulk upload to push all accumulated PI data selection changes in one call."""
	global _dataSelectionCache, _dataSelectionDirty
	if _dataSelectionDirty and _dataSelectionCache is not None:
		results = updateDataSelection(_dataSelectionCache, componentID, PIAddress)
		_dataSelectionDirty = False
		_dataSelectionCache = None
		return results
	_dataSelectionCache = None
	_dataSelectionDirty = False
	return {"status": "success", "message": "No pending PI data selection changes"}

def getCurrentDataSelection(componentID, PIAddress):
	try:
		selectedData = system.piAdapter.getDataSelection(componentID, "MQTT1", PIAddress)
		if selectedData != None:
			return json.loads(selectedData)
		else:
			return {"status":"error", "message":"No data returned"}
	except Exception as e:
		return {"status":"error", "message":str(e)}


def getAttributesForTag(rootTagPath):
	tags = system.tag.browse(rootTagPath, filter={"recursive":True})
	return tags

def getDataType(tagPath, tagName):
	dType = str(system.tag.readBlocking(['{0}/{1}.dataType'.format(tagPath, tagName)])[0].value)
	return mapDataType(dType)

def getDataTypeBatch(tagPath, tagNames):
	"""Read data types for multiple tags in a single readBlocking call."""
	paths = ['{0}/{1}.dataType'.format(tagPath, name) for name in tagNames]
	if not paths:
		return {}
	values = system.tag.readBlocking(paths)
	result = {}
	for i, name in enumerate(tagNames):
		dType = str(values[i].value) if values[i].quality.good else "Float32"
		result[name] = mapDataType(dType)
	return result

def mapDataType(dType):
	"""Map Ignition data types to PI-compatible OMF data types.

	Handles battery values and other sensor types that may use
	Boolean, String, Long, Double, or DateTime types.
	"""
	if dType is None:
		return "Float32"
	if "Float" in dType or "Double" in dType:
		return "Float32"
	elif "Int" in dType:
		return "int16"
	elif "Long" in dType:
		return "int32"
	elif "Bool" in dType:
		return "int16"
	elif "String" in dType:
		return "String"
	elif "Date" in dType or "Time" in dType:
		return "DateTime"
	# Default to Float32 for unrecognized types to prevent PI rejection
	return "Float32"

def generateTopic(tagPath):
	return "mpc/{0}".format(tagPath.replace("[default]PI Integration/", ""))

def generateStreamID(tagPath, tagName):

	return "mpc/{0}.$.{1}".format(tagPath.replace("[default]PI Integration/", ""), tagName)

def formatDataSelectionItem(tagPath, items, selectedData):
	unique_dict = {}
	for item in selectedData:
	    unique_dict[item['streamId']] = item

	# Batch read all data types at once instead of one-by-one
	tagNames = [str(i['fullPath']).split('/')[-1] for i in items]
	dataTypes = getDataTypeBatch(tagPath, tagNames)

	for i in items:
		tagName = str(i['fullPath']).split('/')[-1]
		streamId = generateStreamID(tagPath, tagName)
		if streamId not in unique_dict:
			j = {
			    "selected" : true,
			    "name" : tagName,
			    "streamId" : streamId,
			    "dataFields": null,
			    "indexField": null,
			    "indexFormat": null,
			    "dataFilterId" : null,
			    "dataType" : dataTypes.get(tagName, "Float32"),
			    "topic" : generateTopic(tagPath),
			    "valueField" : "$.{0}".format(tagName)
			  }
			selectedData.append(j)
			unique_dict[streamId] = j

	return selectedData

def updateDataSelection(arrayOfTags, componentID, PIAddress):
	##implements PATCH to add new tags to data selection file
	try:
		updateResults = system.piAdapter.updateDataSelection(componentID, json.dumps(arrayOfTags), PIAddress)
		return updateResults

	except Exception as e:
		return {"status":"error", "message":str(e)}


def addTagToPi(tagPath, componentID, PIAddress):
	"""Add a single device's tags to PI data selection.

	If a data selection cache is active (bulk mode), accumulates changes
	without sending to PI. Call flushDataSelectionCache() to send all at once.
	"""
	global _dataSelectionCache, _dataSelectionDirty

	items = getAttributesForTag(tagPath)

	# In bulk mode, use the cache to avoid repeated GET/PUT cycles
	if _dataSelectionCache is not None:
		_dataSelectionCache = formatDataSelectionItem(tagPath, items, _dataSelectionCache)
		_dataSelectionDirty = True
		return {"status": "success", "message": "Queued for batch PI update"}

	# Single device mode - fetch, merge, push immediately
	existingConfig = getCurrentDataSelection(componentID, PIAddress)
	if isinstance(existingConfig, dict) and existingConfig.get("status") == "error":
		return existingConfig
	piTags = formatDataSelectionItem(tagPath, items, existingConfig)
	results = updateDataSelection(piTags, componentID, PIAddress)
	return results

def beginBulkPIUpdate():
	"""Initialize bulk PI update mode. Call before processing multiple devices.

	This fetches the current PI data selection once and caches it.
	Each addTagToPi call then appends to the cache instead of
	doing a full GET+PUT cycle per device.
	"""
	global _dataSelectionCache, _dataSelectionDirty
	existingConfig = getCurrentDataSelection(componentID, PIAddress)
	if isinstance(existingConfig, dict) and existingConfig.get("status") == "error":
		_dataSelectionCache = []
	else:
		_dataSelectionCache = existingConfig
	_dataSelectionDirty = False
	return {"status": "success", "message": "Bulk PI update mode initialized"}

