

def createInstance(tagPath, tagName):
	system.perspective.print("Creating PI isntance {0}".format(tagPath))
	try:
		limitedModel = system.tag.readBlocking(["{0}/metaData/sparkplug/template".format(tagPath)])[0].value
		if limitedModel != None:
		
			assembledPath = tagPath.replace('[default]', '').replace(tagName, "")
			baseTagPath = "[default]PI Integration/{0}".format(assembledPath)
		  
		  
			# Properties that will be configured on that Tag.
			typeId = "SiteSyncModels/" + limitedModel
			tagType = "UdtInstance"
			# Parameters to pass in.
			sourceTagPath = tagPath
			  
			# Configure the Tag.
			tag = {
			            "name": tagName,         
			            "typeId" : typeId,
			            "tagType" : tagType,
			            "parameters" : {
			              "tagPath" :sourceTagPath
			              }
			       }
			 
			# Set the collision policy to Abort. That way if a tag already exists at the base path,
			# we will not override the Tag. If you are overwriting an existing Tag, then set this to "o".
			collisionPolicy = "a"
			  
			# Create the Tag.
			createReult = system.tag.configure(baseTagPath, [tag], collisionPolicy)
			system.perspective.print(createReult)
			
			system.tag.writeBlocking([tagPath + ".activated"], [True])
			
			results = addDevices.addTagToPi("{0}/{1}".format(baseTagPath, tagName), addDevices.componentID, addDevices.PIAddress)
			#system.perspective.print("PI API")
			system.perspective.print(results)
			return createReult
	except Exception as e:
		system.perspective.print("Error " + str(e))
		return None
		