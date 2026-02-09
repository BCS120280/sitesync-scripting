import json

def saveImage(imageBytes, devEUI):
	j = json.dumps({
	"devEUI":devEUI, 
	"image":imageBytes, 
	"tenantId":0
	
	})
	uploadSuccessful = system.sitesync.createImage(j)
	return json.loads(uploadSuccessful)
	
	
	
def getImageByDevEUI(devEUI):
	imageObject = system.sitesync.getImage(devEUI)
	if imageObject != None:
	
		image = json.loads(imageObject)
		if 'image' in image.keys():
			return image['image']
		else:
			return None
			
	else:
		return None
	