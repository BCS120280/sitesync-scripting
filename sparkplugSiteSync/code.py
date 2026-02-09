def triggerBirth(tagPath):
	## when message comes in, refresh node to trigger birth, and then data 
	#[MQTT Transmission]Transmission Info/Transmitters/siteSyncTest/Edge Nodes/SiteSync/three/Refresh Edge Node
	#transmitterName
	res = ""	
	filterPath = cleanPathForFilter(sourcePath)  
	print filterPath
	# Call the function. Replace the filter with your own search criteria.
	res = browseTags('[MQTT Transmission]Transmission Info/Transmitters', {'name':filterPath})
	print str(res[0])
	import time
	if res != "":
		resetPath = str(res[0]) + "/Refresh Edge Node"
		system.tag.write(resetPath, True)
		## snooze to allow reset
		time.sleep(15)
		##write birthed message to stop this from retriggering, and to publish DData
		##Assuming in LORAMETRICS directory
		resetPath = cleanPathForAlarming(sourcePath)
		print resetPath
		system.tag.write(resetPath, True)
		print "wrote to path"
	
	
	

def cleanPathForFilter(path):

	
	newPath = path.split(']')[1].split("/LoRaMetrics")[0]
	return newPath
	
def cleanPathForAlarming(path):
	newPath = path.split('LoRaMetrics')[0]
	#[default]three/Device 5/LoRaMetrics/sparkplugBirthed
	#[default]three/Device 5/LoRaMetrics/sparkplugBirth
	newPath = newPath + "/LoRaMetrics/sparkplugBirthed"
	return newPath
	

    

def browseTags(path, filter):
    # List to store the matching tag paths
    matching_tags = []

    # First, browse for anything that can have children (Folders and UDTs, generally)
    results = system.tag.browse(path)
    for branch in results.getResults():
        if branch['hasChildren']:
            # If something has a child node, then call this function again so we can search deeper.
            # Include the filter, so newer instances of this call will have the same filter.
            matching_tags.extend(browseTags(branch['fullPath'], filter))

    # Call this function again at the current path, but apply the filter.
    results = system.tag.browse(path, filter)

    for result in results.getResults():
        # Append the matching tag path to the list.
        matching_tags.append(result['fullPath'])

    # Return the list of matching tag paths.
    return matching_tags

