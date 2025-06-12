import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import json
import os
import webbrowser
import pygame
import subprocess

# === TTS Setup ===
engine = pyttsx3.init()

def speak(text):
    update_chat("Buddy", text)
    engine.say(text)
    engine.runAndWait()

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
    except:
        speak("Sorry, I didn't catch that.")
        return ""

# === Command Handler ===
def handle_command(command):
    if "add task" in command:
        add_task()
    elif "show tasks" in command:
        show_tasks()
    elif "note" in command or "record" in command:
        record_note()
    elif "open" in command:
        launch_app_or_website(command)
    elif "play music" in command:
        play_music()
    elif "shutdown" in command:
        speak("Shutting down...")
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting system...")
        os.system("shutdown /r /t 1")
    elif "lock" in command:
        speak("Locking system...")
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        root.after(1000, root.destroy)
    else:
        speak("Sorry, I can't do that offline.")

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

# === Open App or Website ===
def launch_app_or_website(command):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "cmd": "cmd.exe",
    }
    websites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "gmail": "https://mail.google.com",
        "facebook": "https://facebook.com"
    }
    for app in apps:
        if app in command:
            speak(f"Opening {app}")
            subprocess.Popen(apps[app])
            return
    for site in websites:
        if site in command:
            speak(f"Opening {site}")
            webbrowser.open(websites[site])
            return
    speak("Application or website not recognized.")

# === Music Playback ===
def play_music():
    music_folder = "music"
    if not os.path.exists(music_folder):
        speak("Music folder not found.")
        return
    files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
    if not files:
        speak("No music files found.")
        return
    speak("Playing music...")
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(music_folder, files[0]))
    pygame.mixer.music.play()

# === Listening Trigger ===
def start_listening():
    threading.Thread(target=listen_and_respond, daemon=True).start()

def listen_and_respond():
    command = listen()
    if command:
        handle_command(command)

# === GUI Setup ===
def launch_gui():
    global root, chat_area
    root = tk.Tk()
    root.title("🎙️ Buddy – Offline Assistant")
    root.geometry("520x650")
    root.config(bg="#2E3440")

    title = tk.Label(
        root,
        text="🎙️ Buddy – Offline Assistant",
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

    root.after(1000, lambda: speak("Buddy is ready, fully offline."))
    root.mainloop()

# === Run the Assistant ===
if __name__ == "__main__":
    launch_gui()
