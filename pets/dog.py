from pets.base import VirtualPet
from ai.personalities import PERSONALITIES

class DogPet(VirtualPet):
    def __init__(self):
        super().__init__(
            name="Dog",
            personality=PERSONALITIES["dog"]
        )

    def play(self):
        super().play()
        self.happiness += 5
