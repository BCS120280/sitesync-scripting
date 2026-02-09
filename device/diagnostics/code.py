def getTagPaths(dataset):
	#accepts array of dictionaries, gets the fullPath variable
	
	tagPaths = []
	for device in dataset:
		tagPaths.append(device['fullTagPath'])
	return tagPaths
	
	
def getValues(tagPaths):
	paths = []
	for t in tagPaths:
		paths.append(t + "/metaData/diagnostics/code")
		
	values = system.tag.readBlocking(paths)
	return values
	
	
def getStatusCalculations(values):
	statuses = {
	"NotActivated":0, 
	"Operational":0, 
	"TimedOut":0, 
	"DecodeError":0
	}
	for v in values:
		if v.value == -1:
			statuses['NotActivated'] += 1
		elif v.value == 0:
			statuses['Operational']  += 1
		
		elif v.value == 3:
			
			statuses['TimedOut']  += 1
		elif v.value == 4:
			statuses['DecodeError'] += 1
		
	return statuses
	
	
def getStatusPaths(tagPaths, values):
	statuses = {
	-1:[], 
	0:[], 
	3:[], 
	4:[]
	}
	o = 0
	for v in values:
		if v.value == -1:
			statuses[-1].append(tagPaths[o].split('/metaData')[0])
		elif v.value == 0:
			statuses[0].append(tagPaths[o].split('/metaData')[0])
		
		elif v.value == 3:
			
			statuses[3].append(tagPaths[o].split('/metaData')[0])
		elif v.value == 4:
			statuses[4].append(tagPaths[o].split('/metaData')[0])
		o += 1
		
	return statuses