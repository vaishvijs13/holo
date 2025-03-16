import pyttsx3
import speech_recognition as sr
import webbrowser
import sys

engine = pyttsx3.init() # text to speech engine
engine.setProperty("rate", 190)

def recspoken():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Tutorial?")
        engine.say("Tutorial?")
        engine.runAndWait()

        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Couldn't understand audio")
            engine.say("I didn't understand, please try again")
        except sr.RequestError:
            print("Could not connect to SR api")
            engine.say("There was an error processing your request")
        except Exception as e:
            print(f"Error: {e}")
            engine.say("An unexpected error occurred.")

        engine.runAndWait()
        return None

def search(command):
    if "exit" in command:
        print("Exiting program")
        engine.say("Goodbye!")
        engine.runAndWait()
        sys.exit()

    query = command.replace("search", "").strip()
    gURL = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    print(f"Searching Google for: {query}")
    engine.say(f"Searching the web for {query}")
    engine.runAndWait()

    webbrowser.open(gURL)

if __name__ == "__main__":
    while True:
        given_command = recspoken()
        if given_command:
            search(given_command)
