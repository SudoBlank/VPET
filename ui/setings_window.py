from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
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
        self.win.geometry("350x600")
        self.win.attributes("-topmost", True)

        self.always_on_top: tk.BooleanVar
        self.transparent: tk.BooleanVar
        self.scale: tk.Scale
        self.input_reaction: tk.BooleanVar
        self.ai_enabled: tk.BooleanVar
        self.roam_scale: tk.Scale
        self.pet_type_var: tk.StringVar

        self.build()

    def build(self) -> None:
        """Build the settings UI."""
        # Pet Type Selection
        tk.Label(self.win, text="Select Pet Type", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=5)
        self.pet_type_var = tk.StringVar(value=self.settings.get("pet_type", "cat"))
        
        pet_frame = tk.Frame(self.win)
        pet_frame.pack(anchor="w", padx=5, pady=5, fill="x")
        
        for pet in ["cat", "dog", "anime_girl"]:
            tk.Radiobutton(
                pet_frame,
                text=pet.capitalize(),
                variable=self.pet_type_var,
                value=pet,
                command=self.on_pet_change
            ).pack(anchor="w")
        
        tk.Separator(self.win, orient="horizontal").pack(fill="x", pady=5)

        self.always_on_top = tk.BooleanVar(
            value=self.settings.get("always_on_top", True)
        )
        tk.Checkbutton(
            self.win,
            text="Always on top",
            variable=self.always_on_top,
            command=self.apply,
        ).pack(anchor="w", padx=5)

        self.transparent = tk.BooleanVar(value=self.settings.get("transparent", True))
        tk.Checkbutton(
            self.win,
            text="Transparent window",
            variable=self.transparent,
            command=self.apply,
        ).pack(anchor="w", padx=5)

        tk.Label(self.win, text="Pet size", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=(10, 0))
        self.scale = tk.Scale(
            self.win,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            orient="horizontal",
            command=self.on_scale,
        )
        self.scale.set(self.settings.get("pet_scale", 1.0))
        self.scale.pack(fill="x", padx=5)

        self.input_reaction = tk.BooleanVar(
            value=self.settings.get("input_reaction", True)
        )
        tk.Checkbutton(
            self.win,
            text="React to keyboard/mouse",
            variable=self.input_reaction,
            command=self.apply,
        ).pack(anchor="w", padx=5)

        self.ai_enabled = tk.BooleanVar(value=self.settings.get("ai_enabled", True))
        tk.Checkbutton(
            self.win,
            text="Enable AI talking",
            variable=self.ai_enabled,
            command=self.apply,
        ).pack(anchor="w", padx=5)

        tk.Label(self.win, text="Roaming frequency (seconds)", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=(10, 0))
        self.roam_scale = tk.Scale(
            self.win,
            from_=10,
            to=120,
            resolution=5,
            orient="horizontal",
            command=self.on_roam_scale,
        )
        self.roam_scale.set(self.settings.get("roam_interval_ms", 30000) / 1000)
        self.roam_scale.pack(fill="x", padx=5)

        tk.Separator(self.win, orient="horizontal").pack(fill="x", pady=10)

        tk.Button(self.win, text="Reset Pet Stats", command=self.reset_pet, bg="#FFE6E6").pack(
            fill="x", padx=5, pady=5
        )

    def on_pet_change(self) -> None:
        """Handle pet type change."""
        new_pet_type = self.pet_type_var.get()
        self.settings.set("pet_type", new_pet_type)
        messagebox.showinfo(
            "Pet Changed",
            f"Pet changed to {new_pet_type.capitalize()}.\nRestart the application to load the new pet."
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
        self.vpet.pet.is_sleeping = False
        self.vpet.update_sprite()
        messagebox.showinfo("Reset", "Pet stats have been reset to default values.")
