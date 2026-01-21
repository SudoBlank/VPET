class VirtualPet:
    def __init__(self, name: str, personality: str):
        self.name = name
        self.personality = personality

        self.hunger = 50
        self.happiness = 50
        self.energy = 50

    def tick(self):
        self.hunger += 1
        self.energy -= 1
        self.happiness -= 0.5

    def feed(self):
        self.hunger = max(0, self.hunger - 20)
        self.happiness += 5

    def play(self):
        self.happiness += 10
        self.energy -= 5

    def mood(self) -> str:
        if self.happiness > 70:
            return "happy"
        if self.happiness < 30:
            return "sad"
        if self.hunger > 80:
            return "angry"
        return "happy"
