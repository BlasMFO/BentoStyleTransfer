import os
import string
import random
import json
import requests
import functools
from datetime import datetime

from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

headers = {"content-type": "application/json"}
modelUri = "http://bento_app:5000/predict"
outputDir = "./static/temp"

# region functions
def generate_filename():
	"""Generates a random file name with a timestamp."""
	theString = datetime.now().strftime("%Y%m%d_%H%M%S_") + ''.join(random.choices(string.ascii_lowercase, k=5)) 
	return theString + '.jpg'

def make_jason(contentPath, stylePath, outputPath:str):
	"""Make the json for the request. Returns the json data."""
	data = json.dumps({
		'inputs': {
			'contentPath': contentPath.split("./static", maxsplit=1)[1],
			'stylePath': stylePath.split("./static", maxsplit=1)[1]
		},
		'outputPath' : outputPath.split("./static", maxsplit=1)[1]
	})
	return data

def get_result(jasonData:str):
	"""Get the result from the BentoML service."""
	response = requests.post(modelUri, headers=headers, json=jasonData)
	try:
		response = response.json()	# if all is ok, the response should be a boolean -> True
		return response
	except:
		return False
# endregion functions

# region routes
@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		uploaded_file1 = request.files['file1']
		uploaded_file2 = request.files['file2']
		if (uploaded_file1.filename != '') and (uploaded_file2.filename != '') and (uploaded_file1.filename[-3:] in ['jpg', 'png']) and (uploaded_file2.filename[-3:] in ['jpg', 'png']):
			contentPath = os.path.join(outputDir, generate_filename())
			stylePath = os.path.join(outputDir, generate_filename())
			outputPath = os.path.join(outputDir, generate_filename())
			uploaded_file1.save(contentPath)
			uploaded_file2.save(stylePath)
			jasonData = make_jason(
				contentPath=contentPath,
				stylePath=stylePath,
				outputPath=outputPath
			)
			response = get_result(jasonData=jasonData)
			if response:
				print("Response: True")
				result = {
					'contentPath': contentPath,
					'stylePath': stylePath,
					'outputPath': outputPath
				}
				return render_template('show.html', result=result)
	return render_template('index.html')


@app.route('/about')
def about():
	return render_template('about.html')
# endregion routes

# region main
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)
# endregion main