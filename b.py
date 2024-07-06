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
    print(f'{Back.BLACK}{Fore.YELLOW}{Style.BRIGHT}Chatbot: {Fore.RESET}{Back.BLACK}{Fore.YELLOW}{text}{Style.RESET_ALL}')

def takeCommand():
    global speak_enabled
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print(f'{Back.BLACK}{Fore.MAGENTA}{Style.BRIGHT}Listening...{Style.RESET_ALL}')
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en")
            print(f'{Back.BLACK}{Fore.CYAN}{Style.BRIGHT}User Said: {Fore.RESET}{Back.BLACK}{Fore.CYAN}{query}{Style.RESET_ALL}')
            if query.lower() == "i will type":
                speak_enabled = False
            elif query.lower() == "i will speak with you":
                speak_enabled = True
            return query.lower()
        except Exception as e:
            print(f'{Back.BLACK}{Fore.RED}{Style.BRIGHT}Sorry, I didn\'t get that. Please try again.{Style.RESET_ALL}')
            print()  # Line gap after error message
            return ""

def play_youtube_music(song_name):
    try:
        print(f'{Back.BLACK}{Fore.GREEN}{Style.BRIGHT}Playing {song_name} from YouTube...{Style.RESET_ALL}')
        kit.playonyt(song_name)
        print(f'{Back.BLACK}{Fore.GREEN}{Style.BRIGHT}YouTube video should be opening now.{Style.RESET_ALL}')
        time.sleep(5)  # Wait for a few seconds for the video to start playing
    except Exception as e:
        print(f'{Back.BLACK}{Fore.RED}{Style.BRIGHT}An error occurred while playing the song: {e}{Style.RESET_ALL}')
        print()  # Line gap after error message

if __name__ == "__main__":
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)  # Adjust the volume (0.0 to 1.0)

    print(f'{Back.BLACK}{Fore.BLUE}{Style.BRIGHT}PyCharm{Style.RESET_ALL}')
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
                    print()  # Line gap after playing song message
                except Exception as e:
                    print(f'{Back.BLACK}{Fore.RED}{Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}')
                    print()  # Line gap after error message

            # Exit the program if user says quit, exit, or bye
            elif any(keyword in query for keyword in ['quit', 'exit', 'bye']):
                speak('Goodbye, sir.')

                end_time = datetime.now()
                minutes_used = (end_time - start_time).seconds // 60
                print(f'{Back.BLACK}{Fore.GREEN}{Style.BRIGHT}Session started at: {Fore.RESET}{Back.BLACK}{Fore.GREEN}{start_time.strftime("%Y-%m-%d %H:%M:%S")}{Style.RESET_ALL}')
                print(f'{Back.BLACK}{Fore.GREEN}{Style.BRIGHT}Session ended at: {Fore.RESET}{Back.BLACK}{Fore.GREEN}{end_time.strftime("%Y-%m-%d %H:%M:%S")}{Style.RESET_ALL}')
                print(f'{Back.BLACK}{Fore.GREEN}{Style.BRIGHT}Minutes used: {Fore.RESET}{Back.BLACK}{Fore.GREEN}{minutes_used} min{Style.RESET_ALL}')
                break

    pygame.mixer.music.stop()
    pygame.quit()
