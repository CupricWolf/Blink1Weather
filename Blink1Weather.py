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
url = "http://api.openweathermap.org/data/2.5/weather?q=CityName"
red = 0
green = 0
blue = 0
nightBrightnessFactor = 4 # Output is divided by this number at night

# Parses API call to python dict
webFile = str(urllib.request.urlopen(url).read())[2:-3]
jsonDict = json.loads(webFile)

# Parses a piece of the the API call dict into its own dict
weatherDict = json.loads(str(jsonDict["weather"][0]).replace("\'","\""))
condition = str(weatherDict["main"])

# Parse sun up and sun down times and function for if sun is up
sunRiseTime = jsonDict["sys"]["sunrise"]
sunSetTime = jsonDict["sys"]["sunset"]
def sunIsUp():
	currentTime = time.time()
	if (sunRiseTime <= currentTime) and (currentTime <= sunSetTime):
		return True
	else:
		return False

# I didn't know what conditions were going to be passed by the API, so I have the script record all unknown contition types to a file.
# After running for 2 weeks I had enough types to see that the conditions I was parsing matched the group names (in bold) on [this](http://openweathermap.org/weather-conditions) list.
# I went ahead and prepopulated some of the conditions I hadn't parsed yet from that list, they are marked.
# Unfortunatly, some of the stuff that should be under the atmosphere group show up as their own main condition.
# Therefore I'm keeping the recording functionality to catch any other oddities like this.

if (condition == "Atmosphere") or (condition == "Fog") or (condition == "Haze") or (condition == "Mist"): # Haze and Mist should have shown up as Atmosphere, I don't know why they didnt't, Atmosphere is from the list.
	# Yellow
	red = 255
	green = 255
	blue = 0
elif (condition == "Clear"):
	# Green
	red = 0
	green = 255
	blue = 0
elif (condition == "Clouds"):
	# Yellow-ish Green Not very distinct from green, but clouds and clear are close enough for me that I don't care.
	red = 170
	green = 255
	blue = 0
elif (condition == "Drizzle"): # From List
	# Cyan
	red = 0
	green = 255
	blue = 255	
elif (condition == "Extreme"): # From List
	# Red
	red = 255
	green = 0
	blue = 0
elif (condition == "Rain"): # From List
	# Blue
	red = 0
	green = 0
	blue = 255
elif (condition == "Snow"):
	# White
	red = 255
	green = 255
	blue = 255
elif (condition == "Thunderstorm"): # From list
	# Magenta
	red = 255
	green = 0
	blue = 255
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
	red = red / nightBrightnessFactor
	green = green / nightBrightnessFactor
	blue = blue / nightBrightnessFactor

# Blink1-tool call, colors set above, defaults to off.
call(["sudo", "blink1-tool", "--rgb", str(red) + "," + str(green) + "," + str(blue)])
