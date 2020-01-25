###IMPORT###
import string
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
# Requires PyAudio and PySpeech.
import speech_recognition as sr
import pyttsx3
import logging

###LOG###
logging.basicConfig(level=logging.CRITICAL)

###CREATE CHATBOT###
bot = ChatBot('Friend'
    , storage_adapter='chatterbot.storage.SQLStorageAdapter',
    preprocessors=['chatterbot.preprocessors.clean_whitespace',
                    'chatterbot.preprocessors.unescape_html',
            'chatterbot.preprocessors.convert_to_ascii'],
        silence_performance_warning=True,
        filters=["chatterbot.filters.RepetitiveResponseFilter"],
     database='./database.sqlite3'
       )

###TRAIN CHATBOT###
trainer = UbuntuCorpusTrainer(bot)
trainer.train()


###TEXT TO VOICE###
engine = pyttsx3.init() # pyttsx3 text to voice object creation

#""" RATE"""
#rate = engine.getProperty('rate')   # getting details of current speaking rate
#print (rate)                        #printing current voice rate
engine.setProperty('rate', 160)     # setting up new voice rate

#"""VOLUME"""
#volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
#print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1


#"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. 0 for male
engine.setProperty('voice', 'english')   #changing index, changes voices. 1 for female

#bot.get_response("Hello friend, how are you doing today?")    

#print("bot1")

###RUN###
while True:
	#message = input('You: ')
	###VOICE TO TEXT###
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
	try:
		output = r.recognize_google(audio)
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		print("You: " + output)
	except sr.UnknownValueError:
		print("Speech Recognition could not understand audio")
		reply = "I could not understand you, please repeat."
		print('friend:', reply)
		engine.say(reply)
		engine.runAndWait()
	except sr.RequestError as e:
		print("Could not request results, Check your internet; {0}".format(e))
		reply = "I could not understand you, please check your internet connection."
		print('friend:', reply)
		engine.say(reply)
		engine.runAndWait()
	else:
		###CONVERSATION###
		message = output.translate(str.maketrans('', '', string.punctuation))
		print("Processing, please hold.")
		#message = output
		if "bye" not in message:
			reply = bot.get_response(message)
			print('friend:', reply)
			engine.say(reply)
			engine.runAndWait()
		###KILL###
		#if message.strip() == 'bye':
		if "bye" in message:
			print('friend: GoodBye!')
			engine.say("Goodbye!")
			engine.runAndWait()
			engine.stop()
			break
	finally:
		pass
