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


class VoiceManager:
    """Manage voice input and output for the pet."""

    def __init__(self) -> None:
        self.recognizer: Optional[Any] = None
        self.microphone: Optional[Any] = None
        self.voice_thread: Optional[threading.Thread] = None
        self.audio_file = Path("temp_voice.mp3")
        self._initialized = False

    def _lazy_init(self) -> bool:
        if self._initialized:
            return self.recognizer is not None and self.microphone is not None

        self._initialized = True

        if not sr:
            print("SpeechRecognition not installed.")
            return False

        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            return True
        except Exception as e:
            print(f"Voice init failed: {e}")
            return False

    def transcribe_audio(self) -> Optional[str]:
        if not self._lazy_init():
            return None

        if self.recognizer is None or self.microphone is None:
            return None

        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10)

            return self.recognizer.recognize_google(audio)
        except Exception:
            return None

    async def synthesize_speech(self, text: str) -> bool:
        if not edge_tts:
            return False

        try:
            voice = "ja-JP-NanaNeural"
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(self.audio_file))
            return True
        except Exception:
            return False

    def play_audio(self) -> bool:
        if not self.audio_file.exists():
            return False

        try:
            if os.name == "nt":
                subprocess.Popen([
                    "powershell",
                    "-Command",
                    f'(New-Object System.Media.SoundPlayer "{self.audio_file}").PlaySync()'
                ])
            else:
                subprocess.Popen(["ffplay", "-nodisp", "-autoexit", str(self.audio_file)])
            return True
        except Exception:
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

        if self.recognizer is None or self.microphone is None:
            on_text_received("[voice unavailable]")
            return

        def listen() -> None:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, 0.5)
                    audio = self.recognizer.listen(source, timeout=int(duration))
                on_text_received(self.recognizer.recognize_google(audio))
            except Exception as e:
                on_text_received(f"[error: {e}]")

        self.voice_thread = threading.Thread(target=listen, daemon=True)
        self.voice_thread.start()

    def cleanup(self) -> None:
        if self.audio_file.exists():
            try:
                self.audio_file.unlink()
            except Exception:
                pass


class KeyboardListener:
    def __init__(self) -> None:
        if not keyboard:
            self.listener = None
            return

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
        pass

    def _on_release(self, key) -> None:
        pass
