"""Save and load functionality for application state."""

import json
from pathlib import Path
from typing import Any


class SaveLoadManager:
    """Manage saving and loading application state."""

    def __init__(self, save_file: str = "save_data.json") -> None:
        """Initialize save/load manager.
        
        Args:
            save_file: Path to save file
        """
        self.save_file = Path(save_file)

    def save(self, data: dict[str, Any]) -> None:
        """Save data to JSON file.
        
        Args:
            data: Data dictionary to save
        """
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Failed to save: {e}")

    def load(self) -> dict[str, Any]:
        """Load data from JSON file.
        
        Returns:
            Data dictionary or empty dict if file doesn't exist
        """
        if self.save_file.exists():
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Failed to load: {e}")
        return {}

    def save_pet(self, pet: Any) -> None:
        """Save pet state.
        
        Args:
            pet: Pet object with to_dict method
        """
        data = {"pet": pet.to_dict() if hasattr(pet, 'to_dict') else {}}
        self.save(data)

    def load_pet(self, pet: Any) -> None:
        """Load pet state.
        
        Args:
            pet: Pet object with from_dict method
        """
        data = self.load()
        if "pet" in data and hasattr(pet, 'from_dict'):
            pet.from_dict(data["pet"])
