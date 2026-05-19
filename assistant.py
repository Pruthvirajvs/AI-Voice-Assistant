from __future__ import annotations

import datetime as dt
import importlib
import os
import random
import shutil
import subprocess
import time
import webbrowser
from pathlib import Path
from typing import Callable

import tkinter as tk
from tkinter import ttk

try:
    import requests
except ImportError:  # pragma: no cover - handled at runtime for fresh installs
    requests = None


def optional_import(package: str):
    try:
        return importlib.import_module(package)
    except ImportError:
        return None


pyttsx3 = optional_import("pyttsx3")
sr = optional_import("speech_recognition")
wikipedia = optional_import("wikipedia")
pyjokes = optional_import("pyjokes")
winshell = optional_import("winshell")
pyautogui = optional_import("pyautogui")
pytube = optional_import("pytube")
wolframalpha = optional_import("wolframalpha")

try:
    from ecapture import ecapture as ec
except ImportError:  # pragma: no cover
    ec = None

try:
    import ctypes
except ImportError:  # pragma: no cover
    ctypes = None


APP_TITLE = "Desktop Synchronize"
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Bengaluru")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
WOLFRAMALPHA_APP_ID = os.getenv("WOLFRAMALPHA_APP_ID", "")
MUSIC_DIR = Path(os.getenv("MUSIC_DIR", str(Path.home() / "Music")))
SCREENSHOT_DIR = Path(os.getenv("SCREENSHOT_DIR", str(Path.home() / "Pictures" / "Assistant Screenshots")))
DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", str(Path.home() / "Downloads")))
NOTES_FILE = Path(os.getenv("NOTES_FILE", "note.txt"))
MEMORY_FILE = Path(os.getenv("MEMORY_FILE", "data.txt"))


class Speaker:
    def __init__(self) -> None:
        self.engine = None
        if pyttsx3 is None:
            return

        try:
            self.engine = pyttsx3.init("sapi5")
            voices = self.engine.getProperty("voices")
            if len(voices) > 1:
                self.engine.setProperty("voice", voices[1].id)
            self.engine.setProperty("rate", 175)
        except Exception as exc:
            print(f"Text-to-speech unavailable: {exc}")
            self.engine = None

    def say(self, text: str) -> None:
        print(text)
        if self.engine is None:
            return
        self.engine.say(text)
        self.engine.runAndWait()


