from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from polls.forms import getQuery, statsSettings

from polls.reddit_link import get_title
from polls.classify import classify, y_train
from polls.reddit_scraping import get_hot_data, get_new_data

import joblib
import json

image_classes = ["corona.jpeg", "food.jpeg", "india_flag.jpeg", "money.jpeg", "non-political.jpeg", "photography.jpeg", 
					"politics.jpeg", "scheduled.jpeg", "sci-tech.jpeg", "sports.jpeg", "caa.jpg"]

def index(request):
	return redirect("home/")

def home(request):
	if request.method == "POST":
		form = getQuery(request.POST)
		if form.is_valid():
			return redirect("query/")
	else:
		form = getQuery()

	return render(request, 'home.html', {'form':form})

def query(request):
	data = request.POST.copy()
	url = data.get("url")
	classifier = joblib.load("models/native_baye.sav")
	keys = list(y_train.keys())
	values = list(y_train.values())
	prediction = keys[values.index(classify(classifier, get_title(url))[0])]
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
	return render(request, "prediction.html", {'prediction':prediction, 'image_bg':image_bg})

def statistics(request):
	if request.method == "POST":
		form = statsSettings(request.POST)
		if form.is_valid():
			return redirect("statdisp/")
	else:
		form = statsSettings()

	return render(request, 'statistics.html', {'form':form})

def stats_disp(request):
	data = request.POST.copy()
	limit = data.get("limit")
	choice = data.get("sort_type")
	if choice == '1':
		sort = "Hot"
		graph = "hot_graph.png"
		get_dict = get_hot_data(int(limit))
	elif choice == '2':
		sort = "New"
		graph = "new_graph.png"
		get_dict = get_new_data(int(limit))
		values = list(get_dict.values())
		keys = list(get_dict.keys())
		top = keys[values.index(max(values))]
		bottom = keys[values.index(min(values))]

	return render(request, "statsdisp.html", {'limit':limit, 'sort':sort, 'top':top, 'bottom':bottom, 'graph':graph})

@csrf_exempt
def automate(request):
	if request.method == "POST":
		data = request.FILES.copy()
		file = data["upload_file"]
		classifier = joblib.load("models/native_baye.sav")
		keys = list(y_train.keys())
		values = list(y_train.values())
		json_response = dict()
		for link in file:
			prediction = keys[values.index(classify(classifier, get_title(link.decode('ascii').rstrip('\n')))[0])]
			json_response[link.decode('ascii').rstrip('\n')] = prediction
		return JsonResponse(json_response)
	else:
		return HttpResponse("Send POST request automatically to get JSON of predictions")
