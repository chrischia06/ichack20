from flask import render_template, flash, redirect,url_for, request,jsonify,json
from app import app


import requests

# from app.forms import SubmitForm
@app.route('/')
def index():
	r = requests.get("https://coronavirus.m.pipedream.net/")
	data = r.json()
	for i in range(len(data['rawData'])):
		data['rawData'][i]['Province'] = data['rawData'][i]['Province/State']
		data['rawData'][i]['Country'] = data['rawData'][i]['Country/Region']

	return render_template("index.html", data = data)

