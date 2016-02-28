from duethat import app
from flask import render_template, request

import google_doc as gdoc

# homepage, landing page
@app.route('/')
def index():
	#text = gdoc.main()
	return render_template('index.html')

# page that shows docs
@app.route('/duethat')
def duethat():
	return render_template('duethat.html')

