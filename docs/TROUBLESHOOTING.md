# Troubleshooting

Use this guide when setting up or running the AI Voice Assistant on Windows.

## Python Command Not Found

Install Python 3.10 or newer from the official Python website. During installation, enable **Add Python to PATH**.

Check the installation:

```powershell
python --version
pip --version
```

## Virtual Environment Activation Fails

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## PyAudio Installation Fails

`pyaudio` can be difficult to install on Windows. Try:

```powershell
python -m pip install pipwin
pipwin install pyaudio
```

If that does not work, install a compatible wheel file for your Python version.

## Microphone Not Detected

1. Open Windows Settings.
2. Go to Privacy & security > Microphone.
3. Allow microphone access.
4. Make sure your active input device is selected.
5. Restart the assistant.

## Speech Recognition Is Slow or Fails

- Check your internet connection.
- Speak clearly near the microphone.
- Reduce background noise.
- Try another microphone if available.

## Text-to-Speech Does Not Work

The project uses Windows SAPI5 through `pyttsx3`.

Try reinstalling:

```powershell
pip uninstall pyttsx3
pip install pyttsx3
```

Also check Windows voice settings and installed voices.

## Weather or WolframAlpha Does Not Work

These features require API keys. Set them as environment variables:

```powershell
$env:OPENWEATHER_API_KEY="your-openweather-key"
$env:WOLFRAMALPHA_APP_ID="your-wolframalpha-app-id"
```

Do not commit real API keys to GitHub.

## Windows App Commands Do Not Open

Some commands depend on installed Windows apps or local paths. Check that the application exists on your system. Microsoft Office paths may differ between computers.

## Screenshot Folder Not Found

The assistant creates the screenshot folder automatically. You can override the location with:

```powershell
$env:SCREENSHOT_DIR="C:\Users\YourName\Pictures\Assistant Screenshots"
```
