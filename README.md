Blink1Weather
=============

This script uses the Open Weather Map API to update the color of a Blink-1. Use a cron job to keep the color updated to current conditons.

-------------

I didn't know what conditions were going to be passed by the API, so I have the script record all unknown contition types to a file.
After running for 2 weeks I had enough types to see that the conditions I was parsing matched the group names (in bold) on [this](http://openweathermap.org/weather-conditions) list.
I went ahead and prepopulated some of the conditions I hadn't parsed yet from that list, they are marked.
Unfortunatly, some of the stuff that should be under the atmosphere group show up as their own main condition.
Therefore I'm keeping the recording functionality to catch any other oddities like this.