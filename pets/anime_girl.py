from pets.base import VirtualPet
from ai.personalities import PERSONALITIES

class AnimeGirlPet(VirtualPet):
    def __init__(self):
        super().__init__(
            name="Anime Girl",
            personality=PERSONALITIES["anime_girl"]
        )

    def play(self):
        super().play()
        self.happiness += 5
