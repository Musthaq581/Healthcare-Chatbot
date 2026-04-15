from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db import connection

from googleplaces import GooglePlaces
import requests
import folium
import pandas as pd
from django.db.models import Min
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import re
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from geopy.geocoders import GoogleV3
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from keras.models import load_model
from time import sleep
from tensorflow.keras.utils import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import webbrowser as wb
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
import tkinter
from tkinter import *
from django.http import JsonResponse
from .gui import *
from django.views import View

import tensorflow as tf
from nltk.stem import WordNetLemmatizer
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import Adam
import subprocess
import os

# import nltk 



# Get the directory where this app is located
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# nltk_Data = os.path.join(APP_DIR, "nltk_data")
# nltk.data.path.append(nltk_Data)
# nltk.download("punkt",download_dir= 'nltk_data')

# Define dynamic paths for all files
INTENTS_PATH = os.path.join(APP_DIR, 'intents.json')
WORDS_PATH = os.path.join(APP_DIR, 'words.pkl')
CLASSES_PATH = os.path.join(APP_DIR, 'classes.pkl')
MODEL_PATH = os.path.join(APP_DIR, 'chatbot_model.h5')
MAIN_PATH = os.path.join(APP_DIR, 'main.py')

# Create your views here.
def Example(request):
	user_details_count = userDetails.objects.count()
	question_answer_count = Question_Answer.objects.count()
	return render(request,"Example.html",{'user_details_count':user_details_count,'question_answer_count':question_answer_count})


def Home(request):
	user_details_count = userDetails.objects.count()
	question_answer_count = Question_Answer.objects.count()
	return render(request,"Home.html",{'user_details_count':user_details_count,'question_answer_count':question_answer_count})

def Admin_Login(request):
	if request.method == "POST":
		A_username = request.POST['aname']
		A_password = request.POST['apass']
		if AdminDetails.objects.filter(username = A_username,password = A_password).exists():
			ad = AdminDetails.objects.get(username=A_username, password=A_password)
			print('d')
			messages.info(request,'Admin login is Sucessfull')
			request.session['type_id'] = 'Admin'
			request.session['UserType'] = 'Admin'
			request.session['login'] = "Yes"
			return redirect("/")
		else:
			print('y')
			messages.error(request, 'Error wrong username/password')
			return render(request, "Admin_Login.html", {})
	else:
		return render(request, "Admin_Login.html", {})

def User_Login(request):
	if request.method == "POST":
		C_name = request.POST['aname']
		C_password = request.POST['apass']
		if userDetails.objects.filter(Username=C_name,Password=C_password).exists():
			users = userDetails.objects.all().filter(Username=C_name,Password=C_password)
			messages.info(request,C_name +' logged in')
			request.session['UserId'] = users[0].id
			request.session['type_id'] = 'User'
			request.session['UserType'] = C_name
			request.session['login'] = "Yes"
			return redirect('/')
		else:
			messages.info(request, 'Please Register')
			return redirect("/User_Registeration")
	else:
		return render(request,'User_Login.html',{})

def User_Registeration(request):
	if request.method == "POST":
		Name= request.POST['name']
		Age= request.POST['age']
		Phone= request.POST['phone']
		Email= request.POST['email']
		Address= request.POST['address']
		Username= request.POST['Username']
		Password= request.POST['Password']
		if userDetails.objects.all().filter(Username=Username).exists():
			messages.info(request,"Username Taken")
			return redirect('/User_Registeration')
		else:
			obj = userDetails(
			Name=Name
			,Age=Age
			,Phone=Phone
			,Email=Email
			,Address=Address
			,Username=Username
			,Password=Password)
			obj.save()
			messages.info(request,Name+" Registered")
			return redirect('/User_Login')
	else:
		return render(request,"User_Registeration.html",{})

def Change_Password(request):
	if request.method == "POST":
		Userid = request.session['UserId']
		newpass = request.POST['newpass']
		cpass = request.POST['cpass']
		if newpass != cpass:
			messages.info(request,"Passwords dont match")
			return redirect('/Change_Password/')
		else:
			userDetails.objects.filter(id=Userid).update(Password=newpass)
			messages.info(request,"Password Changed")
			return redirect('/Change_Password/')
	else:
		Userid = request.session['UserId']
		details = userDetails.objects.filter(id=Userid)
		return render(request,"Change_Password.html",{'details':details})


def View_Users(request):
    details = userDetails.objects.all()
    return render(request,"view_user.html",{'details':details})


