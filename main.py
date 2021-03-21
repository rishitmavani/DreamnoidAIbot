import pyjokes
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import speedtest
import sys
import os
import smtplib
import random
import tkinter as tk
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import subprocess
from textblob import TextBlob
import geoip2.database
import time
import requests
import pywhatkit as kit
from requests import get

name = "dreamnoid"
engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)
starting = ["Hello!", "Hey!", "How are you?", "How's day going?"]
greetings = ["Your welcome sir!", "Happy to help you sir", "Here for you anytime!"]
goodbyes = ["See you soon!", "Have a great day!", "Good bye", "Bye-Bye", "Cya"]
prefix = ["Hold on,", "Alright,", "Hang on,", "Okay sir,"]


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    if 0 <= hour < 12:
        speak(f"Good Morning!, its {tt}")

    elif 12 <= hour < 18:
        speak(f"Good Afternoon!, its {tt}")
    else:
        speak(f"Good Evening! its {tt}")

    start = random.choice(starting)
    speak(f"{start} sir, I am {name} your personal assistant! How may I help you?")


def takeCommand():
    # It takes microphone i/o from the user and return string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Listening....")
        speak("Listening to your commands sir!")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        # print("Recognizing...")
        speak("Recognizing your command......")
        query = r.recognize_google(audio, language='en-us')
        # print(f"You said: {query.lower()}\n")

    except Exception:
        speak("I couldn't understand it, say that again sir.....")
        # print("Say that again please....")
        return "None"
    return query.lower()


def WakeupCall(choice):
    # It takes microphone i/o from the user and return string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Listening....")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-us')
        if choice == 1:
            speak("Waiting for the command sir.....")
        else:
            ranprefix = random.choice(prefix)
            speak(ranprefix)

    except Exception:
        speak("Couldn't understand it sir!")
        return "None"
    return query.lower()


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremailid', 'password')
    server.sendmail('youremailid', to, content)
    server.close()


class CurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        # first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]

        # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


