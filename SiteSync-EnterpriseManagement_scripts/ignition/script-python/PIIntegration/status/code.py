import json
def getTransmitterStatus():
	##returns connectivity status of MQTT Transmission clients
	return {}
	
def isUsingTransmission():
	return False
	
#	
#def adapterAPIPingStatus():
#	results = system.piAdapter.testConnection("adapter")
#	j = {"status":True, "message":"Adapter API is reachable"}
#	return j
#	
#	
#def PIWebAPIPingStatus():
#	
#	j = {"status":False, "message":"PI Web API is not reachable, SSL cert issue. Check logs for more information"}
#	return j
#	
	
import json
def getTransmitterStatus():
    ##returns connectivity status of MQTT Transmission clients
    return {}
    
def isUsingTransmission():
    return False
    
    
def adapterAPIPingStatus():
	settings = adapter.getAdapterSettings()
	j = system.piAdapter.testConnection(settings["apiURL"], settings["datasourceID"], "adapter")
	j = json.loads(j)
	if j['status']:
		j['message'] = "MQTT Adapter API is Reachable"
	return j
    
    
def PIWebAPIPingStatus():
  	settings = AF.getAFSettings()
  	j = system.piAdapter.testConnection(settings["url"] + "/dataservers", settings["token"], "AF")    
  	j = json.loads(j)
  	system.perspective.print(j)
  	if j['status']:
  		j['message'] = "PI Web API is Reachable"
  	return j