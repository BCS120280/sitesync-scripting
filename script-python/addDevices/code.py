null = None
false = False
true = True
import json
PIAddress = "https://pgwgen002923.mgroupnet.com:5590/api/v1/configuration"
componentID = "MQTT1"

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
	##
	dType = str(system.tag.readBlocking(['{0}/{1}.dataType'.format(tagPath, tagName)])[0].value)
	if "Float" in dType:
		return "Float32"
	elif "Int" in dType:
		return "int16"
	return dType
	
def generateTopic(tagPath):
	return "mpc/{0}".format(tagPath.replace("[default]PI Integration/", ""))
	
def generateStreamID(tagPath, tagName):
	
	return "mpc/{0}.$.{1}".format(tagPath.replace("[default]PI Integration/", ""), tagName)
	
def formatDataSelectionItem(tagPath, items, selectedData):
	unique_dict = {}
	for item in selectedData:
	    unique_dict[item['streamId']] = item
	
	for i in items:
		tagName = str(i['fullPath']).split('/')[-1]
		j = {

		    "selected" : true,
		
		    "name" : tagName,
		
		    "streamId" : generateStreamID(tagPath, tagName),
			 "dataFields": null,
		    "indexField": null,
		    "indexFormat": null,
		    "dataFilterId" : null,
			"dataType" : getDataType(tagPath, tagName),
		    "topic" : generateTopic(tagPath),
		    "valueField" : "$.{0}".format(tagName)
		
		  }
		counter = 0
		if generateStreamID(tagPath, tagName) not in unique_dict.keys():
			selectedData.append(j)
#		j = {
#	        "topic": generateTopic(tagPath),
#	        "metricName": tagName,
#	        "selected": true,
#	        "name": tagName,
#	        "streamId": generateStreamID(tagPath, tagName),
#	        "dataFilterId": null
#	    }
		
	return selectedData
	
def updateDataSelection(arrayOfTags, componentID, PIAddress):
	##implements PATCH to add new tags to data selection file
	try:
		results = []
		
		#return {"url":PIAddress, "componentID":componentID, "payload":json.dumps(arrayOfTags)}
			##add 1 attribute per call
		updateResults = system.piAdapter.updateDataSelection(componentID, json.dumps(arrayOfTags), PIAddress)
			
		return updateResults
		
	except Exception as e:
		return {"status":"error", "message":str(e)}
		
		
def addTagToPi(tagPath, componentID, PIAddress):
	##grab all tags
	items = getAttributesForTag(tagPath)
	existingConfig = getCurrentDataSelection(componentID, PIAddress)
	piTags = formatDataSelectionItem(tagPath, items, existingConfig)
	#system.tag.writeBlocking(["[default]New Tag"], [json.dumps(piTags)])
	results = updateDataSelection(piTags, componentID, PIAddress)
	return results
	
	
