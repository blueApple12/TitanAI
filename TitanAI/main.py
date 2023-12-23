import openai
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import pyjokes
import math
import json

dt = datetime.datetime.now()
current_time = dt.strftime("%H:%M")
current_date = dt.strftime("%Y-%m-%d")
weekday = dt.strftime("%A")
wiki = wikipedia.summary
writing_mode = False

openai.api_key = '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'

bot_Instructions = "You are Titan AI a voice ai program that was designed by Avishai to help people with any question they need"

with open('profiles.json') as f:
    user_profiles = json.load(f)['users']
selected_user_index = 0
selected_user = user_profiles[selected_user_index]



def Reply(question):
    prompt =(f'bot Instructions: {bot_Instructions}\n'
             f'Current Date: {current_date}\n'
             f'Current Time: {current_time}\n'
             f'Weekday: {weekday}\n'
             f'Wikipedia knowledge: {wiki}\n'
             f'Joke: {pyjokes.get_joke}\n'
             f'Math knowledge: {math}\n'
             f'User: {selected_user}\n'
             f'You: {question}\n')
    
    response = openai.completions.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
    )
    answer = response.choices[0].text.strip()


    return answer

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    print(f"Searching in Google: {query}")
    speak(f"Searching in Google: {query}")

def search_youtube(query):
    youtube_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(youtube_url)
    print(f"Searching on YouTube: {query}")
    speak(f"Searching on YouTube: {query}")


def change_user(username):
    global selected_user_index, selected_user

    user_found = False

    for index, user in enumerate(user_profiles):
        if user['name'].lower() == username.lower():
            selected_user_index = index
            selected_user = {}
            user_found = True
            break

    if user_found:
        print(f"Changed user to {username}")
    else:
        print(f"user with the name '{username}' not found. Please try again.")

    return user_found
    
print("Hello, How May I assist you today")
speak("Hello, How May I assist you today")

while True:

    if writing_mode == False:
        def takeCommand():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print('Listening....')
                r.pause_threshold = 1
                audio = r.listen(source)

            try:
                print("Recognizing.....")
                query = r.recognize_google(audio, language='en-in')
                print("You Said: {} \n".format(query))
            except Exception as e:
                print("Say That Again....")
                speak("Say That Again")
                return None
            return query
    elif writing_mode == True:
        def takeCommand():
            query = input()
            print("You Said: {} \n".format(query))
            return query

    try:
        query = takeCommand()
    except Exception as e:
        print(f"Error in voice recognition: {str(e)}")
        speak("There was an error in voice recognition. Please try again.")
        continue

    if query is None:
        continue

    if 'exit writing mode' in query or 'writing mode off' in query:
        print('writing mode is now disabled')
        speak('writing mode is now disabled')
        writing_mode = False
        continue

    ans = Reply(query)

    if 'open youtube' in query.lower():
        print('opening youtube')
        speak('opening youtube')
        webbrowser.open("www.youtube.com")
        break
    elif 'open google' in query.lower():
        print('opening google')
        speak('opening google')
        webbrowser.open("www.google.com")
        break
    elif 'meaning of life' in query.lower():
        print('The Answer to the Ultimate Question of Life, the Universe, and Everything is 42')
        speak('The Answer to the Ultimate Question of Life, the Universe, and Everything is 42')
    elif 'secret command' in query.lower():
        print('you found the secret commands that do nothing! congrats!')
        speak('you found the secret commands that do nothing! congrats!')
    elif 'writing mode' in query.lower():
        if not writing_mode:
            print('writing mode is now enabled')
            print('write "writing mode off" or "exit writing mode" to exit writing mode')
            speak('writing mode is now enabled. write "writing mode off" or "exit writing mode" to exit writing mode')
            writing_mode = True
        else:
            print('writing mode is already enabled')
            speak('writing mode is already enabled')
        continue
    elif query.lower().startswith('search') and 'in google' in query.lower():
        search_query = query.lower().replace('search', '').replace('in google', '').strip()
        search_google(search_query)
        break
    elif query.lower().startswith('search') and 'on youtube' in query.lower():
        search_query = query.lower().replace('search', '').replace('on youtube', '').strip()
        search_youtube(search_query)
        break
    elif 'change user to' in query.lower():
        username = query.lower().replace('change user to', '').strip()
        success = change_user(username)

        if success:
            speak(f"Changed user to {username}")
        else:
            speak(f"User with the name '{username}' not found. Please try again.")
        continue
    elif 'change profile to' in query.lower():
        username = query.lower().replace('change profile to', '').strip()
        success = change_user(username)

        if success:
            speak(f"Changed user to {username}")
        else:
            speak(f"user with the name '{username}' not found. Please try again.")
        continue
    elif 'bye' in query.lower():
        print('Goodbye')
        speak('Goodbye')
        break
    else:
        print(ans)
        speak(ans)