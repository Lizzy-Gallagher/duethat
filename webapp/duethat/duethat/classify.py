"""
Makes a request call to the LUIS API and obtains JSON data 
about text.
@author Marisa Chow
"""

import requests

baseURL = "https://api.projectoxford.ai/luis/v1/application?id=a500a19e-f7ab-4078-9f6c-9b6b8ee3bbeb&subscription-key=598c92029bc24dff8b713c669d774773&q="

def classify(text):
	url = baseURL + text;
	response = requests.get(url);
	data = response.json()
	return data