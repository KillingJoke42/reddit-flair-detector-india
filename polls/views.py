#django respone libraries
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# All the HTML forms that django renders are called here
from polls.forms import getQuery, statsSettings

# Dependancies required from the source code
from polls.reddit_link import get_title
from polls.classify import classify, y_train
from polls.reddit_scraping import get_hot_data, get_new_data

# Joblib required to save/load ML model, json to return json requests.
import joblib
import json

# All background images that will be render at the back of the results page as per the prediction
image_classes = ["corona.jpeg", "food.jpeg", "india_flag.jpeg", "money.jpeg", "non-political.jpeg", "photography.jpeg", 
					"politics.jpeg", "scheduled.jpeg", "sci-tech.jpeg", "sports.jpeg", "caa.jpg"]

# Redirect "/" to 'home/'
def index(request):
	return redirect('home/')

# Home Page for Flairme. Gets form that accepts reddit link as input and sends with a POST to 'query/'
def home(request):
	if request.method == "POST":
		# get URL filled in by the user in the form to the results page
		form = getQuery(request.POST)
		# Check if the form is indeed valid
		if form.is_valid():
			# Redirect to 'query/' with POST request data
			return redirect("query/")
	else:
		# If we reach endpoint with a GET request, render only the form
		form = getQuery()

	return render(request, 'home.html', {'form':form})

# Display prediction made over the reddit URL
def query(request):
	#Make a copy of the data received from the POST request
	data = request.POST.copy()
	# extract the URL from the data received
	url = data.get("url")

	# load the classifier and the label mapping
	classifier = joblib.load("models/native_baye.sav")
	keys = list(y_train.keys())
	values = list(y_train.values())

	# get prediction of flair from the ML model
	prediction = keys[values.index(classify(classifier, get_title(url))[0])]

	# Background image of the results page is rendered based on the prediction made
	if prediction == "Politics":
		image_bg = image_classes[6]
	elif prediction == "Non-Political":
		image_bg = image_classes[4]
	elif prediction == "AskIndia":
		image_bg = image_classes[2]
	elif prediction == "Policy/Economy":
		image_bg = image_classes[3]
	elif prediction == "Business/Finance":
		image_bg = image_classes[3]
	elif prediction == "Science/Technology":
		image_bg = image_classes[8]
	elif prediction == "Scheduled":
		image_bg = image_classes[7]
	elif prediction == "Food":
		image_bg = image_classes[1]
	elif prediction == "Photography":
		image_bg = image_classes[5]
	elif prediction == "Coronavirus":
		image_bg = image_classes[0]
	elif prediction == "Sports":
		image_bg = image_classes[9]
	elif prediction == "CAA-NRC-NPR":
		image_bg == image_classes[10]
	else:
		image_bg = image_classes[2]

	# render results page from template
	return render(request, "prediction.html", {'prediction':prediction, 'image_bg':image_bg})

def statistics(request):
	# Statistics Page displays the current trends on the r/India subreddit
	if request.method == "POST":
		# Get the number of posts and the sorting type from the user-
		form = statsSettings(request.POST)
		if form.is_valid():
			# Redirect to the display page with the results
			return redirect("statdisp/")
	else:
		# If we reach the page with a GET request, render only the form
		form = statsSettings()

	# render the statistics template as placeholder for the form
	return render(request, 'statistics.html', {'form':form})

# Display the generated data about the r/India subreddit
def stats_disp(request):
	data = request.POST.copy()
	# Get the posts limit and the sorting type
	limit = data.get("limit")
	choice = data.get("sort_type")

	# Scrape the data as per the choices
	# Data Collected:
	# 1) Number of Posts per Flair
	# 2) Most Popular Flair
	# 3) Least Popular Flair
	if choice == '1':
		sort = "Hot"
		graph = "hot_graph.png"
		get_dict = get_hot_data(int(limit))
		values = list(get_dict.values())
		keys = list(get_dict.keys())
		top = keys[values.index(max(values))]
		bottom = keys[values.index(min(values))]
	elif choice == '2':
		sort = "New"
		graph = "new_graph.png"
		get_dict = get_new_data(int(limit))
		values = list(get_dict.values())
		keys = list(get_dict.keys())
		top = keys[values.index(max(values))]
		bottom = keys[values.index(min(values))]

	# Render template with received data
	return render(request, "statsdisp.html", {'limit':limit, 'sort':sort, 'top':top, 'bottom':bottom, 'graph':graph})

# Need to prevent check of csrf so as to enable automatic post requests to the endpoint
@csrf_exempt
def automate(request):
	# Sniffing for post request to endpoint
	if request.method == "POST":
		data = request.FILES.copy()
		# Get file pointer
		file = data["upload_file"]

		# Load the ML model and label mapping
		classifier = joblib.load("models/native_baye.sav")
		keys = list(y_train.keys())
		values = list(y_train.values())

		# Ready the json response and send it across after loading generated predictions
		json_response = dict()
		for link in file:
			prediction = keys[values.index(classify(classifier, get_title(link.decode('ascii').rstrip('\n')))[0])]
			json_response[link.decode('ascii').rstrip('\n')] = prediction
		return JsonResponse(json_response)

	else:
		# If endpoint reached with a GET request, inform user of Invalid Usage
		return HttpResponse("Send POST request automatically to get JSON of predictions")