def Tasks():
    global name
    while True:
        def wakeLoop():
            speak("wake me up when you want!")
            wakeUp = WakeupCall(choice=1).lower()
            if "hey dreamnoid" in wakeUp or "hey" in wakeUp or "wakeup" in wakeUp or "listen" in wakeUp:
                Tasks()

        query = takeCommand().lower()
        # query = "don't listen"

        if 'morning already' in query:
            hour = int(datetime.datetime.now().hour)
            if 0 <= hour < 12:
                speak("Yes, sir it is " + datetime.datetime.now().strftime("%H and %M") + "Good morning!")
                wakeLoop()

            elif 12 <= hour < 18:
                speak("Nein, sir it is " + datetime.datetime.now().strftime("%H and %M") + "Good Afternoon!")
                wakeLoop()
            else:
                speak("Negative, sir it is " + datetime.datetime.now().strftime("%H and %M") + "Good evening!")
                wakeLoop()
            speak("what is my task for today master!?")

        elif 'weather' in query or 'temperature' in query:
            def get_temperature(json_data):
                temp_in_celcius = json_data['main']['temp']
                return temp_in_celcius

            def get_weather_type(json_data):
                weather_type = json_data['weather'][0]['description']
                return weather_type

            def get_wind_speed(json_data):
                wind_speed = json_data['wind']['speed']
                return wind_speed

            def get_weather_data(city):
                api_address = 'https://api.openweathermap.org/data/2.5/weather?appid=a10fd8a212e47edf8d946f26fb4cdef8' \
                              '&q= '
                units_format = "&units=metric"
                final_url = api_address + city + units_format
                json_data = requests.get(final_url).json()

                var = json_data['weather'][0]['description']
                if choice == 1:
                    temperature = get_temperature(json_data)
                    weather_details = ''
                    speak(weather_details + f"The temperature in {city} is currently of {temperature} degrees")
                else:
                    weather_type = get_weather_type(json_data)
                    temperature = get_temperature(json_data)
                    wind_speed = get_wind_speed(json_data)
                    weather_details = ''
                    speak(
                        weather_details + f"The weather in {city} is currently {weather_type} with a temperature of {temperature} degrees and wind speeds reaching {wind_speed} kilo meter per hour")

            if 'temperature' in query:
                speak("Speak only the name of city....")
                speak("Of which city you want to see the temperature sir?")
                city = takeCommand().lower()
                # city = "Surat"
                speak("You selected " + city)
                speak("say yes to continue or no for taking name again!")
                ans = WakeupCall(choice=0).lower()
                if 'yes' in ans:
                    choice = 1
                    get_weather_data(city)
                    wakeLoop()
                elif 'no' in ans:
                    speak("Say only the name of which city you want to see the temperature sir.")
                    city = takeCommand().lower()
                    # city = "Surat"
                    speak("You selected " + city)
                    choice = 1
                    get_weather_data(city)

            else:
                speak("Speak only the name of the city!")
                speak("Of which city you want to see the weather sir?")
                city = takeCommand().lower()
                # city = "Surat"
                speak("You selected " + city)
                speak("say yes to continue or no for taking name again!")
                ans = WakeupCall(choice=0).lower()
                if 'yes' in ans:
                    choice = 0
                    get_weather_data(city)
                    wakeLoop()
                elif 'no' in ans:
                    speak("Only say the name of which city you want to see the weather sir.")
                    city = takeCommand().lower()
                    # city = "Surat"
                    speak("You selected " + city)
                    choice = 0
                    get_weather_data(city)

        elif 'news' in query:
            try:
                news_url = "https://news.google.com/news/rss"
                Client = urlopen(news_url)
                xml_page = Client.read()
                Client.close()
                soup_page = soup(xml_page, "xml")
                news_list = soup_page.findAll("item")
                li = []
                for news in news_list[:15]:
                    li.append(str(news.title.text.encode('utf-8'))[1:])

                for _ in range(len(li)):
                    if " - " in li[_]:
                        lie = li[_].replace(" - ", " said by ")
                        speak(lie)
                        print(lie)
                return li

            except Exception as e:
                print(e)
                return False

        elif 'convert' in query:
            if 'currency' in query or 'money' in query:
                speak("say initials of which currency you want to convert")
                # base = "EUR"
                base = WakeupCall(choice=0).upper()
                speak("You said" + base)
                # print(base)
                speak("say initials of in which you want to convert")
                # con = "INR"
                con = WakeupCall(choice=0).upper()
                speak("you said" + con)
                # print(con)
                speak("how much amount you want to convert? sir")
                # amount = 10000
                amount = WakeupCall(choice=0)
                print(amount)
                speak("The amount to convert is" + str(amount))
                # print(amount)
                url = 'https://api.exchangerate-api.com/v4/latest/USD'
                converter = CurrencyConverter(url)
                try:
                    conamount = converter.convert(base, con, int(amount))
                # print(conamount)
                    speak("After converting the amount is " + str(conamount))
                except Exception:
                    speak("Invalid name of the currency or amount found!")
                wakeLoop()

        elif 'calculate' in query:
            speak("Which method you want to calculate in, sir?")
            method = takeCommand().lower()
            # print(method)
            if 'sum' in query or 'addition' in query:
                speak("Say the first value sir!")
                fvalue = float(takeCommand())
                speak("Say the second value sir!")
                svalue = float(takeCommand())
                finalvalue = fvalue + svalue
                speak(f"Sum of {str(fvalue)} + {str(svalue)} is {str(finalvalue)}")
                # print(finalvalue)

            elif 'multiply' in query:
                speak("Say the first value sir!")
                fvalue = float(takeCommand())
                speak("Say the second value sir!")
                svalue = float(takeCommand())
                finalvalue = fvalue * svalue
                speak(f"Multiplication of {str(fvalue)} into {str(svalue)} is {str(finalvalue)}")
                # print(finalvalue)
            elif 'divide' in query or 'division' in query:
                speak("Say the first value sir!")
                fvalue = float(takeCommand())
                speak("Say the second value sir!")
                svalue = float(takeCommand())
                finalvalue = fvalue / svalue
                speak(f"Division of {str(fvalue)} by {str(svalue)} is {str(finalvalue)}")
                # print(finalvalue)
            elif 'subtraction' in query or 'subtract' in query or 'minus' in query:
                speak("Say the first value sir!")
                fvalue = float(takeCommand())
                speak("Say the second value sir!")
                svalue = float(takeCommand())
                finalvalue = fvalue - svalue
                speak(f"By Subtracting {str(fvalue)} from {str(svalue)}, remaining digits is {str(finalvalue)}")
                # print(finalvalue)
            else:
                speak("Sorry I couldn't understand it sir!")
                wakeLoop()
            wakeLoop()

        elif 'translate' in query or 'translator' in query:
            speak("do i need to detect the language or not?")
            ans = takeCommand().lower()
            if ans == 'yes' or 'detect':
                speak("Start speaking to detect!")
                detect = query.lower()
                if len(detect) <= 1:
                    # detect = 'tumhara name kya hai'
                    blob = TextBlob(u'' + detect)
                    # print(blob.detect_language())
                    speak("Language detected!")
                    speak("Translating to english sir.")
                    # print(blob.translate(to='en'))
                    speak(blob.translate(to='en'))
                else:
                    speak("You didn't said anything sir")

            elif ans == 'no' or ans == 'don\'t':
                speak("from which language I need to translate from sir?")
                lan = takeCommand().lower()
                # print(lan)
                speak("start speaking to translate!")
                trans = takeCommand().lower()
                blob = TextBlob(u'' + trans)
                speak(blob.translate(to='en'))
            else:
                pass

            wakeLoop()

        # elif 'jarvis' in query:
        #   speak("I am dreamnoid sir, and who is jarvis firstly!")
        #    query = takeCommand().lower()
        #   if 'sorry dreamnoid' in query:
        #       speak("who is jarvis not the sorry sir. you have sidebot")
        #   elif 'my x' in query:
        #       speak("you never had relationship sir, don't lie lol")
        #   else:
        #       "huh! whatever, tell me what to do."
        #   query = takeCommand().lower()
        #  if 'angry' in query:
        #       speak("ohh, ofcourse i am not what you think so.")
        #   else:
        #      speak("Surely! you don't even need to remember my name.")
        #       speak("please tell me again what to do?")
        #       break

        elif 'long day' in query or 'without you' in query:
            speak("Aw! sir, i you missed me sir?")
            query = takeCommand()
            if 'of course' in query or 'yes' in query:
                speak("That's so sweet of you sir. But you should work on your own sometimes!")
            else:
                speak("Ah! i know you miss me but it was a nice day without work i must say! he he he he he he")

            wakeLoop()

        elif 'to follow' in query:
            speak("without a doubt sir!")

            wakeLoop()

        elif 'nothing' in query or 'nothing for right now' in query or 'no work' in query:
            speak("Alright, sir ask me whenever you need.")
            wakeLoop()

        elif 'search online' in query:
            # query = takeCommand()
            if 'about' in query:
                query = query.replace("search online about", "")
            elif 'for' in query:
                query = query.replace("search online for", "")
            elif 'jarvis' in query:
                query = query.replace("search online", "").replace("jarvis", "")
            elif 'dreamnoid' in query:
                query = query.replace("search online", "").replace("dreamnoid", "")
            if 'for' and 'dreamnoid' in query:
                query = query.replace("search online for", "").replace("dreamnoid", "")
            elif 'about' and 'dreamnoid' in query:
                query = query.replace("search online about", "").replace("dreamnoid", "")
            if 'for' and 'jarvis' in query:
                query = query.replace("search online for", "").replace("jarvis", "")
            elif 'about' and 'jarvis' in query:
                query = query.replace("search online about", "").replace("jarvis", "")
            else:
                query = query.replace("search online", "")

            prefixran = random.choice(prefix)
            speak(prefixran + ", I will show you information about " + query + ".")
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open("http://www.google.com/search?q=" + query)
            speak("Here, it is in your screen sir!")
            wakeLoop()

        elif 'my ip address' in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your ip address is {ip} sir.")
            wakeLoop()

        elif 'send message' in query:
            speak("To which number you want to send message sir")
            speak("say the number please")
            number = int(takeCommand())
            speak("What should I write in message sir?")
            msg = takeCommand()
            speak("at what hour i should send message sir?")
            hr = int(takeCommand())
            speak("at what minute sir?")
            mi = int(takeCommand())
            kit.sendwhatmsg(number, msg, hr, mi)
            speak("Message successfully sent sir.")
            wakeLoop()

        elif 'check internet speed' in query or 'internet speed' in query or 'speed of internet' in query:
            speak("On to it! sir, asking my friend internet for his current speed")
            st = speedtest.Speedtest()
            st.get_best_server()
            rawdl = st.download()
            roundedspeed = round(rawdl)
            finaldl = format(roundedspeed / 1e+6, ".2f")
            rawup = st.upload()
            speak("He is taking time for replying!")
            roundedspeedup = round(rawup)
            finalup = format(roundedspeedup / 1e+6, ".2f")
            # print(f"We have {finaldl} mega bytes per second downloading speed and {finalup} mega bytes per second
            # uploading speed")
            speak("He says,")
            speak(
                f"We have {finaldl} mega bytes per second downloading speed and {finalup} mega bytes per second "
                f"uploading speed")

            wakeLoop()

        elif 'on youtube' in query:
            speak("What should i play")
            topic = takeCommand()
            kit.playonyt(topic)
            prefixran = random.choice(prefix)
            speak(prefixran + ", On to it!")

        elif 'wikipedia' in query:
            speak('Searching wikipedia.......')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(results)
            wakeLoop()

        elif 'your name' in query:
            speak("My name is " + name)
            wakeLoop()

        elif 'play game' in query:
            steamPath = "C:\\Program Files (x86)\\Steam\\Steam.exe"
            os.startfile(steamPath)
            speak('Opening steam sir, Have fun playing!')
            wakeLoop()

        elif 'funny' in query:
            if 'not' in query:
                speak("as if my creator is funny! ha ha ha ha")
            else:
                speak("I know right!")
            wakeLoop()

        elif 'thank you' in query:
            greeting = random.choice(greetings)
            speak(greeting + "")
            wakeLoop()

        elif re.search('launch | open', query):
            dict_app = {
                'chrome': "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                'steam': 'C:\\Program Files (x86)\\Steam\\Steam.exe',
                'discord': 'C:\\Users\\Mavan\\AppData\\Local\\Discord\\app-0.0.309\\Discord.exe',
                'spotify': 'C:\\Users\\Mavan\\OneDrive\\Desktop\\Spotify',
                'pycharm': 'C:\\Program Files\\JetBrains\\PyCharm 2020.2.4\\bin\\pycharm64.exe',
                'CS go': 'C:\\Users\\Mavan\\OneDrive\\Desktop\\Counter-Strike Global Offensive',
                'prompt': 'C:\\Windows\\System32\\cmd'
            }
            keyword_list = ['youtube.com', 'google.com', 'stackoverflow.com', 'CMD']

            word = query.split()
            words = len(word)
            j = 0
            for _ in word:
                if word[j] in keyword_list:
                    prefixran = random.choice(prefix)
                    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
                    webbrowser.get(chrome_path).open(str(word[j]))
                    speak(prefixran + "Starting: " + word[j])
                    pass
                else:
                    j += 1
                if 'cmd' in query:
                    os.system("start cmd")
                    speak("Here it is.")
                    break
                else:
                    for i in range(words):
                        app = query.split(' ', i)[i]
                    '''
                      upper "for" loop for finding the word in the string to open 
                    '''
                    path = dict_app.get(app)
                    if path is None:
                        speak('Application path not found')
                        # print('Application path not found')
                        break
                    else:
                        prefixran = random.choice(prefix)
                        speak(prefixran + 'Launching: ' + app)
                        os.startfile(path)
                        break
            wakeLoop()

        elif 'shutdown' in query:
            if 'pc' in query or 'computer' in query or 'system' in query:
                prefixran = random.choice(prefix)
                speak("Are you sure you want to shutdown sir? say yes if you want cutoff the system.")
                ans = takeCommand().lower()
                if 'yes' in ans:
                    speak(prefixran + " ! Your system is on its way to shut down")
                    subprocess.call('shutdown / p /f')
                else:
                    speak("Command shutdown has been retreated!")
            else:
                pass
            wakeLoop()

        elif "restart" in query:
            if 'pc' in query or 'computer' in query or 'system' in query:
                prefixran = random.choice(prefix)
                speak("Are you sure you want to shutdown sir? say yes if you want cutoff the system.")
                ans = takeCommand().lower()
                if 'yes' in ans:
                    speak(prefixran + " ! Restarting your system, sir!")
                    subprocess.call(["shutdown", "/r"])
                else:
                    speak("Command restart has been retreated!")
            else:
                pass
            wakeLoop()

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop me from listening sir!")
            a = WakeupCall(choice=0)
            # a = "1 minute"
            # print(a)
            if 'seconds' in a or 'second' in a or 'sec' in a:
                # print("In seconds")
                ab = [int(i) for i in a.split() if i.isdigit()]
                wakeTime = ab[0]
                # print(wakeTime)
                speak("I will not be listening for next" + str(wakeTime) + "seconds.")
                time.sleep(int(wakeTime))

            elif 'minutes' in a or 'minute' in a or 'min' in a:
                # print("In minutes")
                ab = [int(i) for i in a.split() if i.isdigit()]
                wakeTime = ab[0]
                # print(wakeTime)
                WakeTime = int(wakeTime * 60)
                speak("I will not be listening for next" + str(wakeTime) + "minutes.")
                time.sleep(WakeTime)

            elif 'hours' in a or 'hour' in a:
                # print("In hours")
                ab = [int(i) for i in a.split() if i.isdigit()]
                wakeTime = ab[0]
                # print(wakeTime)
                WakeTime = int(wakeTime * 3600)
                speak("I will not be listening for next" + str(wakeTime) + "hours.")
                time.sleep(WakeTime)

            # print(a)
            wakeLoop()

        elif re.search('manual | notes | commands', query):
            speak("Showing Notes")
            file = open("dreamnoidAIbot.txt", "r")
            # print(file.read())
            speak(file.read(6))

        elif 'play music' in query:
            speak('Playing your favourite songs now!')
            music_dir = 'D:\\MUJIC'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'current time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Current time is {strTime} sir.')

        elif 'date' in query:
            strDate = datetime.datetime.now().date()
            speak(f'Current date is {strDate} sir.')

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak('Alright, to whome sir?')
                to = input()
                sendEmail(to, content)
                speak("Email sent successfully")
            except Exception as e:
                # print(e)
                speak("Sorry, I am not able to send this email for some reasons.")

        elif 'trace ip' in query or 'find ip' in query or 'locate ip' in query:
            reader = geoip2.database.Reader('./GeoLite2-City/GeoLite2-City.mmdb')
            try:
                speak("Speak the ip address only sir!")
                ip = takeCommand()
                ip = ip.replace(" ", "")

                # ip = '150.107.241.230'

                def trace():
                    response = reader.city(ip)
                    speak(str(ip) + "has been traced and details are as follow")
                    speak("Country is " + response.country.name)
                    speak("postal code is" + response.postal.code)
                    speak("in the state of" + response.subdivisions.most_specific.name)
                    speak("and" + response.city.name + "is the city name")
                    speak("Location in latitude and longitude is")
                    speak(str(response.location.latitude) + "and   ")
                    speak(str(response.location.longitude) + "Respectively")

                trace()
            except Exception:
                speak(f"Say the ip again sir, couldn't trace the current ip  that is {ip}.")
                ip = takeCommand()
                trace()
                return "None"

        elif "change name" in query:
            speak("What would you like to call me, Sir ")
            name = takeCommand()
            speak("Thanks for naming me, sir")

        elif "who made you" in query or "who created you" in query:
            speak("I have been created by Rishit Mavani.")

        elif "where is" in query:
            data = query.split(" ")
            i = len(data)
            location = data[i - 1]
            prefixran = random.choice(prefix)
            speak(prefixran + ", I will show you where " + location + " is.")
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open("http://www.google.com/maps/place/" + location + "/&amp;")
            speak("Here, it is sir.")

        elif 'have sleep' in query or 'neutralize yourself' in query or 'stop' in query or 'stop speaking' in query:
            speak("Alright sir, i am going to sleep, awake me anytime when you need sir.")
            break

        elif 'quit' in query or 'exit' in query or 'leave me alone' in query:
            speak('Auf wiedersehen, Have a great time sir!')
            sys.exit()