def Manage_Question(request):
	details = Question_Answer.objects.all()
	return render(request,"Manage_Question.html",{'details':details})

# def Add_Question(request):
# 	if request.method == "POST":
# 		question= request.POST['question']
# 		answer= request.POST['answer']
# 		keywords= request.POST['keywords']
# 		obj = Question_Answer(Question=question,Answer=answer,Keywords=keywords)
# 		obj.save()
		
# 		messages.info(request,"Question Added")
# 		return redirect('/Manage_Question/')
# 	else:
# 		return render(request,"Add_Question.html",{})


# -----------------------------------------------------------------------

# def Add_Question(request):
#     if request.method == 'POST':
#         tag = request.POST.get("tag")
#         questions = request.POST.get("question", "").split(",")  # Split questions at commas
#         answer = request.POST.get("answer", "")
#         keywords = request.POST.get("keywords", "").split(",")

#         # Check if an intent with the same tag exists in the database
#         existing_intent = Question_Answer.objects.filter(Tag=tag).first()

#         if existing_intent:
#             # Update the existing intent in the database
#             existing_intent.Question = existing_intent.Question + f", {', '.join(questions)}"
#             existing_intent.Answer = existing_intent.Answer + f", {answer}"

#             # Convert the existing keywords to a list and concatenate the new keywords
#             existing_keywords = existing_intent.Keywords.split(",")
#             existing_keywords.extend(keywords)
#             existing_intent.Keywords = ",".join(existing_keywords)

#             existing_intent.save()
#         else:
#             # Create a new intent in the database if it doesn't exist
#             obj = Question_Answer(Question=", ".join(questions), Answer=answer, Keywords=",".join(keywords), Tag=tag)
#             obj.save()

#         # Initialize an empty list to store the intents
#         intents = []

#         # Load existing intents from a JSON file if it exists
#         try:
#             with open("C:/Python Projects/AI_HealthCareBot_Website/Health_App/intents.json", "r") as file:
#                 data = json.load(file)
#                 intents = data.get("intents", [])
#         except FileNotFoundError:
#             pass

#         # Check if an intent with the same tag exists in the JSON file
#         existing_json_intent = next((intent for intent in intents if intent["tag"] == tag), None)

#         if existing_json_intent:
#             # Update the existing intent in the JSON file
#             existing_json_intent["patterns"].extend(questions + [keyword.strip() for keyword in keywords])
#             existing_json_intent["responses"].append(answer)
#         else:
#             # Create a new intent in the JSON file if it doesn't exist
#             intent = {
#                 "tag": tag,
#                 "patterns": questions + [keyword.strip() for keyword in keywords],
#                 "responses": [answer],
#             }
#             intents.append(intent)

#         # Save the updated intents to a JSON file
#         data = {"intents": intents}

#         with open("C:/Python Projects/AI_HealthCareBot_Website/Health_App/intents.json", "w") as file:
#             json.dump(data, file, indent=4)

#         return redirect('Manage_Question')

#     else:
#         return render(request, "Add_Question.html", {})



def Add_Question(request):
    if request.method == 'POST':
        tag = request.POST.get("tag")
        questions = [q.strip() for q in request.POST.get("question", "").split(",")]  # Split questions at commas
        answer = request.POST.get("answer", "").strip()  # Remove leading/trailing whitespace from answer
        keywords = [kw.strip() for kw in request.POST.get("keywords", "").split(",")]  # Remove leading/trailing whitespace from keywords

        # Check if an intent with the same tag exists in the database
        existing_intent = Question_Answer.objects.filter(Tag=tag).first()

        if existing_intent:
            # Update the existing intent in the database
            existing_intent.Question = existing_intent.Question + ", ".join(questions)
            existing_intent.Answer = existing_intent.Answer + ", " + answer

            # Convert the existing keywords to a list and concatenate the new keywords
            existing_keywords = existing_intent.Keywords.split(",")
            existing_keywords.extend(keywords)
            existing_intent.Keywords = ",".join(existing_keywords)

            existing_intent.save()
        else:
            # Create a new intent in the database if it doesn't exist
            obj = Question_Answer(Question=", ".join(questions), Answer=answer, Keywords=",".join(keywords), Tag=tag)
            obj.save()

        # Initialize an empty list to store the intents
        intents = []

        # Load existing intents from a JSON file if it exists
        try:
            with open(INTENTS_PATH, "r") as file:
                data = json.load(file)
                intents = data.get("intents", [])
        except FileNotFoundError:
            pass

        # Check if an intent with the same tag exists in the JSON file
        existing_json_intent = next((intent for intent in intents if intent["tag"] == tag), None)

        if existing_json_intent:
            # Update the existing intent in the JSON file
            existing_json_intent["patterns"].extend(questions + keywords)
            existing_json_intent["responses"].extend([resp.strip() for resp in answer.split(",")])  # Split response at commas
        else:
            # Create a new intent in the JSON file if it doesn't exist
            intent = {
                "tag": tag,
                "patterns": questions + keywords,
                "responses": [resp.strip() for resp in answer.split(",")],  # Split response at commas
            }
            intents.append(intent)

        # Save the updated intents to a JSON file
        data = {"intents": intents}

        with open(INTENTS_PATH, "w") as file:
            json.dump(data, file, indent=4)

        return redirect('Manage_Question')

    else:
        return render(request, "Add_Question.html", {})
