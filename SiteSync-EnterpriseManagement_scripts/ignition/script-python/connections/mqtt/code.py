import json

def getMqttSettings(tenantID):
	m = system.sitesync.getMQTTSettings(tenantID)
	if m != None and m != "null":
		mqttSettings = json.loads(m)
		mqttSettings['useTls'] = utils.boolConverters.getBool(mqttSettings['useTls'])
		mqttSettings['useAuthentication'] = utils.boolConverters.getBool(mqttSettings['useAuthentication'])
		return mqttSettings
	else:
		return None
	
	
	
def saveMqttSettings(url,  un, pw, tenantID, connectionName, 
						tlsVerification, protocol, brokerID, port, auth):
	brokerSettings =  json.dumps({
	            "id": brokerID,
	            "connectionProtocol": protocol.strip(),
	            "qos": 0,
	            "brokerAddress": url.strip(),
	            "brokerPort": port.strip(),
	            "useTls": utils.boolConverters.getInt(tlsVerification),
	            "useAuthentication":  utils.boolConverters.getInt(auth),
	            "userName":un.strip(), 
	            "password":pw.strip(),
	            "tenantID":tenantID, 
	            "connectionName":connectionName.strip()
	            
	            
	        })
	
	result = system.sitesync.updateMqttSettings(brokerSettings)
	r = json.loads(result)
	return r
	

	
def saveMqttTopics(topic, brokerID):
	topicObject = json.dumps({"mqttBrokerId":brokerID, "mqttTopic":topic })
	results = json.loads(system.sitesync.saveMQTTTopics(topicObject))
	return results
	
def startMQTTConnection(tenantID):
	startConnection = json.loads(system.sitesync.startMQTTConnectionImpl(tenantID))
	return startConnection
	
	
def stopMQTTConnection(tenantID):
	stopConnection = json.loads(system.sitesync.breakMQTTConnectionImpl(tenantID))
	return stopConnection
	
	
def getMqttTopics(brokerID):
	topics = json.loads(system.sitesync.getMQTTTopics(brokerID))
	if topics != None and  len(topics) > 0:
		topic = topics[0]['mqttTopic']
	else:
		topic = ""	
	
	return topic
	
	

	