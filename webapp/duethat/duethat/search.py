"""
search.py will search a text for to-do items and 
schedule terms, as denoted by **. 
@author Marisa Chow
"""

import re

def search(text):
	targetText = []
	indices = [m.start() for m in re.finditer('\*\*', text)]
	if len(indices) % 2 != 0:
		# uneven indices
		# ignore last one? :/ 
		indices = indices[:len(indices)-1]
	for x in range(0,len(indices), 2):
		start = indices[x]+2
		end = indices[x+1]
		substr = text[start:end].strip()
		targetText.append(substr)
	return targetText
