from flask import render_template, flash, redirect,url_for, request,jsonify,json
from app import app
import pandas as pd
import plotly.graph_objects as go
import requests
import json
from datetime import datetime

# from app.forms import SubmitForm

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/statistics')
def statistics():
	#API source:
	#https://dev.to/pipedream/http-api-for-latest-wuhan-coronavirus-2019-ncov-data-20jj
	r = requests.get("https://coronavirus.m.pipedream.net/")
	data = r.json()
	for i in range(len(data['rawData'])):
		data['rawData'][i]['Province'] = data['rawData'][i]['Province/State']
		data['rawData'][i]['Country'] = data['rawData'][i]['Country/Region']
	return render_template("statistics.html", data = data, time =datetime.now().strftime("%Y/%m/%d"))

@app.route('/readings')
def readings():
	return render_template("readings.html")

codes = json.load(open("codes.json"))

@app.route('/dashboards')
def dashboards():
	r = requests.get("https://coronavirus.m.pipedream.net/")
	data = r.json()
	df = pd.json_normalize(data['rawData'])
	df[['Confirmed','Recovered','Recovered']] = df[['Confirmed','Recovered','Recovered']].astype('int64')
	df2 = df.groupby(['Country/Region'])[['Confirmed','Recovered','Recovered']].sum()
	df2 = df2.reset_index()
	
		
	df2['CODE'] = ""
	for x in df2['Country/Region']:
		if x in codes:
			df2.loc[df2['Country/Region'] == x,'CODE'] = codes[x]

	
	df2.loc[df2['Country/Region']=='Mainland China','CODE'] = 'CHN'
	df2.loc[df2['Country/Region']=='South Korea','CODE'] = 'KOR'
	df2.loc[df2['Country/Region']=='UK','CODE'] = 'GBR'
	df2.loc[df2['Country/Region']=='US','CODE'] = 'USA'
	fig = go.Figure(data=go.Choropleth(
	    locations = df2['CODE'],
	    z = df2['Confirmed'],
	    text = df2['Country/Region'],
	    colorscale = 'Reds',
	    autocolorscale=False,
	    reversescale=False,
	    marker_line_color='darkgray',
	    marker_line_width=0.5,
	#     colorbar_tickprefix = '$',
	#     colorbar_title = 'GDP<br>Billions US$',
	))
	fig.write_html(file='app/templates/heatmap.html')

	return render_template("dashboards.html")

@app.route('/social_media')
def social_media():
	posts = []
	try:
		r = requests.get("https://www.reddit.com/r/coronavirus/top.json?t=day")
		x = r.json()
		for entry in x:
			temp = {}
			print(entry)
			temp['time'] = datetime.fromtimestamp(entry['data']['created_utc']).strftime("%Y/%m/%d")
			temp['title'] = entry['data']['title']
			temp['score'] = entry['data']['score']
			temp['num_comments'] = entry['data']['num_comments']
			temp['permalink'] = entry['data']['permalink']
			posts += temp
	except:
		posts = []
	return render_template("social_media.html", data=posts)

@app.route('/forecast')
def forecast():
	return render_template("forecast.html")

@app.route('/news')
def news():
	return render_template("news.html")

@app.route('/sources')
def sources():
	return render_template("sources.html")

