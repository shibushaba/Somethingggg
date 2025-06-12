import json
import os
import subprocess
import webbrowser

def speak(text):
    return text  # For web, we return instead of speaking out loud

def handle_command(command):
    command = command.lower()

    if "add task" in command:
        return add_task(command)
    elif "show tasks" in command:
        return show_tasks()
    elif "note" in command or "record" in command:
        return record_note(command)
    elif "open" in command:
        return launch_app_or_website(command)
    elif "play music" in command:
        return play_music()
    elif "shutdown" in command:
        return "Cannot shut down from web version."
    elif "exit" in command or "stop" in command:
        return "Goodbye!"
    else:
        return "Sorry, I can't do that offline in the web version."

def add_task(command):
    try:
        parts = command.split(" at ")
        task = parts[0].replace("add task", "").strip()
        time = parts[1].strip()
    except:
        return "Please use format: Add task [task] at [time]."

    task_data = {"task": task, "time": time}
    tasks = []
    if os.path.exists("data/tasks.json"):
        with open("data/tasks.json", "r") as f:
            try:
                tasks = json.load(f)
            except:
                tasks = []
    tasks.append(task_data)
    with open("data/tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)
    return f"Task '{task}' at {time} added."

def show_tasks():
    if not os.path.exists("data/tasks.json"):
        return "You have no tasks."
    with open("data/tasks.json", "r") as f:
        try:
            tasks = json.load(f)
        except:
            return "Error reading tasks."
    if not tasks:
        return "No tasks found."
    return "<br>".join([f"{t['task']} at {t['time']}" for t in tasks])

def record_note(command):
    note = command.replace("note", "").replace("record", "").strip()
    if not note:
        return "No note detected."
    with open("data/notes.txt", "a") as f:
        f.write(note + "\n")
    return "Note saved."

def launch_app_or_website(command):
    websites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "gmail": "https://mail.google.com",
        "facebook": "https://facebook.com"
    }
    for site in websites:
        if site in command:
            webbrowser.open(websites[site])
            return f"Opening {site}."
    return "Website not recognized."

def play_music():
    folder = "music"
    if not os.path.exists(folder):
        return "Music folder not found."
    files = [f for f in os.listdir(folder) if f.endswith(".mp3")]
    if not files:
        return "No music files found."
    return f"Playing {files[0]} (please open manually)."
