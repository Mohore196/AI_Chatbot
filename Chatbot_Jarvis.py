import speech_recognition as sr
import pyttsx3
import webbrowser
import pywhatkit
import datetime
from openai import OpenAI
from websockets.asyncio import messages
client = OpenAI(base_url="http://localhost:1234/v1" , api_key="lm-studio")

def log_interaction(user_text, ai_text):
    with open("chat_history.txt","a",encoding="utf-8") as file:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        file.write(f"[{timestamp}] \n")
        file.write(f"User : {user_text} \n")
        file.write(f"AI : {ai_text} \n")
        file.write("-"*40 + "\n")


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e :
            return "Sorry, I didn't get that. Please try again."

if __name__ == '__main__':
    print ('Pycharm')
    say("Hello , I am Jarvis A.I")
    while True:
        print("Listening.....")
        query = takeCommand().lower()
        #todo: more sites
        sites =[["YouTube","https://www.youtube.com"],["Wikipedia","https://www.wikipedia.com"],["Google","https://www.google.com"]]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Open {site[0]}")
                webbrowser.open (site[1])
        #todo:Feature of music
        if 'play' in query:
                song = query.replace('play','')
                say('playing' + song)
                pywhatkit.playonyt(song)
        #todo:Time
        if "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strTime}")
        #todo: Facetime
        if "facetime" in query:
            say("Opening FaceTime link in your browser")
            facetime_link = "https://www.facetime.com"
            webbrowser.open(facetime_link)
        #todo: Open AI
        else:
            print("Thinking...")
            try:
                response = client.chat.completions.create(
                    model="llama-3.2-1b-instruct",
                    messages=[{"role":"user","content":query}],
                )
                ai_response= response.choices[0].message.content
                log_interaction(query,ai_response)
                say(ai_response)
            except Exception as e:
                print(f"Error : {e}")







       # say(query)


