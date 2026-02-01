"""Voice interaction system for virtual pets."""

import asyncio
import threading
import subprocess
import os
from pathlib import Path
from typing import Callable, Optional, Any

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

try:
    import sounddevice
    import soundfile
    import numpy as np
except ImportError:
    sounddevice = None  # type: ignore
    soundfile = None  # type: ignore
    np = None  # type: ignore


class VoiceManager:
    """Manage voice input and output for the pet."""

    def __init__(self) -> None:
        self.recognizer: Optional[Any] = None
        self.voice_thread: Optional[threading.Thread] = None
        self.audio_file = Path("temp_voice.mp3")
        self._initialized = False

    def _lazy_init(self) -> bool:
        if self._initialized:
            return self.recognizer is not None

        self._initialized = True

        if not sr:
            print("❌ SpeechRecognition library not installed. Install with: pip install SpeechRecognition")
            return False

        if not sounddevice or not soundfile or not np:
            print("❌ Missing audio libraries. Install with: pip install sounddevice soundfile numpy")
            return False

        try:
            self.recognizer = sr.Recognizer()
            print("✓ Voice system initialized")
            return True
        except Exception as e:
            print(f"❌ Voice initialization failed: {type(e).__name__}: {e}")
            return False

    def transcribe_audio(self) -> Optional[str]:
        if not self._lazy_init():
            return None

        if self.recognizer is None:
            return None

        try:
            # Record audio using sounddevice
            duration = 10  # seconds
            sample_rate = 16000
            print("🎤 Recording audio for 10 seconds...")
            try:
                audio_data = sounddevice.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32', blocksize=16000)
                sounddevice.wait()
                print(f"✓ Audio recorded ({len(audio_data)} samples)")
            except Exception as e:
                print(f"❌ Recording failed: {type(e).__name__}: {e}")
                return None
            
            # Convert float32 to int16 for SpeechRecognition
            try:
                audio_int16 = (audio_data.flatten() * 32767).astype(np.int16)
                audio = sr.AudioData(audio_int16.tobytes(), sample_rate, 2)
                print("✓ Audio converted to proper format")
            except Exception as e:
                print(f"❌ Audio conversion failed: {type(e).__name__}: {e}")
                return None
            
            # Recognize speech
            try:
                print("🔍 Sending to Google Speech Recognition...")
                result = self.recognizer.recognize_google(audio)
                print(f"✓ Recognized: {result}")
                return result
            except sr.UnknownValueError:
                print("❌ Could not understand audio - speak clearly and try again")
                return None
            except sr.RequestError as e:
                print(f"❌ Speech recognition service error: {e}")
                return None
        except Exception as e:
            print(f"❌ Unexpected error in transcribe_audio: {type(e).__name__}: {e}")
            return None

    async def synthesize_speech(self, text: str) -> bool:
        if not edge_tts:
            print("❌ edge-tts not installed. Install with: pip install edge-tts")
            return False

        try:
            print(f"🔊 Synthesizing speech: {text[:50]}...")
            # Use a young Japanese-sounding English voice
            # These voices sound youthful and have a cute quality
            voice = "en-US-AvaNeural"  # Young sounding female voice
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(self.audio_file))
            print(f"✓ Audio synthesized and saved to {self.audio_file}")
            return True
        except Exception as e:
            print(f"❌ Speech synthesis failed: {type(e).__name__}: {e}")
            return False

    def play_audio(self) -> bool:
        if not self.audio_file.exists():
            print(f"❌ Audio file not found: {self.audio_file}")
            return False

        try:
            print(f"▶️  Playing audio: {self.audio_file}")
            if os.name == "nt":
                # Use Windows Media Player instead of SoundPlayer for better reliability
                result = subprocess.run([
                    "powershell",
                    "-Command",
                    f'Start-Process -FilePath "{self.audio_file}" -Wait'
                ], capture_output=True, timeout=30)
                if result.returncode != 0:
                    print(f"⚠️  PowerShell playback returned code {result.returncode}")
            else:
                subprocess.run(["ffplay", "-nodisp", "-autoexit", str(self.audio_file)], timeout=30)
            print("✓ Audio playback completed")
            return True
        except subprocess.TimeoutExpired:
            print("❌ Audio playback timed out")
            return False
        except Exception as e:
            print(f"❌ Audio playback failed: {type(e).__name__}: {e}")
            return False

    def speak_text(self, text: str) -> bool:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(self.synthesize_speech(text))
        loop.close()
        return success and self.play_audio()

    def listen_for_voice(
        self,
        on_text_received: Callable[[str], None],
        duration: float = 5.0
    ) -> None:
        if not self._lazy_init():
            on_text_received("[voice unavailable]")
            return

        if self.recognizer is None:
            on_text_received("[voice unavailable]")
            return

        def listen() -> None:
            try:
                # Record audio using sounddevice
                sample_rate = 16000
                print("🎤 Recording audio...")
                try:
                    audio_data = sounddevice.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32', blocksize=16000)
                    sounddevice.wait()
                    print(f"✓ Audio recorded ({len(audio_data)} samples)")
                except Exception as e:
                    on_text_received(f"❌ Recording failed: {type(e).__name__}: {e}")
                    return
                
                # Convert float32 to int16 for SpeechRecognition
                try:
                    audio_int16 = (audio_data.flatten() * 32767).astype(np.int16)
                    audio = sr.AudioData(audio_int16.tobytes(), sample_rate, 2)
                except Exception as e:
                    on_text_received(f"❌ Audio conversion failed: {type(e).__name__}: {e}")
                    return
                
                # Recognize speech
                try:
                    print("🔍 Sending to Google Speech Recognition...")
                    result = self.recognizer.recognize_google(audio)
                    print(f"✓ Recognized: {result}")
                    on_text_received(result)
                except sr.UnknownValueError:
                    on_text_received("[Could not understand audio - please speak clearly]")
                except sr.RequestError as e:
                    on_text_received(f"[Speech service error: {e}]")
            except Exception as e:
                on_text_received(f"❌ Unexpected error: {type(e).__name__}: {e}")

        self.voice_thread = threading.Thread(target=listen, daemon=True)
        self.voice_thread.start()

    def cleanup(self) -> None:
        if self.audio_file.exists():
            try:
                self.audio_file.unlink()
            except Exception:
                pass


class KeyboardListener:
    """Listen for keyboard events to trigger voice recording."""

    def __init__(self, on_activate: Callable[[], None]) -> None:
        if not keyboard:
            self.listener = None
            return

        self.on_activate = on_activate
        self.alt_pressed = False

        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

    def start(self) -> None:
        if self.listener:
            self.listener.start()

    def stop(self) -> None:
        if self.listener:
            self.listener.stop()

    def _on_press(self, key) -> None:
        try:
            if key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
                self.alt_pressed = True

            if self.alt_pressed and hasattr(key, "char") and key.char == "v":
                self.on_activate()
        except Exception:
            pass

    def _on_release(self, key) -> None:
        if key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
            self.alt_pressed = False
