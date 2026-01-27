from voice_manager import VoiceManager, KeyboardListener
from pathlib import Path
from settings.manager import Settings
from ai.chat import AIChat
from save_load_manager import SaveLoadManager
from ui.window import VPetWindow
from pets.cat import CatPet
from pets.dog import DogPet
from pets.anime_girl import AnimeGirlPet


def get_pet_by_type(pet_type: str):
    """Get pet instance by type name."""
    pet_types = {
        "cat": CatPet,
        "dog": DogPet,
        "anime_girl": AnimeGirlPet,
    }
    pet_class = pet_types.get(pet_type.lower(), CatPet)
    return pet_class()


def main() -> None:
    settings = Settings(str(Path("settings") / "setings.json"))
    pet_type = settings.get("pet_type", "cat")

    pet = get_pet_by_type(pet_type)
    ai = AIChat()
    save_load_manager = SaveLoadManager()
    save_load_manager.load()

    voice = VoiceManager()

    def on_alt_v():
        print("Alt+V detected — listening...")
        voice.listen_for_voice(print)

    listener = KeyboardListener(on_alt_v)
    listener.start()

    print("VPET running. Press Alt+V to talk.")

    window = VPetWindow(pet, ai, settings)
    window.run()  # This keeps the app alive


if __name__ == "__main__":
    main()
