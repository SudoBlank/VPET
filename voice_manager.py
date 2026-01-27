"""Voice interaction system for virtual pets."""

import asyncio
import threading
import subprocess
import os
from pathlib import Path
from typing import Callable, Optional

try:
    import speech_recognition as sr
except ImportError:
    sr = None  # type: ignore

try:
    import edge_tts
except ImportError:
    edge_tts = None  # type: ignore

try:
    from pynput import keyboard
except ImportError:
    keyboard = None  # type: ignore


class VoiceManager:
    """Manage voice input and output for the pet."""

    def __init__(self) -> None:
        """Initialize voice manager."""
        self.recognizer = sr.Recognizer() if sr else None
        self.microphone = sr.Microphone() if sr else None
        self.is_listening = False
        self.voice_thread: Optional[threading.Thread] = None
        self.audio_file = Path("temp_voice.mp3")

    def transcribe_audio(self) -> Optional[str]:
        """Transcribe audio from microphone to text.
        
        Returns:
            Transcribed text or None if failed
        """
        if not self.recognizer or not self.microphone:
            return None

        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10)
            
            # Use Google Speech Recognition (free, no API key needed)
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None  # Could not understand audio
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"Voice transcription error: {e}")
            return None

    async def synthesize_speech(self, text: str, language: str = "en") -> bool:
        """Convert text to speech in Japanese female voice.
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., 'en', 'ja')
            
        Returns:
            True if successful, False otherwise
        """
        if not edge_tts:
            print("edge-tts not installed")
            return False

        try:
            # Japanese female voice (young sounding)
            # Using ja-JP-NanaNeural which is a younger sounding female voice
            voice = "ja-JP-NanaNeural"
            
            # But speak the content in the requested language
            # We'll use a Japanese voice but it can handle English/other languages
            communicate = edge_tts.Communicate(text, voice, rate="+10%", pitch="+15Hz")
            
            await communicate.save(str(self.audio_file))
            return True
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            return False

    def play_audio(self) -> bool:
        """Play the generated audio file.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.audio_file.exists():
            return False

        try:
            # Use Windows media player or PowerShell to play audio
            if os.name == 'nt':  # Windows
                # Use PowerShell to play the audio file
                subprocess.Popen([
                    'powershell', '-Command',
                    f'(New-Object System.Media.SoundPlayer "{str(self.audio_file)}").PlaySync()'
                ])
                return True
            else:  # Linux/Mac
                subprocess.Popen(['ffplay', '-nodisp', '-autoexit', str(self.audio_file)])
                return True
        except Exception as e:
            print(f"Audio playback error: {e}")
            return False

    def speak_text(self, text: str) -> bool:
        """Convert text to speech and play it.
        
        Args:
            text: Text to speak
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Run async TTS in a thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(self.synthesize_speech(text))
            loop.close()
            
            if success:
                return self.play_audio()
            return False
        except Exception as e:
            print(f"Speak error: {e}")
            return False

    def listen_for_voice(self, on_text_received: Callable[[str], None], duration: float = 5.0) -> None:
        """Listen for voice input in background thread.
        
        Args:
            on_text_received: Callback function to handle transcribed text
            duration: Max duration to listen (seconds)
        """
        def listen_thread() -> None:
            try:
                # Set timeout for listening
                if self.recognizer and self.microphone:
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = self.recognizer.listen(source, timeout=int(duration))
                    
                    text = self.recognizer.recognize_google(audio)
                    on_text_received(text)
            except sr.UnknownValueError:
                on_text_received("[unintelligible]")
            except sr.RequestError as e:
                on_text_received(f"[error: {e}]")
            except Exception as e:
                on_text_received(f"[error: {e}]")

        self.voice_thread = threading.Thread(target=listen_thread, daemon=True)
        self.voice_thread.start()

    def cleanup(self) -> None:
        """Clean up voice resources."""
        if self.audio_file.exists():
            try:
                self.audio_file.unlink()
            except Exception:
                pass


class KeyboardListener:
    """Listen for keyboard events to trigger voice recording."""

    def __init__(self, keybind: str = "<alt>v") -> None:
        """Initialize keyboard listener.
        
        Args:
            keybind: Key combination to listen for (e.g., '<alt>v')
        """
        if not keyboard:
            self.listener = None
            return

        self.keybind = keybind
        self.key_down = False
        self.on_key_pressed: Optional[Callable[[], None]] = None
        self.on_key_released: Optional[Callable[[], None]] = None
        
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

    def start(self) -> None:
        """Start listening for keyboard events."""
        if self.listener:
            self.listener.start()

    def stop(self) -> None:
        """Stop listening for keyboard events."""
        if self.listener:
            self.listener.stop()

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        """Handle key press."""
        try:
            # Check if Alt+V is pressed
            if hasattr(key, 'vk') and key.vk == 86:  # 'V' key
                # Check if Alt is pressed
                alt_pressed = False
                try:
                    alt_pressed = keyboard.Controller().is_pressed(keyboard.Key.alt)
                except:
                    pass
                
                if alt_pressed and not self.key_down:
                    self.key_down = True
                    if self.on_key_pressed:
                        self.on_key_pressed()
        except:
            pass

    def _on_release(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        """Handle key release."""
        try:
            if hasattr(key, 'vk') and key.vk == 86:  # 'V' key
                if self.key_down:
                    self.key_down = False
                    if self.on_key_released:
                        self.on_key_released()
        except:
            pass
