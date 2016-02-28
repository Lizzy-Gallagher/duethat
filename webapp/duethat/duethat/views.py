from duethat import app
from flask import render_template, request

import google_doc as gdoc

# homepage, landing page
@app.route('/')
def index():
	service = gdoc.get_service()
	list_of_readable_files = gdoc.list_files(service) # array of file dictionaries

	sample_file = list_of_readable_files[0]

	text = gdoc.get_text_from_file(sample_file, service)
	print (text)

	return render_template('index.html')

# page that shows docs
@app.route('/duethat')
def duethat():
	return render_template('duethat.html')

