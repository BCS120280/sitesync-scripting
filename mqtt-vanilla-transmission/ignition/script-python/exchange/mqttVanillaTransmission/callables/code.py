def resolvePublishParameters(
		tagPathFull, tagQualifiedValue,
		readTagProps, qos, retain,
		rootPathsToCut, topicPrefix,
		payloadFormat, timestampFormat, qualityFormat, 
		ConfigError, DropReason):
	"""Function that will resolve publish parameters such as topic, payload, QoS, retain
	based on given tag change data and config tags 
	
	Parameters
	--------------
	tagPathFull : string : Full path passed from tag change event
	tagQualifiedValue : Object : Qualified Value object passed from tag change event
	qos : int : Description in UDT tag's documentation
	retain : bool : Description in UDT tag's documentation
	rootPathsToCut : list : String array tag Cut From Tag Path, Description in its documentation
	topicPrefix : string : Description in UDT tag's documentation
	payloadFormat : string : Description in UDT tag's documentation
	includeDataType : bool : Description in UDT tag's documentation
	timestampFormat : string : Description in UDT tag's documentation
	qualityFormat : string : Description in UDT tag's documentation
	
	Returns
	--------------
	Topic : string : 
	Payload : string : 
	Qos : int : 
	Retain : int : Cirrus Link publish methods expects integer
	
	"""
	##########
	# Init
	##########
	Topic = tagPathFull
	Payload = None
	Qos = qos if qos in (0,1,2) else 0
	Retain = int(retain) if retain in (True,False) else 0
	
	##########
	# Tag Properties
	##########
	if readTagProps:
		tagPropsNameList = ["ExcludeFromPayload","QoS","Retain"]
		tagPropsFullPathList = []
		for tagProp in tagPropsNameList:
			tagPropsFullPathList.append("%s.%s" % (tagPathFull,tagProp))
		tagProps = system.tag.readBlocking(tagPropsFullPathList)

		# ExcludeFromPayload
		if tagProps[tagPropsNameList.index("ExcludeFromPayload")].value:
			raise DropReason("ExcludeFromPayload tag property")	
	
		# Qos
		qosReadIndex = tagPropsNameList.index("QoS")
		if tagProps[qosReadIndex].quality.good and tagProps[qosReadIndex].value in (0.0,1.0,2.0,0,1,2):
			Qos = int(tagProps[qosReadIndex].value)
		
		# Retain
		retainReadIndex = tagPropsNameList.index("Retain")
		if tagProps[retainReadIndex].quality.good and tagProps[retainReadIndex].value in (0.0,1.0,0,1,True,False):
			Retain = int(tagProps[retainReadIndex].value)
		
	##########
	# Drop message conditions
	##########
	if payloadFormat == "value" and tagQualifiedValue.quality.isNotGood():
		raise DropReason("Quality is not good and Payload Format is set to 'value'")
		
	if tagQualifiedValue.value is None and tagQualifiedValue.quality.good:
		raise DropReason("Value is none")
		
	if not isinstance(tagQualifiedValue.value,(bool,int,long,float,unicode)):
		raise DropReason("Not allowed data type: %s" % type(tagQualifiedValue.value))
		
		
	##########
	# Topic
	##########
	if rootPathsToCut:
		for rootPathToCut in rootPathsToCut:
			# if Topic starts with cutting string, cut and it and no need to search for more (break)
			if Topic.find(rootPathToCut) == 0:
				Topic = Topic.replace(rootPathToCut,"")
				break
	# always add prefix before topic
	Topic = str(topicPrefix) + Topic
	
	##########
	# Payload
	##########
	
	# timestamp
	if timestampFormat == "millis": # 1722327218694
		timestamp = system.date.toMillis(tagQualifiedValue.timestamp) 
	elif timestampFormat == "iso": # 2024-07-30T12:56:13.025Z
		timestamp = tagQualifiedValue.timestamp.toInstant().toString() 
	elif timestampFormat == "local": # 2024-07-30 14:56:13.025
		timestamp = system.date.format(tagQualifiedValue.timestamp,"yyyy-MM-dd HH:mm:ss.sss") 
	else:
		raise ConfigError("Invalid Timestamp Format: %s" % timestampFormat)
	
	# quality
	if qualityFormat == "code":
		quality = tagQualifiedValue.quality.getCode()
	elif qualityFormat == "text":
		quality = tagQualifiedValue.quality.toString()
	else:
		raise ConfigError("Invalid Quality Format: %s" % qualityFormat)
		
	# payload format
	if payloadFormat == "value":
		Payload = str(tagQualifiedValue.value)
	elif payloadFormat == "qualifiedValue":
		Payload = "%s,%s,%s" % (timestamp,quality,tagQualifiedValue.value)
	elif payloadFormat == "json":
		Payload = system.util.jsonEncode({
			"timestamp": timestamp,
			"quality": quality,
			"value": tagQualifiedValue.value
		})
	elif payloadFormat == "influx":
		# resolve value format according to Influx specs
		if type(tagQualifiedValue.value) in (int,long):
			valueInfluxString = "%ii" % tagQualifiedValue.value
		elif type(tagQualifiedValue.value) is unicode:
			valueInfluxString = "\"%s\"" % tagQualifiedValue.value
		else:
			valueInfluxString = str(tagQualifiedValue.value)
				
		Payload = "%s value=%s,quality=%ii %i" % (
			tagPathFull.replace(" ","_"),
			valueInfluxString,
			tagQualifiedValue.quality.getCode(),
			system.date.toMillis(tagQualifiedValue.timestamp) * 1000000
		)
	else:
		raise ConfigError("Invalid Payload Format: %s" % payloadFormat)
		
	return Topic, Payload, Qos, Retain

