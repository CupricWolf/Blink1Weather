#!/usr/bin/env python3
import time
import urllib.request
import json
from subprocess import call

# This script is run every 15 minutes by a cron job.
# It changes the color of the Blink1 according to the weather returned by the open weather map api.
# At night the colors aren't as bright so that the tool isn't disruptive to sleep.

# Variables
localUnknownTypesFile = "/path/to/unknownTypes/file"
weatherApiUrl = "http://api.openweathermap.org/data/2.5/weather?id=0000&APPID=11111"

redSetting = 0
greenSetting = 0
blueSetting = 0

NIGHT_BRIGHTNESS_DIVISOR = 4 # Color settings are divided by this number at night

# Parses API call to python dict
webFile = str(urllib.request.urlopen(weatherApiUrl).read())[2:-3]
webFile = webFile.replace("[","").replace("]","") # Clean up the extra array around the weather object
jsonObject = json.loads(webFile)

condition = str(jsonObject["weather"]["main"])
print("Condition is: " + condition)

# Parse sun up and sun down times and function for if sun is up
sunRiseTime = jsonObject["sys"]["sunrise"]
sunSetTime = jsonObject["sys"]["sunset"]

def sunIsUp():
	currentTime = time.time()
	if (sunRiseTime <= currentTime) and (currentTime <= sunSetTime):
		return True
	else:
		return False

# I didn't know what conditions were going to be passed by the API, so I have the script record all unknown condition types to a file.
# After running for 2 weeks I had enough types to see that the conditions I was parsing matched the group names (in bold) on [this](http://openweathermap.org/weather-conditions) list.
# I went ahead and pre-populated some of the conditions I hadn't parsed yet from that list, they are marked.
# Unfortunately, some of the stuff that should be under the atmosphere group show up as their own main condition.
# Therefore I'm keeping the recording functionality to catch any other oddities like this.

if (condition == "Atmosphere") or (condition == "Fog") or (condition == "Haze") or (condition == "Mist"): # Haze and Mist should have shown up as Atmosphere, I don't know why they didnt't, Atmosphere is from the list.
	# Yellow
	redSetting = 255
	greenSetting = 255
	blueSetting = 0
elif (condition == "Clear"):
	# Green
	redSetting = 0
	greenSetting = 255
	blueSetting = 0
elif (condition == "Clouds"):
	# Yellow-ish Green Not very distinct from Green, but clouds and clear are close enough for me that I don't care.
	redSetting = 170
	greenSetting = 255
	blueSetting = 0
elif (condition == "Drizzle"): # From List
	# Cyan
	redSetting = 0
	greenSetting = 255
	blueSetting = 255	
elif (condition == "Extreme"): # From List
	# Red
	redSetting = 255
	greenSetting = 0
	blueSetting = 0
elif (condition == "Rain"): # From List
	# Blue
	redSetting = 0
	greenSetting = 0
	blueSetting = 255
elif (condition == "Snow"):
	# White
	redSetting = 255
	greenSetting = 255
	blueSetting = 255
elif (condition == "Thunderstorm"): # From list
	# Magenta
	redSetting = 255
	greenSetting = 0
	blueSetting = 255
else:
	# For adding unknown types to the unknown types file
	typeExistsInUnknownTypesFile = False
	unknownTypesFile = open(localUnknownTypesFile, "r")
	for line in unknownTypesFile:
		if (condition == line.replace("\n", "")):
			typeExistsInUnknownTypesFile = True
	unknownTypesFile.close()
	if (not typeExistsInUnknownTypesFile):
		unknownTypesFile = open(localUnknownTypesFile, "a")
		unknownTypesFile.write(condition + "\n")
		unknownTypesFile.close()

# If the sun isn't up I want the colors to be less bright
if not sunIsUp():
	redSetting = redSetting / NIGHT_BRIGHTNESS_DIVISOR
	greenSetting = greenSetting / NIGHT_BRIGHTNESS_DIVISOR
	blueSetting = blueSetting / NIGHT_BRIGHTNESS_DIVISOR

# Blink1-tool call, colors set above, defaults to off.
call(["sudo", "blink1-tool", "--rgb", str(redSetting) + "," + str(greenSetting) + "," + str(blueSetting)])
