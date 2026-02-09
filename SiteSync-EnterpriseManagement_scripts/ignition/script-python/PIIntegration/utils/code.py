import json
import time
def showLoading(loadingID = "loading"):
	##shows the loading, defaultsID to loading if not specified
	system.perspective.openPopup(loadingID, "Popups/loading", showCloseIcon = False, modal=True )
	
def hideLoading(loadingID="loading"):
	##shows the loading, defaultsID to loading if not specified
	system.perspective.closePopup(loadingID)
	
def showError(errorText):
	system.perspective.print(errorText)
	try:
		system.perspective.openPopup("error", "Popups/error",  params = {"errorText":str(errorText)})
	except Exception as e:
		system.perspective.print(e)
	
def showSuccess(successText):
	system.perspective.openPopup("success", "Popups/success",  params = {"successText":successText})
	time.sleep(3)
	system.perspective.closePopup("success")
	
def isSuccess(resultMessage):
	if type(resultMessage) != dict:
		j = json.loads(resultMessage)
	else:
		j = resultMessage
	return j['status']
	
def getResultMessage(resultMessage):
	if type(resultMessage) != dict:
		j = json.loads(resultMessage)
	else:
		j = resultMessage
	return j['message']