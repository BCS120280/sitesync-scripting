def createLimitedInstance(intendedTagPath, limitedTemplate, newTagName, sourceTagPath):
		
	typeId = "SiteSyncModels/"  + limitedTemplate
	tagType = "UdtInstance"
	  
	# Configure the Tag.
	tag = {
	            "name": newTagName,         
	            "typeId" : typeId,
	            "tagType" : tagType,
	            "parameters" : {
	              "tagPath" : sourceTagPath
	              }
	       }
	# Set the collision policy to Abort. That way if a tag already exists at the base path,
	# we will not override the Tag. If you are overwriting an existing Tag, then set this to "o".
	collisionPolicy = "a"
	  
	# Create the Tag.
	system.tag.configure(baseTagPath, [tag], collisionPolicy)
	
def refreshSparkplugTransmission():
	import time
	time.sleep(2)
	##trigger birth of undiscovered tags
	system.tag.write("[MQTT Transmission]Transmission Control/Refresh", True)