# -----------------------------------------------------------------------


def Update_Question(request):
    if request.method == "POST":
        print(request.POST)  # Debug statement to print POST data to the console
        q_id = request.POST.get('viewid')
        question = request.POST.get('question')
        answer = request.POST.get('answer')  # Match the name attribute in your form
        keywords = request.POST.get('keywords')
        Question_Answer.objects.filter(id=q_id).update(Question=question, Answer=answer, Keywords=keywords)
        messages.info(request, "Information Updated")
    return redirect('/Manage_Question/')





# def Delete_Question(request,id):
# 	Question_Answer.objects.filter(id=id).delete()
# 	return redirect('Manage_Question')


def Delete_Question(request, id):
    # First, retrieve the intent to be deleted from the database
    intent_to_delete = Question_Answer.objects.filter(id=id).first()

    if intent_to_delete:
        # Get the tag of the intent
        tag_to_delete = intent_to_delete.Tag

        # Delete the intent from the database
        intent_to_delete.delete()

        # Load existing intents from the JSON file
        intents = []

        try:
            with open(INTENTS_PATH, "r") as file:
                data = json.load(file)
                intents = data.get("intents", [])
        except FileNotFoundError:
            pass

        # Remove the intent with the matching tag from the JSON file
        intents = [intent for intent in intents if intent["tag"] != tag_to_delete]

        # Save the updated intents back to the JSON file
        data = {"intents": intents}

        with open(INTENTS_PATH, "w") as file:
            json.dump(data, file, indent=4)

        return redirect('Manage_Question')



def U_NearbyHospitals(request):
	if request.method == "POST":
		userId = request.session['UserId']
		# userloc = UserDetails.objects.all().filter(id = userId)
		lat = request.POST['text1']
		print(lat)
		lang = request.POST['text2']
		print(lang)
		userDetails.objects.filter(id = userId).update(Lat=lat,Lng=lang)
		
		API_KEY = 'AIzaSyAkbDwHDm9JtbjLfiiqFFUbmaquU9K6DPQ'
		print(API_KEY)
		google_places = GooglePlaces(API_KEY)
		print('a')
		query_result = google_places.nearby_search(
			lat_lng ={'lat': lat, 'lng': lang},
			radius = 5000, types=['hospital'])
		if query_result.has_attributions:
			print (query_result.html_attributions)
		for place in query_result.places:
			print(place.get_details())
			h_name = place.name
			REPLACE_APS = re.compile(r"[\']")
			h_name = REPLACE_APS .sub("", h_name)
			
			print (h_name)
			h_lat = place.geo_location['lat']
			h_lon = place.geo_location['lng']
			print("Latitude",h_lat)
			print("Longitude",h_lon)
			print()
		

			data = NearbyHospitals(hospitalname=h_name,Lat=h_lat,Lng=h_lon)
			data.save()
			print(data)
		return redirect('/maps') 
	else:
		return render(request,'U_NearbyHospitals.html',{})

def maps(request):
	userId = request.session['UserId']
	user = userDetails.objects.all().filter(id = userId)
	print(user)
	#StoreData = NearbyHospitals.objects.all()
	#print(StoreData)
	StoreData = NearbyHospitals.objects.all()
	print(StoreData)
	StoreDataStr = serializers.serialize("json",StoreData,cls=DjangoJSONEncoder)
	print(StoreDataStr)
	return render(request, 'maps.html', {'StoreDataStr':StoreDataStr,'user':user})


