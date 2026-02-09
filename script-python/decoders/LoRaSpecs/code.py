import json
def getRegions():
	regionList = json.loads(system.sitesync.getRegions())
	dropdownOptions = []
	for r in regionList:
		dropdownOptions.append(utils.dropdowns.formatDropdownOption(r, r))
	return dropdownOptions
	
	
def getLoRaVersions():
	regionList = json.loads(system.sitesync.getLoRaVersions())
	dropdownOptions = []
	for r in regionList["LoRAversion"]:
		dropdownOptions.append(utils.dropdowns.formatDropdownOption(r["name"], r["TTNParam"]))
	return dropdownOptions
	
	
def getLoRaRevisions(region, version):
	regionList = json.loads(system.sitesync.getLoRaRevisions(region, version))
	dropdownOptions = []
	for r in regionList['LoRAversion']:
		dropdownOptions.append(utils.dropdowns.formatDropdownOption(r['name'], r['value']))
	return dropdownOptions
	
def getLoRaClass():
	classes = json.loads(system.sitesync.getClasses())
	dropdownOptions = []
	for r in classes['deviceClasses']:
		dropdownOptions.append(utils.dropdowns.formatDropdownOption(r, r))
	return dropdownOptions