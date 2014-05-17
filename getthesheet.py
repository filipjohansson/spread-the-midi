import urllib2
import json
req = urllib2.urlopen("https://spreadsheets.google.com/feeds/cells/1poWnTI6BpJtYMmcGtOE33Kqes6yzQmw46jJwXttsPu0/od6/public/values?alt=json")
data = json.load(req)

def getNotesOnColumn(col):
	for j in data["feed"]["entry"]:
		if(j["gs$cell"]["col"] == str(col)):
			print j["gs$cell"]["$t"]

getNotesOnColumn(1)