import speech_recognition as sr
import pyttsx3
import webbrowser
import pywhatkit as kit
import pygame
import time
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Global flag to track if Chatbot should speak
speak_enabled = True

def speak(text):
    global speak_enabled
    if speak_enabled:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    print(f'{Fore.YELLOW}{Style.BRIGHT}Chatbot: {Fore.RESET}{text}')

def takeCommand():
    global speak_enabled
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print(f'{Fore.YELLOW}{Style.BRIGHT}Listening...')
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en")
            print(f'{Fore.CYAN}{Style.BRIGHT}User Said: {Fore.RESET}{query}')
            if query.lower() == "i will type":
                speak_enabled = False
            elif query.lower() == "i will speak with you":
                speak_enabled = True
            return query.lower()
        except Exception as e:
            print(f'{Fore.RED}{Style.BRIGHT}Sorry, I didn\'t get that. Please try again.')
            return ""

def play_youtube_music(song_name):
    try:
        print(f'{Fore.GREEN}{Style.BRIGHT}Playing {song_name} from YouTube...')
        kit.playonyt(song_name)
        time.sleep(5)  # Wait for a few seconds for the video to start playing
    except Exception as e:
        print(f'{Fore.RED}{Style.BRIGHT}An error occurred while playing the song: {e}')

if __name__ == "__main__":
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)  # Adjust the volume (0.0 to 1.0)

    print(f'{Fore.BLUE}{Style.BRIGHT}PyCharm')
    speak("Hello, I am Chatbot AI, my name is Mithun")

    start_time = datetime.now()
    while True:
        query = takeCommand()

        if speak_enabled:
            # Check for commands to open specific websites
            if 'open' in query:
                website_name = query.split('open')[1].strip()
                speak(f'Opening {website_name}, sir...')
                webbrowser.open(f"https://www.{website_name}.com")

            # Check for command to play a YouTube song
            elif 'play' in query and 'song' in query:
                try:
                    song_start_index = query.find('play') + len('play')
                    song_end_index = query.find('song')
                    song_name = query[song_start_index:song_end_index].strip()
                    speak(f'Playing {song_name}...')
                    play_youtube_music(song_name)
                except Exception as e:
                    print(f'{Fore.RED}{Style.BRIGHT}An error occurred: {e}')

            # Exit the program if user says quit, exit, or bye
            elif any(keyword in query for keyword in ['quit', 'exit', 'bye']):
                speak('Goodbye, sir.')

                end_time = datetime.now()
                minutes_used = (end_time - start_time).seconds // 60
                print(f'{Fore.GREEN}{Style.BRIGHT}Session started at: {Fore.RESET}{start_time.strftime("%Y-%m-%d %H:%M:%S")}')
                print(f'{Fore.GREEN}{Style.BRIGHT}Session ended at: {Fore.RESET}{end_time.strftime("%Y-%m-%d %H:%M:%S")}')
                print(f'{Fore.GREEN}{Style.BRIGHT}Minutes used: {Fore.RESET}{minutes_used} min')
                break

    pygame.mixer.music.stop()
    pygame.quit()
