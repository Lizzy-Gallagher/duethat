from duethat import app
from flask import render_template, request

import search
import json
from classify import classify
from parseJSON import parseJSON

from GoogleCalendar import GoogleCalendar
from GoogleTask import GoogleTask
from GoogleDoc import GoogleDoc

from dateutil import parser
from datetime import datetime

documents = GoogleDoc()
list_of_readable_files = documents.get_list_of_readable_files()

# homepage, landing page
@app.route('/')
def index():
	#documents = GoogleDoc()
	# list_of_readable_files = documents.get_list_of_readable_files()

	my_filenames = []

	# print ("Length: " + str(len(list_of_readable_files)) + "\n")
	for my_file in list_of_readable_files:
		# print my_file.items()
		my_filenames.append(my_file['name'])

	return render_template('index2.html', filenames=my_filenames)

# where you show the tasks and events gathere
@app.route('/duenote=<index>')
def duenote(index):
	target = list_of_readable_files[int(index)]
	text = documents.get_text_from_file(target)

	textSnippets = search.search(text)
	data = []
	for text in textSnippets:
		labels = classify(text)
		data.append(labels)

	scheduling, todo = parseJSON(data)

	google_calendar = GoogleCalendar()
	google_task = GoogleTask()

	for t in todo:
		print ("Sending task\n")
		google_task.add_task(t)
		t.due_date = datetime.strftime(parser.parse(t.due_date), '%m/%d/%y')

	for s in scheduling:
		print ("Sending cal\n")
		google_calendar.send_to_google_calendar(s)
		s.start_time = datetime.strftime(parser.parse(s.start_time), '%m/%d/%y')

	return render_template('duenote.html', scheduling=scheduling,todo=todo)
