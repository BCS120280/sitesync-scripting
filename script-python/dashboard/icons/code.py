def getIcon(sensorType):
	if sensorType == "TEMPERATURE":
		return "material/whatshot"
	elif sensorType == "LOCKOUT":
		return "material/lock_open"
	elif sensorType == "VIBRATION":
		return "material/vibration"
	elif sensorType == "VALVEPOSITION":
		return ""
	elif sensorType == "PRESSURE":
		return ""
	elif sensorType == "THL":
		return ""
	else:
		return ""