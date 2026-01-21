from pets.base import VirtualPet
from ai.personalities import PERSONALITIES

class CatPet(VirtualPet):
    def __init__(self):
        super().__init__(
            name="Cat",
            personality=PERSONALITIES["cat"]
        )

    def play(self):
        super().play()
        self.happiness += 5
