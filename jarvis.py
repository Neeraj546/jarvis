import speech_recognition as sr
import os
import webbrowser
import pyttsx3
import time
import conf
from boltiot import Bolt
import todaydate
import yourdata
import subprocess
import json
from importlib import reload
from googlesearch import search

#Definations
mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voice')
engine.setProperty('voice', voices[0])
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)
myname = "Jarvis"
url = "https://google.com/search?q="
searched = False

#Functions

def googlesrch(query):
	try:
		for j in search(query, tld="com",lang='en', num=1, stop=1, pause=2):
			webbrowser.get().open(j)
			speak("Here is what i found")
	except:
		msg="Something Went Wrong"
		speak(msg)
		
def namecheck():
	if yourdata.name == " " :
		speak("Hey i am Jarvis, Whats your name :")
		myfile = open("yourdata.py","a+")
		temp = input("Your Name :")
		myfile.write('name = "' + temp +'"')
		myfile.close()
		reload(yourdata)

def speak(msg):
	engine.say("{}".format(msg))
	engine.runAndWait()
	engine.stop()


def listenme():
	with sr.Microphone() as source:
		audio = r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
	try:
		print(r.recognize_google(audio))
		reload(todaydate)
		return(r.recognize_google(audio))
	except:
		print("Couldn't Hear!")
		return(listenme())

namecheck()
speak("hey " + yourdata.name + "How can i help you")
alrm = True
while True:
	os.system("clear")
	query = listenme().lower()
	if "hello jarvis" in query:
		speak("Hello " + yourdata.name)
	elif "sleep jarvis" in query:
		speak("i am going to sleep sir")
		slept = True
		while slept:
			query = listenme().lower()
			if "wake up jarvis" in query:
				slept = False
				speak("Online and ready sir")
	elif "search" in query:
		speak("What do you wanna search")
		searchele = listenme().lower()
		googlesrch(searchele)
		searched = True
	elif "show more results" in query:
		if(searched):
			webbrowser.get().open(url + searchele)
			msg = "Here are more results for " + searchele
			speak(msg)
		else:
			speak("What do you wanna search")
			searchele = listenme().lower()
			webbrowser.get().open(url + searchele)
	elif "turn off computer" in query:
		speak("are you sure?")
		query = listenme().lower()
		if "yes" or "sure" in query:
			speak("OK, Turning off computer")
			os.system("shutdown now")
		else:
			speak("ok Listening")
	elif "what's my name" in query:
		speak(yourdata.name)
	elif "tell me about yourself" in query:
		speak("Hello I'm Jarvis. I was developed by Neeraj and he integrated me with bolt platform. I can help humans to avoid physical contacts. and avoid spreading Harmful virus like corona")
	elif "open audacity" in query:
		speak("Opening audacity sir")
		subprocess.call("audacity")
	elif "turn on light" in query:
		speak("Turning on lights")
		mybolt.digitalWrite('0','HIGH')
	elif "turn off light" in query:
		speak("Turning off lights")
		mybolt.digitalWrite('0','LOW')
	elif "what time is it" in query:
		if(todaydate.hours > 12):
			prnttime = "it's " + str(todaydate.hours-12) + " " + str(todaydate.mins) + " PM"
			speak(prnttime)
		else:
			prnttime = "it's " + str(todaydate.hours) + " " + str(todaydate.mins) + " AM"
			speak(prnttime)
	elif "what day is it" in query:
		prnttime = "it's" + str(todaydate.todayday)
		speak(prnttime)
	elif "room temperature" in query:
		try:
			response = mybolt.analogRead('A0') 
			data = json.loads(response)
			temp = "it's " + str(int((100*int(data['value']))/1024)) + " degree Celcius"
			speak(temp)
		except:
			speak("Could not fetch data from device. check whether your device and sensors are working properly")
	elif "today's date" in query:
		if((todaydate.todaydat%10 == 1) or (todaydate.todaydat == 1)):
			prnttime = "it's " + str(todaydate.todaydat) + " st " + str(todaydate.todaymon) + str(todaydate.todayyear)
		if((todaydate.todaydat%10 == 2) or (todaydate.todaydat == 2)):
			prnttime = "it's " + str(todaydate.todaydat) + " nd " + str(todaydate.todaymon) + str(todaydate.todayyear)
		if((todaydate.todaydat%10 == 3) or (todaydate.todaydat == 3)):
			prnttime = "it's " + str(todaydate.todaydat) + " rd " + str(todaydate.todaymon) + str(todaydate.todayyear)
		else:
			prnttime = "it's " + str(todaydate.todaydat) + " th " + str(todaydate.todaymon) + str(todaydate.todayyear)
		speak(prnttime)
	else:
		speak("sorry could not recognize")
		
