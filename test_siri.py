import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import wolframalpha
import subprocess
from os import path
import timeit
import requests
import pyautogui
from forex_python.converter import CurrencyRates 
from speedtest import Speedtest   



sr.pause_threshold = 2
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        talk("Good Morning !")
    elif hour >= 12 and hour < 18:
        talk("Good Afternoon !")
    else:
        talk("Good Evening !")
        
talk("I am alexa. How may I help you")

def take_command():
    try:
         with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source)
                print('listening...')
                voice = listener.listen(source,timeout=4, phrase_time_limit=4)
                command = listener.recognize_google(voice)
                command = command.lower()
                if 'alexa ' in command:
                    command = command.replace('alexa ','')
                    print(command)
         return command
    except:
         return ''
 


command = take_command()




def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


NOTE_STRS = ["make a note", "write this down", "remember this"]
for phrase in NOTE_STRS:
    if phrase in command:
        talk("what would you like me to write?")
        note_text = take_command().lower()
        note(note_text)
        talk("I have made note of that")


def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        talk("The day is " + day_of_the_week) 


def run_alexa():
     command = take_command()
     print(command)
     if 'play' in command:
         song = command.replace('play', '')
         talk('playing' + song)
         pywhatkit.playonyt(song)
     elif 'time' in command:
         time = datetime.datetime.now().strftime('%I:%M %p')
         talk('current time is ' + time)         
     elif 'what day is it' in command:
         day = datetime.datetime.today()
         talk('today is ' + str(day))
         #tellDay()
     elif 'who is' in command:
         person = command.replace('who is','')
         info = wikipedia.summary(person, 2)
         print(info)
         talk(info)
     elif 'date' in command:
         talk('sorry, I dont like you')
     elif 'are you single' in command:
         talk('no')
     elif 'joke' in command:
         talk(pyjokes.get_joke())
     elif 'youtube' in command:
         video = command
         talk('playing' + video)
         pywhatkit.playonyt(video) 
     elif "bye" in command:
         talk("Shutting down")
         exit()
     elif "search" in command:
         pywhatkit.search(command)
         google = command.replace('search', '')
         talk(google)
     elif "calculate" in command:
            try:
                app_id = "JUGV8R-RXJ4RP7HAG"
                client = wolframalpha.Client(app_id)
                indx = command.lower().split().index('calculate')
                command = command.split()[indx + 1:]
                res = client.query(' '.join(command))
                answer = next(res.results).text
                print("The answer is " + answer)
                talk("The answer is " + answer)

            except Exception as e:
                print("Couldn't get what you have said, Can you say it again??")
     elif 'volume up' in command:
            pyautogui.press("volumeup")
     elif 'volume down' in command:
            pyautogui.press("volumedown")
     elif 'mute volume' in command:
            pyautogui.press("volumemute")
     elif 'convert currency' in command:
            try:
                curr_list = {
                    'dollar': 'USD', 'taka': 'BDT', 'dinar': 'BHD',
                    'rupee': 'INR', 'afghani': 'AFN', 'real': 'BRL',
                    'yen': 'JPY', 'peso': 'ARS', 'pound': 'EGP', 'rial': 'OMR',
                    'lek': 'ALL', 'kwanza': 'AOA', 'manat': 'AZN', 'franc': 'CHF'
                }

                cur = CurrencyRates()
                # print(cur.get_rate('USD', 'INR'))
                talk('From which currency u want to convert?')
                from_cur = command()
                src_cur = curr_list[from_cur.lower()]
                talk('To which currency u want to convert?')
                to_cur = command()
                dest_cur = curr_list[to_cur.lower()]
                talk('Tell me the value of currency u want to convert.')
                val_cur = float(command())
                # print(val_cur)
                print(cur.convert(src_cur, dest_cur, val_cur))
                        
            except Exception as e:
                print("Couldn't get what you have said, Can you say it again??")

     elif 'stop code' in command:
         exit()
     elif 'shut up' in command:
         exit()
     elif 'internet speed' in command:
            st = Speedtest()
            print("I am checking your Internet Speed...")
            talk("I am checking your Internet Speed...")
            dw_speed = st.download()
            up_speed = st.upload()
            dw_speed = dw_speed / 1000000
            up_speed = up_speed / 1000000
            print('Your download speed is', round(dw_speed, 3), 'Mbps')
            print('Your upload speed is', round(up_speed, 3), 'Mbps')
            talk(f'Your download speed is {round(dw_speed, 3)} Mbps')
            talk(f'Your upload speed is {round(up_speed, 3)} Mbps')

     #else:
      #   pywhatkit.search(command)
       #  talk(command)
     

while True:
    run_alexa()
