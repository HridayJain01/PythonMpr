import tkinter as tk
import speech_recognition as sr
import os
import webbrowser
import datetime
from youtube_search import YoutubeSearch
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pyttsx3

# Function to speak out text
def say(text):
    os.system(f"say {text}")  # Fallback to system synthesizer

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)  # Increase timeout if needed
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return "Some Error Occurred. Sorry from Jarvis"
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
            return "Some Error Occurred. Sorry from Jarvis"


# Create the main window
root = tk.Tk()
root.title("Desktop Widget")
root.geometry("200x200")

# Function to make the window stay on top
def toggle_stay_on_top():
    if root.attributes('-topmost'):
        root.attributes('-topmost', False)
        stay_on_top_button.config(text="Stay on Top")
    else:
        root.attributes('-topmost', True)
        stay_on_top_button.config(text="Not on Top")



def extract_snippet(url):
    """Fetches and extracts the snippet from a given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if description_tag:
            snippet = description_tag.get('content')
            return snippet
        else:
            return "Snippet not found on the page."
    else:
        return "Failed to fetch page content."


def sayaloud(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        os.system(f"say {text}")


def google_search_with_snippet(query, num_results=1):
    """Performs a Google search and retrieves search results with snippets."""
    search_results = search(query, num_results=num_results)
    for i, result in enumerate(search_results, start=1):
        snippet = extract_snippet(result)
        print(f"{snippet}\n")
        sayaloud(snippet)  # Call sayaloud to speak the snippet

def searchedit(text, keywords):
    """Edits the text by removing unnecessary keywords and replacing spaces with '+' for searches."""
    for keyword in keywords:
        text = text.replace(keyword, "", 1)
    return text.replace(" ", "+")


# Function to handle voice commands
def handle_voice_command():
    query = takeCommand()

    if "play" in query:
        if "youtube" in query:
            deletethese = ["on+youtube+for", "on+youtube", "youtube+for", "play", "youtube"]
            queryedit = searchedit(query, deletethese)
            results = YoutubeSearch(queryedit, max_results=1).to_dict()
            if results:
                top_result = results[0]
                video_url = f"https://www.youtube.com/watch?v={top_result['id']}"
                webbrowser.open(video_url)
            else:
                print("No search results found.")
        elif "spotify" in query:
            deletethese = ["on+spotify+for", "on+spotify", "spotify+for", "play", "spotify "]
            queryedit = searchedit(query, deletethese)
            queryedit = queryedit.replace("+", " ")
            webbrowser.open("https://open.spotify.com/search/" + queryedit)

        # Search functionalities
    if "search" in query:
        if "youtube" in query:
            deletethese = ["on+youtube+for", "on+youtube", "youtube+for", "search", "youtube","for"]
            queryedit = searchedit(query, deletethese)
            webbrowser.open("https://www.youtube.com/results?search_query=" + queryedit)
        elif "spotify" in query:
            deletethese = ["on+spotify+for", "on+spotify", "spotify+for", "search", "spotify ","for"]
            queryedit = searchedit(query, deletethese)
            queryedit = queryedit.replace("+", "%20")
            webbrowser.open("https://open.spotify.com/search/" + queryedit)
        else:
            google_search_with_snippet(query)
    #webbrowser.open("https://google.com/search?q="+query.replace(" ","+"))
    sites = [["youtube", "https://youtube.com"],
             ["wikipedia", "https://wikipedia.org"],
             ["google", "https://google.com"],
             ["chat", "https://chat.openai.com"]]



    for site in sites:
        if f"open {site[0]}".lower() in query:
            say(f"Opening {site[0]} Sir...")
            webbrowser.open(site[1])

    if "play music" in query:
        say("Playing Music")
        musicPath= "/Users/hridayjain/Desktop/python/music/Unstoppable(Mr-Jatt1.com).mp3"
        import subprocess, sys

        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, musicPath])

        #add more songs to it

    if "the time" in query:
        strfTime=datetime.datetime.now().strftime("%H:%M:%S")
        say(f"Sir the time is {strfTime}")

    if "open facetime" in query:
        say("Opening Facetime")
        os.system(f"open /System/Applications/FaceTime.app")

    if "open code" in query:
        say("Opening PyCharm")
        os.system(f"open /Applications/PyCharm.app")

    #start making an apps list to make it more useable
    if "open whatsapp" in query:
        say("Opening Whatsapp")
        os.system(f"open /Applications/WhatsApp.app")

    if "thanks" in query:
        say("Welcome and bye sir")
        quit()

    if "who is the best" in query:
        say("Alps")

    if "Hello".lower() in query:
        say("Hello Sir")

# Button to toggle "stay on top" behavior
stay_on_top_button = tk.Button(root, text="Stay on Top", command=toggle_stay_on_top)
stay_on_top_button.pack(pady=10)

# Button to handle voice commands
voice_command_button = tk.Button(root, text="Voice Command", command=handle_voice_command)
voice_command_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
