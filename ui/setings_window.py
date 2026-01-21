from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.window import VPetWindow


class SettingsWindow:
    """Settings window for configuring VPet preferences."""

    def __init__(self, vpet_window: VPetWindow) -> None:
        self.vpet = vpet_window
        self.settings = vpet_window.settings

        self.win = tk.Toplevel()
        self.win.title("VPet Settings")
        self.win.geometry("300x500")
        self.win.attributes("-topmost", True)

        self.always_on_top: tk.BooleanVar
        self.transparent: tk.BooleanVar
        self.scale: tk.Scale
        self.input_reaction: tk.BooleanVar
        self.ai_enabled: tk.BooleanVar
        self.roam_scale: tk.Scale

        self.build()

    def build(self) -> None:
        """Build the settings UI."""
        self.always_on_top = tk.BooleanVar(
            value=self.settings.get("always_on_top", True)
        )
        tk.Checkbutton(
            self.win,
            text="Always on top",
            variable=self.always_on_top,
            command=self.apply,
        ).pack(anchor="w")

        self.transparent = tk.BooleanVar(value=self.settings.get("transparent", True))
        tk.Checkbutton(
            self.win,
            text="Transparent window",
            variable=self.transparent,
            command=self.apply,
        ).pack(anchor="w")

        tk.Label(self.win, text="Pet size").pack(anchor="w")
        self.scale = tk.Scale(
            self.win,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            orient="horizontal",
            command=self.on_scale,
        )
        self.scale.set(self.settings.get("pet_scale", 1.0))
        self.scale.pack(fill="x")

        self.input_reaction = tk.BooleanVar(
            value=self.settings.get("input_reaction", True)
        )
        tk.Checkbutton(
            self.win,
            text="React to keyboard/mouse",
            variable=self.input_reaction,
            command=self.apply,
        ).pack(anchor="w")

        self.ai_enabled = tk.BooleanVar(value=self.settings.get("ai_enabled", True))
        tk.Checkbutton(
            self.win,
            text="Enable AI talking",
            variable=self.ai_enabled,
            command=self.apply,
        ).pack(anchor="w")

        tk.Label(self.win, text="Roaming frequency (seconds)").pack(anchor="w")
        self.roam_scale = tk.Scale(
            self.win,
            from_=10,
            to=120,
            resolution=5,
            orient="horizontal",
            command=self.on_roam_scale,
        )
        self.roam_scale.set(self.settings.get("roam_interval_ms", 30000) / 1000)
        self.roam_scale.pack(fill="x")

        tk.Button(self.win, text="Reset Pet Stats", command=self.reset_pet).pack(
            fill="x", pady=10
        )

    def on_scale(self, value: str) -> None:
        """Handle pet scale slider changes."""
        self.settings.set("pet_scale", float(value))
        self.vpet.reload_sprites()

    def on_roam_scale(self, value: str) -> None:
        """Handle roaming frequency slider changes."""
        # Convert seconds to milliseconds
        self.settings.set("roam_interval_ms", int(float(value) * 1000))

    def apply(self) -> None:
        """Apply all settings changes."""
        self.settings.set("always_on_top", self.always_on_top.get())
        self.settings.set("transparent", self.transparent.get())
        self.settings.set("input_reaction", self.input_reaction.get())
        self.settings.set("ai_enabled", self.ai_enabled.get())

        self.vpet.apply_settings()

    def reset_pet(self) -> None:
        """Reset pet statistics to default values."""
        self.vpet.pet.hunger = 50
        self.vpet.pet.happiness = 50
        self.vpet.pet.energy = 50
        self.vpet.update_sprite()