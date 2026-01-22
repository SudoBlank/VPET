from __future__ import annotations

from ai.chat import AIChat
from pets.cat import CatPet
from pets.dog import DogPet
from pets.anime_girl import AnimeGirlPet
from ui.window import VPetWindow
from save_load_manager import SaveLoadManager
from settings.manager import Settings


def get_pet_by_type(pet_type: str):
    """Get pet instance by type name.
    
    Args:
        pet_type: Type of pet ('cat', 'dog', 'anime_girl')
        
    Returns:
        Pet instance
    """
    if pet_type == "dog":
        return DogPet()
    elif pet_type == "anime_girl":
        return AnimeGirlPet()
    else:
        return CatPet()


def main() -> None:
    """Initialize and run the virtual pet application."""
    settings = Settings(Path("settings") / "setings.json")
    pet_type = settings.get("pet_type", "cat")
    
    pet = get_pet_by_type(pet_type)
    ai = AIChat()
    save_load_manager = SaveLoadManager()  # Initialize SaveLoadManager
    saved_data = save_load_manager.load()  # Load existing data
    window = VPetWindow(pet, ai, settings)
    window.run()


if __name__ == "__main__":
    from pathlib import Path
    main()
