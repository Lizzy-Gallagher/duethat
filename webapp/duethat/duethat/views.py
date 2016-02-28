from duethat import app
from flask import render_template, request

import search
import json

from GoogleCalendar import GoogleCalendar
from GoogleTask import GoogleTask
from GoogleDoc import GoogleDoc

documents = GoogleDoc()
list_of_readable_files = documents.get_list_of_readable_files()

# homepage, landing page
@app.route('/')
def index():
	#documents = GoogleDoc()
	list_of_readable_files = documents.get_list_of_readable_files()

	filenames = []

	for file in list_of_readable_files:
		filenames.append(file['name'])

	return render_template('index2.html', filesnames=filenames)

# where you show the tasks and events gathere
@app.route('/duenote=<index>')
def duenote(index):
	target = list_of_readable_files[index]
	text = documents.get_text_from_file(target)

	textSnippets = search(text)

	return render_template('duenote.html', textSnippets=textSnippets)