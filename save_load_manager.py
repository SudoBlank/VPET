# Save and Load functionality
import json
from pathlib import Path

class SaveLoadManager:
    def __init__(self, save_file: str = "save_data.json"):
        self.save_file = Path(save_file)

    def save(self, data: dict) -> None:
        with open(self.save_file, 'w') as f:
            json.dump(data, f)

    def load(self) -> dict:
        if self.save_file.exists():
            with open(self.save_file, 'r') as f:
                return json.load(f)
        return {}  # Return empty dict if no save file exists
