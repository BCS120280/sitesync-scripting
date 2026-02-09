

def createInstance(tagPath, tagName):
	try:
		limitedModel = system.tag.readBlocking(["{0}/metaData/sparkplug/template".format(tagPath)])[0].value
		if limitedModel is None or str(limitedModel).strip() == "":
			system.perspective.print("WARNING: PI Integration skipped for {0} - no sparkplug template configured for this device model. "
				"Ensure the device profile has a sparkplug/template metadata tag set.".format(tagName))
			return None

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
		createResult = system.tag.configure(baseTagPath, [tag], collisionPolicy)

		system.tag.writeBlocking([tagPath + ".activated"], [True])

		results = addDevices.addTagToPi("{0}/{1}".format(baseTagPath, tagName), addDevices.componentID, addDevices.PIAddress)
		if isinstance(results, dict) and results.get("status") == "error":
			system.perspective.print("WARNING: PI Adapter data selection update failed for {0}: {1}".format(
				tagName, results.get("message", "Unknown error")))

		return createResult
	except Exception as e:
		system.perspective.print("Error creating PI instance for {0}: {1}".format(tagName, str(e)))
		return None