def publish(module, server, topic, payload, qos, retain, checkServerValidity=False):
	"""Function that will publish MQTT messages, using one of Cirrus Link modules (based on parameter module)
	
	Parameters
	--------------
	module : string : Which module to use to publish message
	server : string : Valid server connection name configured in Ignition Gateway under relevant module 
	topic : string : 
	payload : string : 
	qos : int : Enum:[0,1,2]
	retain : int : Enum:[0,1]

	Returns
	--------------
	None
	
	"""
	import java.lang.Exception as JException
	
	try:
		if qos not in (0,1,2):
			raise ValueError ("Invalid QoS: %s. Enum:[0,1,2]" % qos)
		if retain not in (0,1):
			raise ValueError ("Invalid Retain: %s. Enum:[0,1]" % retain)
			
		topic = str(topic)
		payload = str(payload)
			
		if module == "engine":
			system.cirruslink.engine.publish(server,topic,payload,qos,retain)
		elif module == "transmission":
			system.cirruslink.transmission.publish(server,topic,payload,qos,retain)
		else:
			raise ValueError("Config error: Not a valid Cirrus Link Module: %s , Enum:['engine','transmission']" % module)
			
	except JException as e:
		raise Exception(str(e))
	except ValueError as e:
		raise Exception(str(e))
			
def writeStatistics(udtInstancePath, count=1, errorMessage="", dropMessage=""):
	"""Function that will write result of previous operations to statistics tags of UDT instance
	
	Parameters
	--------------
	udtInstancePath : string : Full path to instance of MQTT Vanilla Transmission UDT
	count : int : default = 1
	errorMessage : string : default = ""
	dropMessage : string : default = ""
	
	Returns
	--------------
	None
	
	"""
	
	readTagNames = ["Event Count"]
	if errorMessage:
		readTagNames.append("Error Count")
	elif dropMessage:
		readTagNames.append("Drop Count")
	else:
		readTagNames.append("Sent Count")
	
	tagPaths = []
	statisticsPath = "%s/Statistics/Counters" % udtInstancePath 
	for tagName in readTagNames:
		tagPaths.append("%s/%s" % (statisticsPath,tagName))
	
	read = system.tag.readBlocking(tagPaths)
	
	addValues = [
		1, # Event Count is always 1
		count # Second is variable tag based on condition above
	]
	writeValues = []
	for i in range(len(readTagNames)):
		writeValues.append(read[i].value + addValues[i])
	
	if errorMessage:
		tagPaths += ["%s/Statistics/Error Message" % udtInstancePath]
		writeValues += [errorMessage]
	elif dropMessage:
		tagPaths += ["%s/Statistics/Drop Message" % udtInstancePath]
		writeValues += [dropMessage]
	
	system.tag.writeBlocking(tagPaths,writeValues)
	
