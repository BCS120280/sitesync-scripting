import json

def getDecoder(modelID):
	try:
		decoder = system.sitesync.getDecoder(modelID)
		return json.loads(decoder)
	except Exception as e:
		return {}
	
def validateDecoder(decoderText):
	decoder = system.sitesync.validateDecoder(decoderText)
	return json.loads(decoder)
	
def testDecoder(decoderText, hexPayload, port):
	results = system.sitesync.testDecoder(decoderText, hexPayload, port)
	return json.loads(results)

def testApiDecoder(decoderId, hexPayload, port, devEui):
	results = system.sitesync.testApiDecoder(decoderId, hexPayload, port, devEui)
	return json.loads(results)
	
def updateDecoder(tenantID, decoderID, decoderName, content, decoderType):
	decoder = json.dumps({
	"name":decoderName, 
	"decoderType":decoderType, 
	"code":content, 
	"tenantID":tenantID, 
	"id":decoderID
	})
	decoderResult = system.sitesync.updateDecoder(decoder)
	return json.loads(decoderResult)
	
def listDecoders(tenantID):
	decodeList = system.sitesync.listDecoders(tenantID)
	if decodeList != None:
		return json.loads(decodeList)	
	else:
		return None

def addDecoder(tenantID, name):
	decoder = json.dumps({
		"name":name, 
		"decoderType":"JS", 
		"tenantID":tenantID, 

		})
	results = system.sitesync.createDecoder(decoder)	
	return json.loads(results)
	
def updateAPI(modelID, url, token, isOAuth, username, password, name, payloadFormat):
	api = json.dumps({
			"name":"New API Connection", 
			"apiToken":token, 
			"apiURL":url, 
			"decoder":modelID ,
			"authenticationType":isOAuth,
			"authenticationCreds":token,
			"apiUserName":username,
			"apiPassword":password,
			"payloadFormat":payloadFormat
			
			})
	results = system.sitesync.updateAPIConnection(api)
	return json.loads(results)

	
def loadAPI(modelID):
	try:
		api = system.sitesync.getAPIConnection(modelID)
	except:
		api = None
	if api != None and api != "null":
		return json.loads(api)
	else:
		api = {
				"name":"New API Connection", 
				"apiToken":None, 
				"apiURL":None, 
				"decoder":modelID, 
				"authenticationType":"NONE",
				"authenticationCreds":"",
				"apiUserName":"",
				"apiPassword":""
				
				
				}
		return api