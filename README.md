# AI Voice Assistant

A Windows desktop voice assistant built with Python. It listens to voice commands, speaks responses, opens apps and websites, answers basic questions, checks weather, takes notes, captures screenshots, and handles simple desktop automation.

The repository also includes a polished static showcase page for presenting the project professionally on GitHub.

## Project Background

This project was developed as an academic Python application by Pruthviraj, an MCA graduate with hands-on experience in Python, Java, MySQL, and web technologies. The assistant focuses on practical Windows automation through speech commands, combining voice recognition, text-to-speech, browser control, file actions, calculations, notes, weather updates, and desktop utilities.

The goal is to demonstrate problem-solving, application development, and user-focused automation skills in a complete, recruiter-friendly GitHub project.

## Features

- Voice input using `SpeechRecognition`
- Text-to-speech output using `pyttsx3` and Windows SAPI5
- Wikipedia summaries
- Weather reports using OpenWeather
- WolframAlpha question answering
- Web shortcuts for Google, YouTube, Instagram, WhatsApp, and Twitter
- Music playback from a configurable folder
- Notes and memory commands
- Screenshot capture
- Calculator, Microsoft Word, and PowerPoint launch commands
- Windows actions such as lock, sleep, shutdown, restart, and recycle bin cleanup
- Clean Tkinter desktop interface

## Tech Stack

- **Language:** Python
- **UI:** Tkinter
- **Voice input:** SpeechRecognition
- **Speech output:** pyttsx3
- **Automation:** os, subprocess, webbrowser, pyautogui, winshell
- **APIs:** OpenWeather, WolframAlpha, Wikipedia
- **Frontend showcase:** HTML, CSS, JavaScript

## Major Project Blueprints

This repository also includes 6 larger portfolio project blueprints that can be built next to strengthen a software engineering profile:

1. AI Voice Assistant Pro
2. Smart Student Attendance Management System
3. E-Commerce Product Management Platform
4. Cybersecurity Log Analyzer Dashboard
5. Personal Portfolio and Resume Builder
6. Smart Expense Tracker with Analytics

See [docs/MAJOR_PROJECTS.md](docs/MAJOR_PROJECTS.md) for feature plans, suggested tech stacks, and portfolio positioning.

## Project Structure

| File | Purpose |
| --- | --- |
| `assistant.py` | Main Python desktop assistant |
| `requirements.txt` | Python dependencies |
| `.env.example` | Safe example configuration for API keys and local paths |
| `index.html` | Static project showcase page |
| `styles.css` | Showcase page styling |
| `script.js` | Showcase page demo interaction |
| `docs/COMMANDS.md` | Supported voice commands |
| `docs/MAJOR_PROJECTS.md` | Larger portfolio project blueprints |
| `docs/PROFILE.md` | Developer and resume-based project context |
| `docs/ROADMAP.md` | Future improvement roadmap |

## Requirements

- Windows 10 or Windows 11
- Python 3.10+
- Working microphone
- Internet connection for speech recognition, weather, Wikipedia, and WolframAlpha features

Some packages are Windows-specific, especially `pyttsx3` with SAPI5, `winshell`, and `pywin32`.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Set environment variables for optional API features:

```powershell
$env:OPENWEATHER_API_KEY="your-openweather-key"
$env:WOLFRAMALPHA_APP_ID="your-wolframalpha-app-id"
```

You can also copy `.env.example` as a reference when configuring your local machine. Real keys should stay out of GitHub.

## Run

```powershell
python assistant.py
```

Click **Start**, say your name, and then speak a command such as:

```text
open youtube
weather
take screenshot
write a note
calculator
```

## Developer Profile

Pruthviraj is an MCA graduate with a strong foundation in Python, Java, MySQL, HTML, CSS, JavaScript, object-oriented programming, and problem solving. He has completed a Java Full Stack Development internship and has experience building academic and practical software projects.

More profile context is available in [docs/PROFILE.md](docs/PROFILE.md).

LinkedIn: [Pruthvi Raj](https://www.linkedin.com/in/pruthvi-raj-344aa8254)

## Security Notes

API keys were intentionally not committed. If an API key has ever been shared publicly, rotate it from the provider dashboard before using it again.

Potentially sensitive commands like shutdown and restart ask for confirmation before running.

## Showcase Page

Open `index.html` in a browser to view the professional project presentation page.

## License

MIT License. See [LICENSE](LICENSE).
