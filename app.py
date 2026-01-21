from __future__ import annotations

from ai.chat import AIChat
from pets.cat import CatPet
from ui.window import VPetWindow


def main() -> None:
    """Initialize and run the virtual pet application."""
    pet = CatPet()
    ai = AIChat()
    window = VPetWindow(pet, ai)
    window.run()


if __name__ == "__main__":
    main()