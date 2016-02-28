"""
parseJSON.py parses the LUIS AI JSON response.
"""

from CalItem import CalItem
from TaskItem import TaskItem
import json
import datetime


def parseJSON(json):
	scheduling = []
	todo = []
	for j in json:
		print (j.items())

		query = j["query"]
		intent = j["intents"][0]["intent"]
		action = ""
		actionTarget = ""
		location = ""
		startTime = ""
		for ent in j["entities"]:
			enttype = ent["type"]
			if enttype == "Action":
				action = ent["entity"]
			elif enttype == "ActionTarget":
				actionTarget = ent["entity"]
			elif enttype == "Place":
				location = ent["entity"]
			else:
				# not all entities have date
				if 'date' in ent["resolution"].keys():
					startTime = ent["resolution"]["date"].replace('XXXX', '2016')

		if intent == "Schedule":
			scheduling.append(CalItem(query, action,actionTarget,location,startTime))
		else:
			todo.append(TaskItem(query, action,actionTarget,location,startTime))

	return (scheduling,todo)
