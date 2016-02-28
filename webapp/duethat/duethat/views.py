from duethat import app
from flask import render_template, request

import search
import json
from classify import classify
from parseJSON import parseJSON

from GoogleCalendar import GoogleCalendar
from GoogleTask import GoogleTask
from GoogleDoc import GoogleDoc

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

	scheduling,todo = parseJSON(data)

	return render_template('duenote.html', scheduling=scheduling,todo=todo)
