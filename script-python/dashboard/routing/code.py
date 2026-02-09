def getTile(sensorType):
	if value in ("TEMPERATURE", "PRESSURE", "420ma", "FLOWMETER"):
		return "Dashboard/components/assets/Pressure"
	elif value == "VALVEPOSITION":
		return "Dashboard/components/assets/ValvePosition"
		
	elif value == "LEVEL":
		return "Dashboard/components/assets/Level"
	elif value == "THL":
		return "Dashboard/components/assets/THL"
		
	elif value == "HOTDROP":
		return "Dashboard/components/assets/Current"
		
	elif value == "VIBRATION":
		return "Dashboard/components/assets/Vibration"
		
	elif value == "LOCKOUT":
		return "Dashboard/components/assets/Lockout"
	
	else:
	
		return "Dashboard/components/assets/OtherPV"
		
		
		