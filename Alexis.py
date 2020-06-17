import speech_recognition as sr # to recognize the speech
import playsound
import os
import random
from gtts import gTTS
from time import ctime
import time
import webbrowser
import pyaudio

# This method to print the working microphone indices
def microphoneIndex():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))


# print(pyaudio.pa.get_default_input_device())
# print(sr.Microphone().list_microphone_names())

r = sr.Recognizer()

def record_audio(ask = False):
    # print("__________record_audio")
    with sr.Microphone() as source:
        if ask:
            alexis_speak(ask)
        # r.adjust_for_ambient_noise(source, duration=0.2)
        # r.energy_threshold = 50
        # r.dynamic_energy_threshold = False
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            alexis_speak("Sorry, I did not get that")
        except sr.RequestError:
            alexis_speak("Sorry, my speech service is down")

        return voice_data

def alexis_speak(audio_string):
    # print("_________alexis_speak")
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 1e10)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def respond(voice_data):
    # print("___________respond")
    if 'what is your name' in voice_data:
        alexis_speak("My name is Alexis")
    elif 'what time is it' in voice_data:
        alexis_speak(ctime())
    elif 'search' in voice_data:
        search = record_audio("what do you want to search for?...")
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        alexis_speak("Here is waht I found for " + search)
    elif 'find location' in voice_data:
        location = record_audio("what is the location you want?...")
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        alexis_speak("Here is the location of " + location)
    elif 'exit' in voice_data:
        alexis_speak("See you later...")
        exit()
    elif 'options' in voice_data:
        print("search")
        print("find location")
        print("what time is it")
        print("exit")


time.sleep(1)
alexis_speak("How can I help you?...")
while 1:
    voice_data = record_audio()
    respond(voice_data)