class VoiceAssistant:
    def __init__(self, status_var: tk.StringVar, root: tk.Tk) -> None:
        self.status_var = status_var
        self.root = root
        self.speaker = Speaker()
        self.user_name = "sir"
        self.assistant_name = ASSISTANT_NAME
        self.running = False

    def update_status(self, message: str) -> None:
        self.status_var.set(message)
        self.root.update_idletasks()

    def speak(self, text: str) -> None:
        self.update_status(text)
        self.speaker.say(text)

    def wish(self) -> None:
        hour = dt.datetime.now().hour
        self.speak("Welcome back sir.")

        if 4 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 16:
            greeting = "Good afternoon"
        elif 16 <= hour < 24:
            greeting = "Good evening"
        else:
            greeting = "Good night"

        self.speak(f"{greeting}, sir. {self.assistant_name} is at your service.")

    def listen(self) -> str:
        if sr is None:
            self.speak("Speech recognition is not installed. Please install the requirements first.")
            return ""

        self.update_status("Listening...")
        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                recognizer.pause_threshold = 0.7
                recognizer.adjust_for_ambient_noise(source, duration=0.4)
                audio = recognizer.listen(source)
        except Exception as exc:
            self.speak(f"Microphone error: {exc}")
            return ""

        try:
            self.update_status("Recognizing...")
            command = recognizer.recognize_google(audio, language="en-in")
            self.update_status(command)
            return command.lower().strip()
        except Exception:
            self.speak("I could not recognize that. Please try again.")
            return ""

    def ask(self, prompt: str) -> str:
        self.speak(prompt)
        return self.listen()

    def get_name(self) -> None:
        name = self.ask("Can I please know your name?")
        if name:
            self.user_name = name.title()
            self.speak(f"I am glad to know you, {self.user_name}. How can I help?")

    def weather(self, city_name: str) -> None:
        if requests is None:
            self.speak("The requests package is not installed.")
            return
        if not OPENWEATHER_API_KEY:
            self.speak("OpenWeather API key is missing. Add it to your environment first.")
            return

        params = {"appid": OPENWEATHER_API_KEY, "q": city_name, "units": "metric"}
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
        data = response.json()

        if str(data.get("cod")) == "404":
            self.speak("City not found.")
            return

        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        report = (
            f"Weather in {city_name}: {weather.get('description', 'not available')}. "
            f"Temperature {main.get('temp')} degrees Celsius, "
            f"humidity {main.get('humidity')} percent, "
            f"pressure {main.get('pressure')} hectopascals."
        )
        self.speak(report)

    def wolfram_answer(self, command: str) -> None:
        if wolframalpha is None:
            self.speak("WolframAlpha package is not installed.")
            return
        if not WOLFRAMALPHA_APP_ID:
            self.speak("WolframAlpha app ID is missing. Add it to your environment first.")
            return

        client = wolframalpha.Client(WOLFRAMALPHA_APP_ID)
        result = client.query(command)
        try:
            answer = next(result.results).text
        except StopIteration:
            self.speak("I could not find a result.")
            return
        self.speak(answer)

    def open_calculator(self) -> None:
        try:
            subprocess.Popen("calc.exe")
            self.speak("Calculator opened.")
        except FileNotFoundError:
            self.speak("Calculator app was not found on this system.")

    def open_office_app(self, executable: str, friendly_name: str) -> None:
        candidates = [
            Path("C:/Program Files/Microsoft Office/root/Office16") / executable,
            Path("C:/Program Files (x86)/Microsoft Office/root/Office16") / executable,
        ]
        for path in candidates:
            if path.exists():
                subprocess.Popen([str(path)])
                self.speak(f"{friendly_name} opened.")
                return
        self.speak(f"I could not find {friendly_name} on this computer.")

    def play_music(self) -> None:
        if not MUSIC_DIR.exists():
            self.speak(f"Music directory not found: {MUSIC_DIR}")
            return

        songs = [item for item in MUSIC_DIR.iterdir() if item.is_file()]
        if not songs:
            self.speak("No music files found.")
            return

        os.startfile(str(random.choice(songs)))
        self.speak("Enjoy the music.")

    def take_screenshot(self) -> None:
        if pyautogui is None:
            self.speak("PyAutoGUI is not installed.")
            return

        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        filename = SCREENSHOT_DIR / f"screenshot-{dt.datetime.now():%Y%m%d-%H%M%S}.png"
        pyautogui.screenshot().save(filename)
        self.speak(f"Screenshot saved to {filename}")

    def download_video(self) -> None:
        if pytube is None:
            self.speak("Pytube is not installed.")
            return

        url = self.ask("Please say or paste the YouTube video URL.")
        if not url.startswith("http"):
            self.speak("That does not look like a valid URL.")
            return

        video = pytube.YouTube(url).streams.get_highest_resolution()
        video.download(str(DOWNLOAD_DIR))
        self.speak("Video saved.")

    def calculate(self, operator_name: str, operation: Callable[[float, float], float]) -> None:
        first = self.ask("First number?")
        second = self.ask("Second number?")

        try:
            num1 = float(first)
            num2 = float(second)
            result = operation(num1, num2)
        except ZeroDivisionError:
            self.speak("Cannot divide by zero.")
            return
        except ValueError:
            self.speak("Sorry, I could not understand the numbers.")
            return

        self.speak(f"The result of {operator_name} is {result}.")

    def write_note(self) -> None:
        note = self.ask("What should I write?")
        if not note:
            return

        include_time = self.ask("Should I include date and time?")
        prefix = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} - " if "yes" in include_time or "sure" in include_time else ""
        NOTES_FILE.write_text(prefix + note, encoding="utf-8")
        self.speak("Note saved.")

    def remember(self) -> None:
        data = self.ask("What should I remember?")
        if data:
            MEMORY_FILE.write_text(data, encoding="utf-8")
            self.speak(f"I will remember that {data}.")

    def recall_memory(self) -> None:
        if not MEMORY_FILE.exists():
            self.speak("You have not asked me to remember anything yet.")
            return
        self.speak(f"You told me to remember that {MEMORY_FILE.read_text(encoding='utf-8')}.")

    def open_folder(self, folder: Path, label: str) -> None:
        if folder.exists():
            os.startfile(str(folder))
            self.speak(f"Opening {label}.")
        else:
            self.speak(f"{label} folder not found.")

    def shutdown(self, restart: bool = False) -> None:
        command = ["shutdown", "/r" if restart else "/s", "/f"]
        self.speak("Please confirm by saying yes.")
        if "yes" in self.listen():
            subprocess.call(command)
        else:
            self.speak("Cancelled.")

    def handle_command(self, command: str) -> None:
        if not command:
            return

        sites = {
            "open youtube": "https://youtube.com",
            "open google": "https://google.com",
            "open instagram": "https://instagram.com",
            "open whatsapp": "https://web.whatsapp.com",
            "open twitter": "https://twitter.com",
        }

        for phrase, url in sites.items():
            if phrase in command:
                webbrowser.open(url)
                self.speak(f"Opening {phrase.replace('open ', '')}.")
                return

        if self.assistant_name.lower() in command:
            self.wish()
        elif "how are you" in command:
            self.speak(f"I am fine, thank you. How are you, {self.user_name}?")
        elif "who are you" in command:
            self.speak("I am your virtual assistant.")
        elif "change my name" in command:
            self.get_name()
        elif "your name" in command or "what's your name" in command:
            self.speak(f"My name is {self.assistant_name}.")
        elif "time" in command:
            self.speak(f"The time is {dt.datetime.now():%I:%M:%S %p}.")
        elif "wikipedia" in command:
            self.search_wikipedia()
        elif "play music" in command or "play song" in command:
            self.play_music()
        elif "joke" in command:
            self.speak(pyjokes.get_joke() if pyjokes else "Install pyjokes to hear jokes.")
        elif "weather" in command:
            city = self.ask("Please tell me your city name.") or DEFAULT_CITY
            self.weather(city)
        elif command.startswith("what is") or command.startswith("who is"):
            self.wolfram_answer(command)
        elif "search" in command:
            query = command.replace("search", "", 1).strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            self.speak("Searching the web.")
        elif "remember that" in command:
            self.remember()
        elif "do you remember" in command:
            self.recall_memory()
        elif "stop listening" in command or "don't listen" in command:
            self.pause_listening()
        elif "camera" in command or "take a photo" in command:
            self.capture_photo()
        elif "shutdown" in command:
            self.shutdown(restart=False)
        elif "restart" in command:
            self.shutdown(restart=True)
        elif "sleep mode" in command:
            self.speak("Putting the computer into sleep mode.")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif "download video" in command:
            self.download_video()
        elif "take screenshot" in command:
            self.take_screenshot()
        elif "calculator" in command:
            self.open_calculator()
        elif "add" in command or "addition" in command:
            self.calculate("addition", lambda a, b: a + b)
        elif "sub" in command or "subtraction" in command:
            self.calculate("subtraction", lambda a, b: a - b)
        elif "mul" in command or "multiplication" in command:
            self.calculate("multiplication", lambda a, b: a * b)
        elif "div" in command or "division" in command:
            self.calculate("division", lambda a, b: a / b)
        elif "ms word" in command:
            self.open_office_app("WINWORD.EXE", "Microsoft Word")
        elif "powerpoint" in command:
            self.open_office_app("POWERPNT.EXE", "Microsoft PowerPoint")
        elif "empty recycle bin" in command:
            if winshell:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                self.speak("Recycle bin emptied.")
            else:
                self.speak("Winshell is not installed.")
        elif "lock window" in command or "lock windows" in command:
            if ctypes:
                ctypes.windll.user32.LockWorkStation()
            else:
                self.speak("Lock workstation is not available.")
        elif "write a note" in command:
            self.write_note()
        elif "open c drive" in command:
            self.open_folder(Path("C:/"), "C drive")
        elif "open d drive" in command:
            self.open_folder(Path("D:/"), "D drive")
        elif "open documents" in command:
            self.open_folder(Path.home() / "Documents", "Documents")
        elif "open downloads" in command:
            self.open_folder(Path.home() / "Downloads", "Downloads")
        elif "open pictures" in command:
            self.open_folder(Path.home() / "Pictures", "Pictures")
        elif "exit" in command or "stop assistant" in command:
            self.speak("Exiting Jarvis. Goodbye.")
            self.running = False
            self.root.quit()
        else:
            self.speak("Sorry, I am not able to understand you.")

    def search_wikipedia(self) -> None:
        if wikipedia is None:
            self.speak("Wikipedia package is not installed.")
            return

        query = self.ask("What do you want to search on Wikipedia?")
        if not query:
            return

        try:
            result = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia.")
            self.speak(result)
        except wikipedia.exceptions.DisambiguationError:
            self.speak("Please be more specific. I found multiple results.")
        except wikipedia.exceptions.PageError:
            self.speak("I could not find a matching result.")

    def pause_listening(self) -> None:
        timeout = self.ask("For how many seconds should I stop listening?")
        try:
            seconds = int(timeout)
        except ValueError:
            self.speak("I did not understand the duration.")
            return
        self.speak(f"I will stop listening for {seconds} seconds.")
        time.sleep(seconds)
        self.speak("I am listening again.")

    def capture_photo(self) -> None:
        if ec is None:
            self.speak("Camera capture package is not installed.")
            return
        ec.capture(0, "Assistant Camera", "img.jpg")
        self.speak("Photo captured.")

    def run(self) -> None:
        if self.running:
            return
        self.running = True
        os.system("cls")
        self.wish()
        self.get_name()

        while self.running:
            command = self.listen()
            self.handle_command(command)


def build_window() -> tk.Tk:
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("760x360")
    root.resizable(False, False)

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background="#101820")
    style.configure("Title.TLabel", background="#101820", foreground="#f4f7fb", font=("Segoe UI", 20, "bold"))
    style.configure("Status.TLabel", background="#101820", foreground="#9fb0c3", font=("Consolas", 13))
    style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"), padding=10)

    frame = ttk.Frame(root, padding=32)
    frame.pack(fill="both", expand=True)

    status_var = tk.StringVar(value="Click Start and speak your command.")
    assistant = VoiceAssistant(status_var, root)

    ttk.Label(frame, text="Welcome. Meet your Personal Assistant", style="Title.TLabel").pack(pady=(8, 30))
    ttk.Button(frame, text="Start", style="Accent.TButton", command=assistant.run).pack(pady=8)
    ttk.Label(frame, textvariable=status_var, style="Status.TLabel", wraplength=660, justify="center").pack(pady=(42, 0))

    return root


if __name__ == "__main__":
    window = build_window()
    window.mainloop()
