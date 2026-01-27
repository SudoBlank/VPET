# Voice Interaction Feature - Installation & Usage Guide

## Overview
The VPET application now includes a press-to-hold voice interaction system where you can:
- **Hold Alt+V** to record your voice
- **Release** to send the message
- **Pet responds** in a cute Japanese female voice (with content in any language)

## Installation

### Optional Installation (Voice Features)
Voice features are **optional**. The app runs fine without them, but voice input/output won't be available.

### Step 1: Install Required Packages (Optional)
To enable voice features, install the voice packages:

```bash
pip install SpeechRecognition pynput
```

For full voice support with PyAudio (microphone input):
```bash
pip install pyaudio
```

**Note:** PyAudio can be tricky to install on Windows. If you skip it, voice input won't work but you can still use the chat feature.

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 2: Verify Installation (Optional)
Test voice features in Python:
```python
python -c "import speech_recognition; print('Speech Recognition OK')"
python -c "import edge_tts; print('Edge TTS OK')"
python -c "import pynput; print('Pynput OK')"
```

If any fail, that feature won't be available but app will still run.

### What Each Package Does:
- **SpeechRecognition**: Converts your voice to text using Google's speech API (free, no key needed)
- **edge-tts**: Microsoft's text-to-speech engine with Japanese voice support (free)
- **pynput**: Monitors keyboard globally to detect Alt+V keybind
- **PyAudio**: (Optional) Low-level audio input - required for microphone recording

## Graceful Degradation

The app is designed to work with or without voice features:

✅ **App runs without voice packages** - Core functionality works  
✅ **Voice input disabled if PyAudio missing** - Shows message in console  
✅ **Voice output disabled if edge-tts missing** - Shows message in console  
✅ **Keyboard listener fails gracefully** - App continues without hotkey  

If any voice component is missing:
- Settings still show voice option
- Voice toggle can be checked but won't work
- Console shows which features are disabled
- App continues running normally without voice

## How to Use

### Basic Voice Chat
1. **Open Settings** (right-click on pet → Settings)
2. **Check "Enable voice input"** checkbox
3. **Press and hold Alt+V** on your keyboard
4. **Speak clearly** into your microphone
5. **Release Alt+V** when done
6. **Pet responds** with voice in Japanese female voice

### Visual Feedback
- **Yellow outline** appears around pet while you're recording
- Pet automatically answers your question
- Response plays in Japanese female voice

### Customization
In the Settings window:
- **Toggle Voice Input**: Enable/disable the voice feature
- **Language**: Content is spoken in Japanese but understands any language you speak
- **Keybind**: Default is Alt+V (press Alt and hold V)

## Troubleshooting

### "No sound is playing"
- Check your speakers/volume are on
- Windows may show a speaker notification when audio plays
- Check the `temp_voice.mp3` file is created in the app folder

### "Can't hear what I'm saying"
- Make sure your **microphone is connected and working**
- Test microphone in Windows Settings
- Grant microphone permission to Python if prompted

### "No response from pet"
- Check **AI is enabled** in settings
- Verify **voice_enabled** is True in settings
- Check your **internet connection** (needed for voice recognition)
- Speech recognition failed - try speaking more clearly

### "Can't import modules"
If you get import errors:
```bash
# Fix by installing again with --user flag
pip install --user SpeechRecognition edge-tts pynput

# Or upgrade pip first
python -m pip install --upgrade pip
pip install SpeechRecognition edge-tts pynput
```

## Technical Details

### Voice Processing Flow
1. **Key Press Detection** (pynput)
   - Monitors Alt+V globally
   - Works even when app window is not focused

2. **Audio Recording** (SpeechRecognition)
   - Records from default microphone
   - Sends to Google Speech API
   - Returns transcribed text (no API key needed)

3. **AI Response** (AIChat)
   - Sends transcribed text to AI
   - AI responds based on pet personality and state
   - Response includes pet mood context

4. **Text-to-Speech** (edge-tts)
   - Converts AI response to speech
   - Uses Japanese female voice (NanaNeural)
   - Saves to `temp_voice.mp3`

5. **Audio Playback** (PowerShell/subprocess)
   - Plays audio using Windows Media Player (via PowerShell)
   - Automatic cleanup of temp files

### Settings Storage
Voice settings are saved in `settings/setings.json`:
```json
{
  "voice_enabled": true,
  "voice_keybind": "alt+v"
}
```

## Features

✅ **Press-to-Hold Recording** - Intuitive voice input  
✅ **Transcription** - Speech to text (Google Speech API)  
✅ **AI Response** - Pet understands context and mood  
✅ **Japanese Voice** - Cute young female voice (15-18 yo voice actor style)  
✅ **Multi-language** - Speak in any language, response in Japanese  
✅ **No API Keys Needed** - Uses free Google and Microsoft APIs  
✅ **Global Keybind** - Works even when window isn't focused  
✅ **Settings UI** - Toggle and configure from app settings  

## Limitations

- Requires internet connection for both speech recognition and TTS
- Google Speech API has a 10-second recording limit per request
- Edge-TTS needs internet to generate voice
- Windows currently has the best support (PowerShell audio playback)

## Future Enhancements

Potential improvements:
- Add support for other voice options (different accents, ages)
- Allow custom keybind configuration in UI
- Add noise reduction for better recognition
- Support for other languages with appropriate voices
- Offline voice recognition option

## Environment Variables

Optional - for advanced users:
```bash
# Use custom Google Speech Recognition API endpoint
GOOGLE_SPEECH_RECOGNITION_API_KEY=your_key

# Configure edge-tts voice options
VOICE_LANGUAGE=ja-JP
VOICE_GENDER=Female
```

## Support

If you encounter issues:
1. Check microphone is working in Windows Sound settings
2. Verify internet connection
3. Try speaking more clearly and slowly
4. Check that Python can access microphone (Windows may prompt)
5. Look at console output for specific error messages

Enjoy talking to your pet! 🎤🐱
