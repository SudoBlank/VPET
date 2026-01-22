"""Sprite management for virtual pets."""

from pathlib import Path
from PIL import Image, ImageTk
from typing import Optional


class Sprites:
    """Manage pet sprites for different states and animations."""

    def __init__(self, pet_type: str = "cat", size: int = 128) -> None:
        """Initialize sprite manager.
        
        Args:
            pet_type: Type of pet ('cat', 'dog', 'anime_girl')
            size: Size of sprites in pixels
        """
        self.pet_type = pet_type
        self.size = size
        self.sprites: dict[str, ImageTk.PhotoImage] = {}
        self.asset_base = Path("assets") / f"{pet_type}s"
        self.load_default_sprites()

    def load_default_sprites(self) -> None:
        """Load default sprites for the pet."""
        # All possible sprite states - some may not exist for all pets
        sprite_states = [
            "happy",
            "sad",
            "angry",
            "shy",
            "sleeping",
            "picked_up",
            "grabed",  # Alternate spelling
            "tickling",
            "walking",
        ]

        for state in sprite_states:
            filepath = self.asset_base / f"{self.pet_type}_{state}.png"
            if filepath.exists():
                self.load_sprite(state, str(filepath))

    def load_sprite(self, state: str, filepath: str) -> None:
        """Load a sprite from file.
        
        Args:
            state: State name (e.g., 'happy', 'sad')
            filepath: Path to sprite image
        """
        try:
            img = Image.open(filepath).convert("RGBA")
            img = img.resize((self.size, self.size), Image.Resampling.LANCZOS)
            self.sprites[state] = ImageTk.PhotoImage(img)
        except RuntimeError as e:
            # Handle "no default root window" error in non-GUI contexts
            if "no default root window" in str(e):
                # Silently skip - GUI isn't running
                return
            print(f"Failed to load sprite {filepath}: {e}")
        except Exception as e:
            print(f"Failed to load sprite {filepath}: {e}")

    def get_sprite(self, state: str) -> Optional[ImageTk.PhotoImage]:
        """Get sprite for a given state.
        
        Args:
            state: State name
            
        Returns:
            PhotoImage or None if state not found
        """
        return self.sprites.get(state)

    def get_available_states(self) -> list[str]:
        """Get list of available sprite states."""
        return list(self.sprites.keys())

    def resize(self, new_size: int) -> None:
        """Resize all sprites to a new size."""
        self.size = new_size
        self.sprites.clear()
        self.load_default_sprites()

