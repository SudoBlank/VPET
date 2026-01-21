from __future__ import annotations

from ai.chat import AIChat
from pets.cat import CatPet
from ui.window import VPetWindow
from save_load_manager import SaveLoadManager


def main() -> None:
    """Initialize and run the virtual pet application."""
    pet = CatPet()
    ai = AIChat()
    save_load_manager = SaveLoadManager()  # Initialize SaveLoadManager
    saved_data = save_load_manager.load()  # Load existing data
    window = VPetWindow(pet, ai)
    window.run()


if __name__ == "__main__":
    main()