from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypeVar, overload

T = TypeVar("T")


class Settings:
    """Manage application settings with JSON persistence."""

    def __init__(self, config_file: str = "settings.json") -> None:
        self.config_path = Path(config_file)
        self._settings: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        """Load settings from JSON file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_defaults()
        return self._get_defaults()

    def _get_defaults(self) -> dict[str, Any]:
        """Return default settings."""
        return {
            "pet_scale": 1.0,
            "always_on_top": True,
            "transparent": True,
            "tick_interval_ms": 5000,
            "roam_interval_ms": 30000,  # Roam every 30 seconds
        }

    def save(self) -> None:
        """Save settings to JSON file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2)
        except IOError as e:
            print(f"Failed to save settings: {e}")

    @overload
    def get(self, key: str) -> Any: ...

    @overload
    def get(self, key: str, default: T) -> T: ...

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value with optional default."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a setting value and save."""
        self._settings[key] = value
        self.save()

    def reset(self) -> None:
        """Reset to default settings."""
        self._settings = self._get_defaults()
        self.save()

    def get_all(self) -> dict[str, Any]:
        """Get all settings as a dictionary."""
        return self._settings.copy()