def Profile(request):
	if request.method == "POST":
		userId = request.session['UserId']
		Name= request.POST['name']
		Age= request.POST['age']
		Phone= request.POST['phone']
		Email= request.POST['email']
		Address= request.POST['address']
		userDetails.objects.filter(id=userId).update(Name=Name,Age=Age,Phone=Phone,Email=Email,Address=Address)
		messages.info(request,"Details Updated")
		return redirect('/Profile/')
	else:
		userId = request.session['UserId']
		details = userDetails.objects.filter(id=userId)
		return render(request,"Profile.html",{'details':details})

import re

class Message(View):

	def post(self, request):
		msg = request.POST.get('message')
		print(msg)
		# Check if the user's input contains the phrase "my name is" followed by the name
		match = re.search(r"my name is (\w+)", msg, re.IGNORECASE)
		if match:
			name = match.group(1)
			print("User's name:", name)
			# Use the extracted name in the chatbot response
			response = f"Hello {name}! How can I assist you today?"
		else:
			response = chatbot_response(msg)
		valid = validators.url(response)
		if valid==True:
			data1 = 'True'
			data = {
			'respond': response,'respond1':data1
			}
			return JsonResponse(data)
		else:
			data1 = 'False'
			data = {
			'respond': response,'respond1':data1
			}
			return JsonResponse(data)




		
	   
	 




def train_chatbot_model(request):
	lemmatizer = WordNetLemmatizer()

	words = []
	classes = []
	documents = []
	ignore_words = ['?', '!']
	data_file = open(INTENTS_PATH).read()
	intents = json.loads(data_file)
	for intent in intents['intents']:
	    for pattern in intent['patterns']:

	        #tokenize each word
	        w = nltk.word_tokenize(pattern)
	        words.extend(w)
	        #add documents in the corpus
	        documents.append((w, intent['tag']))

	        # add to our classes list
	        if intent['tag'] not in classes:
	            classes.append(intent['tag'])

	# lemmatize, lower each word and remove duplicates
	words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
	words = sorted(list(set(words)))
	# sort classes
	classes = sorted(list(set(classes)))
	# documents = combination between patterns and intents
	print (len(documents), "documents")
	# classes = intents
	print (len(classes), "classes", classes)
	# words = all words, vocabulary
	print (len(words), "unique lemmatized words", words)

	pickle.dump(words,open(WORDS_PATH,'wb'))
	pickle.dump(classes,open(CLASSES_PATH,'wb'))
	# create our training data
	training = []
	# create an empty array for our output
	output_empty = [0] * len(classes)
	# training set, bag of words for each sentence
	for doc in documents:
	    # initialize our bag of words
	    bag = []
	    # list of tokenized words for the pattern
	    pattern_words = doc[0]
	    # lemmatize each word - create base word, in attempt to represent related words
	    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
	    # create our bag of words array with 1, if word match found in current pattern
	    for w in words:
	        bag.append(1) if w in pattern_words else bag.append(0)
	    # output is a '0' for each tag and '1' for current tag (for each pattern)
	    output_row = list(output_empty)
	    output_row[classes.index(doc[1])] = 1
	    training.append([bag, output_row])
	# shuffle our features and turn into np.array
	random.shuffle(training)
	training = np.array(training,dtype=object)
	# create train and test lists. X - patterns, Y - intents
	train_x = list(training[:,0])
	train_y = list(training[:,1])
	print("Training data created")
	# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
	# equal to number of intents to predict output intent with softmax
	model = Sequential()
	model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(64, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(len(train_y[0]), activation='softmax'))
	#opt = keras.optimizers.Adam(lr=0.001)
	# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
	#sgd = SGD(opt, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	#fitting and saving the model
	hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
	score = model.evaluate(np.array(train_x),np.array(train_y), verbose=0)
	#print('Test loss:', score[0])
	#print('Train accuracy:', score[1])
	Training_Accuracy = score[1]*100
	print('Training Accuracy=',Training_Accuracy)
	model.save(MODEL_PATH, hist)

	print("model created")
	return JsonResponse({"message": "Chatbot model trained successfully"})
	return redirect('/Manage_Question/')



def Demo(request):
	return render(request,"Demo.html",{})


def run_training_and_redirect(request):
    # Run the training script using subprocess with dynamic path
    subprocess.run(['python', MAIN_PATH])
    return JsonResponse({"message": "Chatbot model trained successfully"})
    # Redirect to the desired URL
    return redirect('/Manage_Question/')



def Logout(request):
	Session.objects.all().delete()
	return redirect("/")



