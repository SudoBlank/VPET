"""Pet memory and interaction tracking system."""

from datetime import datetime
from typing import Any


class PetMemory:
    """Track pet interactions and memories."""

    def __init__(self) -> None:
        """Initialize pet memory."""
        self.interactions: list[dict[str, Any]] = []
        self.preferences: dict[str, Any] = {}
        self.last_interaction: datetime | None = None

    def record_interaction(self, interaction_type: str, details: str = "") -> None:
        """Record an interaction with the pet.
        
        Args:
            interaction_type: Type of interaction (e.g., 'talk', 'feed', 'play')
            details: Additional details about the interaction
        """
        self.interactions.append({
            "type": interaction_type,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        })
        self.last_interaction = datetime.now()

    def get_interaction_count(self, interaction_type: str) -> int:
        """Get count of specific interaction type.
        
        Args:
            interaction_type: Type of interaction to count
            
        Returns:
            Number of interactions of this type
        """
        return sum(1 for i in self.interactions if i["type"] == interaction_type)

    def set_preference(self, key: str, value: Any) -> None:
        """Set a pet preference.
        
        Args:
            key: Preference key
            value: Preference value
        """
        self.preferences[key] = value

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a pet preference.
        
        Args:
            key: Preference key
            default: Default value if key not found
            
        Returns:
            Preference value or default
        """
        return self.preferences.get(key, default)

    def to_dict(self) -> dict[str, Any]:
        """Convert memory to dictionary for saving."""
        return {
            "interactions": self.interactions,
            "preferences": self.preferences,
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        """Load memory from dictionary."""
        self.interactions = data.get("interactions", [])
        self.preferences = data.get("preferences", {})
        
        last_int = data.get("last_interaction")
        if last_int:
            self.last_interaction = datetime.fromisoformat(last_int)
