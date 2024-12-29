import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pyjokes
import smtplib

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Helper functions
def speak(audio):
    """Speak the given text."""
    engine.say(audio)
    engine.runAndWait()

def wish_user():
    """Wish the user based on the time of the day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How can I assist you today?")

def take_command():
    """Listen to the user command and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Could you please say that again?")
        return None
    return query.lower()

def send_email(to, content):
    """Send an email using Gmail's SMTP server."""
    sender_email = "nehasharma482002@gmail.com"
    sender_password = "your_password"
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, content)
        server.close()
        speak("Email has been sent.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")

# Main function
def main():
    wish_user()
    while True:
        query = take_command()

        if query is None:
            continue

        # Commands
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "").strip()
            if query:  # Check if query is not empty
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                except Exception as e:
                    speak("Sorry, I couldn't fetch the information from Wikipedia. Please try again.")
                    print(e)
            else:
                speak("It seems you didn't specify a topic to search on Wikipedia.")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")

        elif 'time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = take_command()
                speak("To whom should I send the email?")
                recipient = take_command()
                send_email(recipient, content)
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day!")
            break

        else:
            speak("Searching in Google")
            webbrowser.open(f"https://www.google.com/search?q={query}")

if __name__ == "__main__":
    main()