if __name__ == "__main__":
    window = tk.Tk()

    label_1 = tk.Label(text="Username:")
    entry_var = tk.StringVar()
    label_1.pack()
    entry = tk.Entry(window, textvariable=entry_var)
    entry.pack()

    # print(entry_var.get())


    def activate():
        var = entry_var.get()
        if var == '' or None:
            speak("Please enter the name sir this field cannot be empty!")
        else:
            label_1.pack_forget()
            entry.pack_forget()
            button.pack_forget()
            start = random.choice(starting)
            label_name.pack()
            button_1.pack(pady=10)
            speak("Registered as " + var)
            speak(start + "sir, Click button to activate your personal assistant Jiggnnass!")
            # print(f"Registered, as {var}")


    label_name = tk.Label(
        text=f"Hello, This is {name}",
        foreground="white",  # Set the text color to white
        background="black"  # Set the background color to black
    )


    def start():
        while True:
            # print("Say, hey dreamnoid or aaaiiii dreamnoid to power up...")
            permission = takeCommand().lower()
            # permission = "wake up"
            if 'wake up' in permission or 'hey dreamnoid' in permission or 'hello dreamnoid' in permission:
                wishMe()
                Tasks()
            elif 'quit' in permission or 'have sleep' in permission:
                speak('Auf wiedersehen, Have a great time sir!')
                sys.exit()


    def handle_click():
        window.destroy()
        # print("Activated!")
        speak("Activated")
        speak("Say, hey dreamnoid to power-up your assistant!")
        start()


    button = tk.Button(
        window,
        text="Click to register!",
        bg="blue",
        fg="yellow",
        command=activate,
    )


    def manual():
        speak("Opening manual!")
        os.startfile("dreamnoidAIbot.txt")


    button_manual = tk.Button(
        window,
        text='Click to see manual',
        bg="black",
        fg="white",
        command=manual
    )

    button_1 = tk.Button(
        window,
        text="Click to activate!",
        bg="blue",
        fg="yellow",
        command=handle_click,
    )


    def exit1():
        goodbye = random.choice(goodbyes)
        speak(f"Exiting! sir, {goodbye}")
        exit()


    button_exit = tk.Button(
        window,
        text='Quit',
        bg='red',
        fg='black',
        command=exit1,
    )

    button.pack(pady=10)
    button_manual.pack(pady=10)
    button_exit.pack(pady=5)

    window.mainloop()
