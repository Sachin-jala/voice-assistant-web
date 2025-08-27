import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import pyjokes
import webbrowser
import sys
import smtplib
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 = male, 1 = female
engine.setProperty('rate', 170)

# Volume setup (using pycaw)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def talk(text):
    """Speak out text"""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for user command"""
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎙️ Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5, phrase_time_limit=8)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"👉 You said: {command}")
            return command
    except Exception:
        return ""

def send_email(receiver, subject, message):
    """Send email using Gmail"""
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # Gmail App Password required

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, receiver, email)
        server.quit()
        talk("Email has been sent successfully.")
    except Exception as e:
        print(e)
        talk("Sorry, I could not send the email.")

def run_assistant():
    """Main assistant logic"""
    command = take_command()

    if "play" in command:
        song = command.replace("play", "")
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        talk("Current time is " + current_time)

    elif "date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        talk("Today's date is " + today)

    elif "who is" in command or "what is" in command:
        person = command.replace("who is", "").replace("what is", "")
        info = wikipedia.summary(person, 1)
        talk(info)

    elif "open notepad" in command:
        talk("Opening Notepad")
        os.system("notepad.exe")

    elif "open chrome" in command:
        talk("Opening Google Chrome")
        os.system("start chrome")

    elif "open youtube" in command:
        talk("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in command:
        talk("Opening Google")
        webbrowser.open("https://google.com")

    elif "search" in command:
        query = command.replace("search", "")
        talk("Here is what I found on Google")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        talk(joke)

    # WhatsApp message
    elif "send whatsapp" in command:
        talk("Who should I send the message to?")
        contact = take_command()
        talk("What is the message?")
        message = take_command()
        talk(f"Sending WhatsApp message to {contact}")
        # Example number (replace with your own)
        pywhatkit.sendwhatmsg_instantly("+911234567890", message, 15, True, 2)

    # Email sending
    elif "send email" in command:
        talk("Please tell me the receiver email address")
        receiver = take_command()
        talk("What is the subject?")
        subject = take_command()
        talk("What is the message?")
        message = take_command()
        send_email(receiver, subject, message)

    # 🔊 Volume control
    elif "increase volume" in command:
        talk("Increasing volume")
        volume.SetMasterVolumeLevelScalar(min(volume.GetMasterVolumeLevelScalar() + 0.1, 1.0), None)

    elif "decrease volume" in command:
        talk("Decreasing volume")
        volume.SetMasterVolumeLevelScalar(max(volume.GetMasterVolumeLevelScalar() - 0.1, 0.0), None)

    elif "mute" in command:
        talk("Muting volume")
        volume.SetMute(1, None)

    elif "unmute" in command:
        talk("Unmuting volume")
        volume.SetMute(0, None)

    # 💡 Brightness control
    elif "increase brightness" in command:
        current = sbc.get_brightness(display=0)[0]
        new_brightness = min(current + 20, 100)
        sbc.set_brightness(new_brightness)
        talk(f"Brightness increased to {new_brightness} percent")

    elif "decrease brightness" in command:
        current = sbc.get_brightness(display=0)[0]
        new_brightness = max(current - 20, 10)
        sbc.set_brightness(new_brightness)
        talk(f"Brightness decreased to {new_brightness} percent")

    elif "set brightness" in command:
        try:
            level = int(''.join([c for c in command if c.isdigit()]))
            sbc.set_brightness(level)
            talk(f"Brightness set to {level} percent")
        except:
            talk("Please say a number for brightness level")

    # System controls
    elif "shutdown" in command:
        talk("Shutting down your system, goodbye!")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        talk("Restarting your system, please wait.")
        os.system("shutdown /r /t 5")

    elif "bye" in command or "stop" in command or "exit" in command:
        talk("Goodbye! Have a great day.")
        sys.exit()

    else:
        talk("Sorry, I didn’t understand. Please say it again.")

# Run the assistant in loop
if __name__ == "__main__":
    talk("Hi, I am your advanced smart assistant. How can I help you?")
    while True:
        run_assistant()