def tagChangeEvent(initialChange, event, udtInstancePath):
	"""Trigger function that should be called from Gateway Tag Change event.
	
	
	Parameters
	--------------
	initialValue : Bool : Event parameter, that indicates first change (new tag, after restart,...)
	event : Object : Event parameter, that holds all required tag data (path, value, quality, timestamp,...)
	udtInstancePath : String : User input parameter, that indicates path to instance of UDT (MQTT Vanilla Transmission)
	
	Returns
	--------------
	None
	
	"""
	# Not initialChange to avoid execution after project save. Unfortunately, this also filters first change after gateway restart
	# https://forum.inductiveautomation.com/t/tag-change-script-initialchange-behaviour/33976
	if not initialChange and udtInstancePath:
		####################################################################
		# Prepare params
		####################################################################
		import traceback
		
		instance = system.tag.readBlocking(udtInstancePath)[0]
		if instance.quality.good and instance.value:
			config = instance.value["Config"]
			if config["General"]["Enabled"]:
				
				# read config tags
				module = config["General"]["Cirrus Link Module"]
				serverList = config["General"]["Server List"]
				readTagProps = config["General"]["Read Tag Properties"]
				qos = config["General"]["QoS"]
				retain = config["General"]["Retain"]
				rootPathsToCut = config["Topic"]["Cut From Tag Path"]
				topicPrefix = config["Topic"]["Prefix"]
				payloadFormat = config["Payload"]["Payload Format"] 
				timestampFormat = config["Payload"]["Timestamp Format"] 
				qualityFormat = config["Payload"]["Quality Format"] 
				loggerName = config["Logging"]["Gateway Logger Name"]
				logStatistics = config["Logging"]["Log Statistics"]
				
				# extract params from event object
				tagPathFull = event.tagPath.toStringFull()
				tagQualifiedValue = event.currentValue
				
				# initiate logger
				log = system.util.getLogger(loggerName)
				
				# define custom exceptions
				class ConfigError(Exception):
					pass
				class DropReason(Exception):
					pass
				class PublishError(Exception):
					pass
				
				####################################################################
				# Execution
				####################################################################
				try:
					if not serverList:
						raise ConfigError("No servers specified")
						
					topic,payload,qos,retain = resolvePublishParameters(
													tagPathFull, tagQualifiedValue,
													readTagProps, qos, retain, 
													rootPathsToCut, topicPrefix, 
													payloadFormat, timestampFormat, qualityFormat,
													ConfigError, DropReason)
						
					for server in serverList:
						try:
							publish(module, server, topic, payload, qos, retain)
							log.debug("Publish message: Module: %s, Server: %s, Topic: %s, Payload: %s, Qos: %s, Retain: %s" % (module, server, topic, payload, qos, retain))
						except Exception as e:
							raise PublishError(str(e))
						
						if logStatistics:
							writeStatistics(udtInstancePath)
						
				except ConfigError as e:
					if logStatistics:
						writeStatistics(udtInstancePath, errorMessage="Config Error: %s" % e)
				except DropReason as e:
					if logStatistics:
						writeStatistics(udtInstancePath, dropMessage="Drop Reason: %s" % e)
				except PublishError as e:
					if logStatistics:
						writeStatistics(udtInstancePath, errorMessage="Publish Error: %s" % e)
				except Exception as e:
					log.error("Unhandled exception: %s" % traceback.format_exc())
					if logStatistics:
						writeStatistics(udtInstancePath, errorMessage="Unhandled exception. Check gateway log for more info.")
	