import json


def getSettings():
	a =  system.piAdapter.getSettings("generic")	
	return json.loads(a)
	
def updateSettings(jsonObject):
	j = json.dumps(dict(jsonObject))
	res = system.piAdapter.updateSettings(j, "generic")
	r = json.loads(res)
	if utils.isSuccess(r):
		utils.showSuccess("Updated")
	else:
		utils.showError(utils.getResultMessage(r))