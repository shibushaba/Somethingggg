import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import webbrowser
import pywhatkit
import wikipedia
import os
import requests
from gtts import gTTS
import pygame
import datetime
import time
import random
import json
from dotenv import load_dotenv
import threading

# Initialize pygame mixer
pygame.mixer.init()

# === GUI Setup ===
root = tk.Tk()
root.title("Buddy Voice Assistant")
root.geometry("600x700")
root.configure(bg="#1e1e1e")

# Chat display
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    width=70,
    height=25,
    font=("Arial", 12),
    bg="#252526",
    fg="white",
    insertbackground="white"
)
chat_area.pack(pady=10)
chat_area.configure(state='disabled')

# Microphone button
mic_button = tk.Button(
    root,
    text="🎤 Push to Talk",
    font=("Arial", 14, "bold"),
    bg="#007acc",
    fg="white",
    command=lambda: threading.Thread(target=listen_and_respond).start()
)
mic_button.pack(pady=10)

# === Voice Functions ===
def speak(text):
    update_chat("Buddy", text)
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print("TTS Error:", e)

def update_chat(sender, message):
    chat_area.configure(state='normal')
    chat_area.insert(tk.END, f"{sender}: {message}\n")
    chat_area.configure(state='disabled')
    chat_area.see(tk.END)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_chat("System", "Listening...")
        audio = r.listen(source)
    
    try:
        command = r.recognize_google(audio).lower()
        update_chat("You", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Network error.")
    return ""

# === Smart Features ===
def handle_command(command):
    if "hello" in command:
        speak("Hello! How can I help you?")
    elif "time" in command:
        speak(f"It's {datetime.datetime.now().strftime('%H:%M')}")
    elif "date" in command:
        speak(f"Today is {datetime.datetime.now().strftime('%B %d, %Y')}")
    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://google.com/search?q={query}")
        speak(f"Searching for {query}")
    elif "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia: {summary}")
        except:
            speak("Sorry, no Wikipedia results found.")
    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
    elif "joke" in command:
        jokes = [
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call fake spaghetti? An impasta!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ]
        speak(random.choice(jokes))
    elif "exit" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        root.after(1000, root.destroy)
    else:
        speak("I didn't understand. Can you repeat?")

def listen_and_respond():
    command = listen()
    if command:
        handle_command(command)

# === Run the App ===
if __name__ == "__main__":
    speak("Buddy assistant activated. How can I help you?")
    root.mainloop()