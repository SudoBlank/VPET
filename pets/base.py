"""Base class for virtual pets."""


class VirtualPet:
    """Base class for all virtual pets."""

    def __init__(self, name: str, personality: str) -> None:
        """Initialize a virtual pet.
        
        Args:
            name: Name of the pet
            personality: Personality description/prompt for AI
        """
        self.name = name
        self.personality = personality

        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.is_sleeping = False

    def tick(self) -> None:
        """Update pet state each tick."""
        if self.is_sleeping:
            # Gain energy when sleeping
            self.energy = min(100, self.energy + 2)
            # Still get slightly hungry
            self.hunger += 0.5
        else:
            self.hunger += 1
            self.energy -= 1
            self.happiness -= 0.5

        # Clamp values
        self.hunger = min(100, max(0, self.hunger))
        self.energy = min(100, max(0, self.energy))
        self.happiness = min(100, max(0, self.happiness))

    def feed(self) -> None:
        """Feed the pet."""
        self.hunger = max(0, self.hunger - 20)
        self.happiness += 5
        self.is_sleeping = False

    def play(self) -> None:
        """Play with the pet."""
        if not self.is_sleeping:
            self.happiness += 10
            self.energy -= 5
            self.hunger += 3

    def sleep(self) -> None:
        """Make the pet sleep."""
        self.is_sleeping = True

    def wake_up(self) -> None:
        """Wake the pet up."""
        self.is_sleeping = False

    def mood(self) -> str:
        """Get the pet's current mood.
        
        Returns:
            Mood string: 'happy', 'sad', 'angry', 'shy', 'tickling', 'walking', or 'sleeping'
        """
        if self.is_sleeping:
            return "sleeping"
        if self.happiness > 80:
            return "tickling"  # Very happy and playful
        if self.happiness > 70:
            return "happy"
        if self.happiness > 50 and self.energy > 60:
            return "walking"  # Content and energetic
        if self.happiness < 20:
            return "sad"
        if self.happiness < 40:
            return "shy"  # Somewhat unhappy
        if self.hunger > 80:
            return "angry"
        return "happy"

    def to_dict(self) -> dict:
        """Convert pet state to dictionary for saving."""
        return {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "is_sleeping": self.is_sleeping,
        }

    def from_dict(self, data: dict) -> None:
        """Load pet state from dictionary."""
        self.hunger = data.get("hunger", 50)
        self.happiness = data.get("happiness", 50)
        self.energy = data.get("energy", 50)
        self.is_sleeping = data.get("is_sleeping", False)
