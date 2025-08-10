import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import json
import webbrowser
import pywhatkit
import wikipedia
import os
import traceback
import requests
from gtts import gTTS
import pygame

# === Setup ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "<YOUR_GROQ_API_KEY>"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
NEWS_API_KEY = os.getenv("NEWS_API_KEY") or "<YOUR_NEWS_API_KEY>"

# === Text-to-Speech Setup ===
def speak(text):
    update_chat("Buddy", text)
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        print("TTS Error:", e)

# === GUI Update ===
def update_chat(sender, message):
    def insert():
        chat_area.configure(state='normal')
        chat_area.insert(tk.END, f"{sender}: {message}\n")
        chat_area.configure(state='disabled')
        chat_area.see(tk.END)
    chat_area.after(0, insert)

# === Listen from Microphone ===
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_chat("System", "Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        except Exception as e:
            update_chat("System", f"Microphone error: {e}")
            return ""
    try:
        command = recognizer.recognize_google(audio)
        update_chat("You", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Network error.")
    return ""

# === GPT Interaction (Groq) ===
def ai_process(command):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant like Jarvis."},
            {"role": "user", "content": command}
        ]
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("AI Error:", e)
        speak("AI error.")
        return ""

# === Command Handling ===
def handle_command(command):
    if "add task" in command:
        add_task()
    elif "show tasks" in command:
        show_tasks()
    elif "summarize" in command or "daily summary" in command:
        daily_summary()
    elif "open" in command:
        launch_website(command)
    elif "search" in command:
        smart_search(command.replace("search", ""))
    elif "note" in command or "record" in command:
        record_note()
    elif "news" in command:
        get_news()
    elif command.startswith("play "):
        play_song(command)
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        root.after(1000, root.destroy)
    else:
        output = ai_process(command)
        speak(output)

def play_song(command):
    song = command.replace("play", "").strip()
    speak(f"Playing {song} on YouTube")
    pywhatkit.playonyt(song)

def launch_website(command):
    sites = {
        "gmail": "https://mail.google.com",
        "youtube": "https://youtube.com",
        "google docs": "https://docs.google.com",
        "notion": "https://notion.so",
        "google": "https://google.com",
        "facebook": "https://facebook.com",
        "linkedin": "https://linkedin.com"
    }
    for site in sites:
        if site in command:
            speak(f"Opening {site}")
            webbrowser.open(sites[site])
            return
    speak("Website not found.")

def smart_search(command):
    if "youtube" in command:
        speak("Searching YouTube...")
        pywhatkit.playonyt(command.replace("youtube", ""))
    elif "wikipedia" in command:
        speak("Searching Wikipedia...")
        try:
            result = wikipedia.summary(command, sentences=2)
            speak(result)
        except:
            speak("Sorry, no result found on Wikipedia.")
    else:
        speak("Searching Google...")
        webbrowser.open(f"https://www.google.com/search?q={command}")

# === Task Management ===
def add_task():
    speak("What is the task?")
    task = listen()
    speak("At what time?")
    time = listen()
    if not task or not time:
        speak("Task or time not recognized.")
        return
    task_data = {"task": task, "time": time}
    tasks = []
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            try:
                tasks = json.load(f)
            except:
                tasks = []
    tasks.append(task_data)
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)
    speak(f"Task '{task}' at {time} added.")

def show_tasks():
    if not os.path.exists("tasks.json"):
        speak("You have no tasks.")
        return
    with open("tasks.json", "r") as f:
        try:
            tasks = json.load(f)
        except:
            speak("Error reading tasks.")
            return
        if not tasks:
            speak("No tasks found.")
            return
        for task in tasks:
            speak(f"{task['task']} at {task['time']}")

# === Notes ===
def record_note():
    speak("Please speak your note.")
    note = listen()
    if note:
        with open("notes.txt", "a") as f:
            f.write(note + "\n")
        speak("Note saved.")
        try:
            summary = ai_process(f"Summarize this: {note}")
            speak("Summary: " + summary)
        except:
            speak("Could not summarize the note.")

# === Daily Summary ===
def daily_summary():
    tasks_summary = "No tasks for today."
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            try:
                task_list = json.load(f)
                if task_list:
                    tasks_summary = ". ".join([f"{t['task']} at {t['time']}" for t in task_list])
            except:
                pass
    fake_news = "OpenAI released new updates."
    weather = "Today is sunny."
    prompt = f"Summarize my day. Tasks: {tasks_summary}. News: {fake_news}. Weather: {weather}"
    try:
        summary = ai_process(prompt)
        speak("Here's your summary:")
        speak(summary)
    except:
        speak("Could not summarize your day.")

# === News ===
def get_news():
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
        data = r.json()
        for article in data.get("articles", [])[:5]:
            speak(article['title'])
    except Exception as e:
        speak("News fetch failed.")

# === GUI Setup ===
def start_listening():
    threading.Thread(target=listen_and_respond, daemon=True).start()

def listen_and_respond():
    speak("Listening...")
    command = listen()
    if command:
        handle_command(command)

def launch_gui():
    global root, chat_area
    try:
        root = tk.Tk()
        root.title("🎙️ Buddy – Voice Assistant")
        root.geometry("520x650")
        root.config(bg="#2E3440")

        title = tk.Label(
            root,
            text="🎙️ Buddy – Voice Assistant",
            font=("Segoe UI", 22, "bold"),
            bg="#2E3440",
            fg="#88C0D0"
        )
        title.pack(pady=(20, 10))

        chat_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            width=58,
            height=25,
            font=("Segoe UI", 11),
            bg="#3B4252",
            fg="#ECEFF4",
            insertbackground="#ECEFF4",
            borderwidth=0
        )
        chat_area.pack(padx=20, pady=10)
        chat_area.configure(state='disabled')

        def on_enter(e): mic_button.config(bg="#5E81AC")
        def on_leave(e): mic_button.config(bg="#4C566A")

        mic_button = tk.Button(
            root,
            text="🎤 Speak",
            font=("Segoe UI", 14, "bold"),
            bg="#4C566A",
            fg="white",
            activebackground="#5E81AC",
            padx=30,
            pady=12,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=start_listening
        )
        mic_button.pack(pady=20)
        mic_button.bind("<Enter>", on_enter)
        mic_button.bind("<Leave>", on_leave)

        root.after(1000, lambda: speak("Initializing Buddy..."))
        root.mainloop()
    except Exception as e:
        print("GUI Launch Error:", e)

# === Main Execution Block ===
if __name__ == "__main__":
    print("Launching Buddy GUI...")
    launch_gui()
