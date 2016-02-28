from duethat import app
from flask import render_template, request

from GoogleCalendar import GoogleCalendar
from GoogleTask import GoogleTask
from GoogleDoc import GoogleDoc
import cal

# homepage, landing page
@app.route('/')
def index():
	documents = GoogleDoc()
	list_of_readable_files = documents.get_list_of_readable_files()

	filenames = []

	for file in list_of_readable_files:
		filenames.append(file['name'])

	return render_template('index.html')

# page that shows docs
@app.route('/duethat')
def duethat():
	return render_template('duethat.html')

