from __future__ import annotations

import tkinter as tk
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from PIL import Image, ImageTk

if TYPE_CHECKING:
    from pets.base import VirtualPet
    from ai.chat import AIChat

try:
    from settings.manager import Settings
except ImportError:
    # Fallback if Settings doesn't exist
    class Settings:
        def __init__(self) -> None:
            self._settings: dict[str, Any] = {}
        
        def get(self, key: str, default: Any = None) -> Any:
            return self._settings.get(key, default)


class VPetWindow:
    """Virtual pet window with sprite rendering and interaction."""

    def __init__(self, pet: VirtualPet, ai: AIChat | None = None, settings: Settings | None = None) -> None:
        self.pet = pet
        self.ai = ai
        self.settings = settings if settings is not None else Settings()

        # Window setup
        self.root = tk.Tk()
        self.root.title("VPet")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        self.transparent_color = "pink"
        self.root.wm_attributes("-transparentcolor", self.transparent_color)

        # Canvas
        self.base_size = 128
        pet_scale = cast(float, self.settings.get("pet_scale", 1.0))
        self.size = int(self.base_size * pet_scale)

        self.canvas = tk.Canvas(
            self.root,
            width=self.size,
            height=self.size,
            bg=self.transparent_color,
            highlightthickness=0,
        )
        self.canvas.pack()

        # Import Sprites class
        from ui.sprites import Sprites
        self.sprites_manager = Sprites(pet_type=pet.name.lower(), size=self.size)

        # Current sprite
        self.current_sprite: ImageTk.PhotoImage | None = None
        self.sprite_id: int | None = None
        self.is_dragging = False

        self.update_sprite()

        # Dragging
        self._drag_x = 0
        self._drag_y = 0
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag)
        self.root.bind("<ButtonRelease-1>", self.end_drag)

        # Right-click menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Talk", command=self.talk)
        self.menu.add_command(label="Feed", command=self.feed)
        self.menu.add_command(label="Play", command=self.play)
        self.menu.add_command(label="Sleep", command=self.sleep)
        self.menu.add_separator()
        self.menu.add_command(label="Stats", command=self.show_stats)
        self.menu.add_command(label="Settings", command=self.open_settings)
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=self.root.quit)

        self.root.bind("<Button-3>", self.show_menu)

        # Apply settings
        self.apply_settings()

        # Start loops
        self.tick()
        self.idle_animation()
        self.roam_around()

    def load_sprites(self) -> None:
        """Load and resize pet sprites."""
        base = Path("assets") / f"{self.pet.name.lower()}s"

        def load(name: str) -> ImageTk.PhotoImage:
            img = Image.open(base / name).convert("RGBA")
            img = img.resize((self.size, self.size), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        # Try to load sprites, skip if files don't exist
        try:
            self.sprites_manager.load_sprite("happy", str(base / f"{self.pet.name.lower()}_happy.png"))
            self.sprites_manager.load_sprite("sad", str(base / f"{self.pet.name.lower()}_sad.png"))
            self.sprites_manager.load_sprite("angry", str(base / f"{self.pet.name.lower()}_angry.png"))
        except Exception as e:
            print(f"Could not load sprites: {e}")

    def update_sprite(self) -> None:
        """Update displayed sprite based on pet mood."""
        mood = self.pet.mood()
        sprite = self.sprites_manager.get_sprite(mood)
        
        # Fallback to happy sprite if mood sprite not available
        if sprite is None:
            sprite = self.sprites_manager.get_sprite("happy")
        
        # Create placeholder if no sprite available
        if sprite is None:
            sprite = self._create_placeholder_sprite()

        if self.sprite_id:
            self.canvas.delete(self.sprite_id)

        self.current_sprite = sprite
        self.sprite_id = self.canvas.create_image(
            self.size // 2, self.size // 2, image=self.current_sprite
        )

    def _create_placeholder_sprite(self) -> ImageTk.PhotoImage:
        """Create a placeholder sprite when real sprites aren't available."""
        img = Image.new("RGBA", (self.size, self.size), self.transparent_color)
        return ImageTk.PhotoImage(img)

    def apply_settings(self) -> None:
        """Apply user settings to window."""
        always_on_top = cast(bool, self.settings.get("always_on_top", True))
        self.root.attributes("-topmost", always_on_top)

        transparent = cast(bool, self.settings.get("transparent", True))
        if transparent:
            self.root.wm_attributes("-transparentcolor", self.transparent_color)
        else:
            self.root.wm_attributes("-transparentcolor", "")

    def reload_sprites(self) -> None:
        """Reload sprites with new scale setting."""
        scale = cast(float, self.settings.get("pet_scale", 1.0))
        self.size = int(self.base_size * scale)

        self.canvas.config(width=self.size, height=self.size)
        self.sprites_manager.resize(self.size)
        self.update_sprite()

    def feed(self) -> None:
        """Feed the pet."""
        self.pet.feed()
        self.update_sprite()

    def play(self) -> None:
        """Play with the pet."""
        self.pet.play()
        self.update_sprite()

    def sleep(self) -> None:
        """Make the pet sleep."""
        self.pet.sleep()
        self.update_sprite()

    def talk(self) -> None:
        """Open chat window to talk with the pet."""
        if self.ai is None:
            from tkinter import messagebox
            messagebox.showinfo("AI Not Available", "AI chat is not enabled.")
            return

        ai_enabled = cast(bool, self.settings.get("ai_enabled", True))
        if not ai_enabled:
            from tkinter import messagebox
            messagebox.showinfo("AI Disabled", "AI chat is disabled in settings.")
            return

        try:
            from ui.chat_window import ChatWindow
            ChatWindow(self.pet, self.ai)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to open chat: {e}")

    def show_stats(self) -> None:
        """Display pet stats in a message box."""
        from tkinter import messagebox

        stats = (
            f"{self.pet.name}'s Stats:\n\n"
            f"Hunger: {self.pet.hunger:.0f}%\n"
            f"Happiness: {self.pet.happiness:.0f}%\n"
            f"Energy: {self.pet.energy:.0f}%\n"
            f"Mood: {self.pet.mood()}\n"
            f"Sleeping: {'Yes' if self.pet.is_sleeping else 'No'}"
        )
        messagebox.showinfo("Pet Stats", stats)

    def open_settings(self) -> None:
        """Open settings window."""
        try:
            from ui.setings_window import SettingsWindow
            SettingsWindow(self)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to open settings: {e}")

    def tick(self) -> None:
        """Update pet state periodically."""
        self.pet.tick()
        self.update_sprite()

        tick_interval = cast(int, self.settings.get("tick_interval_ms", 5000))
        self.root.after(tick_interval, self.tick)

    def idle_animation(self) -> None:
        """Idle animation (pet bobs up and down)."""
        if not self.sprite_id or self.is_dragging:
            self.root.after(4000, self.idle_animation)
            return

        self.canvas.move(self.sprite_id, 0, -2)
        self.root.after(150, lambda: self.canvas.move(self.sprite_id, 0, 2))
        self.root.after(4000, self.idle_animation)

    def roam_around(self) -> None:
        """Make pet roam around the screen periodically (mostly horizontal movement)."""
        import random

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Get current position
        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()

        # Generate target position with mostly X-axis movement
        # X: full horizontal range movement
        target_x = random.randint(0, screen_width - self.size)

        # Y: small random change (±50 pixels from current)
        target_y = current_y + random.randint(-50, 50)
        target_y = max(0, min(target_y, screen_height - self.size))

        # Animate movement slowly (120 steps = ~4 seconds)
        self._animate_to_position(current_x, current_y, target_x, target_y, steps=120)

        # Schedule next roam
        roam_interval = cast(int, self.settings.get("roam_interval_ms", 30000))
        self.root.after(roam_interval, self.roam_around)

    def _animate_to_position(
        self, start_x: int, start_y: int, end_x: int, end_y: int, steps: int = 120
    ) -> None:
        """Smoothly animate window movement to target position."""
        if steps <= 0:
            return

        # Calculate incremental movement
        delta_x = (end_x - start_x) / steps
        delta_y = (end_y - start_y) / steps

        new_x = int(start_x + delta_x)
        new_y = int(start_y + delta_y)

        self.root.geometry(f"+{new_x}+{new_y}")

        # Continue animation (slower at 32ms per frame = ~4 seconds total)
        self.root.after(
            32, lambda: self._animate_to_position(new_x, new_y, end_x, end_y, steps - 1)
        )

    def start_drag(self, event: tk.Event[Any]) -> None:
        """Record drag start position."""
        self._drag_x = event.x
        self._drag_y = event.y
        self.is_dragging = True
        # Change sprite when picked up
        picked_up = self.sprites_manager.get_sprite("picked_up")
        if picked_up and self.sprite_id:
            self.current_sprite = picked_up
            self.canvas.itemconfig(self.sprite_id, image=self.current_sprite)

    def drag(self, event: tk.Event[Any]) -> None:
        """Move window during drag."""
        x = self.root.winfo_x() + event.x - self._drag_x
        y = self.root.winfo_y() + event.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    def end_drag(self, event: tk.Event[Any]) -> None:
        """Handle end of drag."""
        self.is_dragging = False
        self.update_sprite()

    def show_menu(self, event: tk.Event[Any]) -> None:
        """Display right-click context menu."""
        self.menu.tk_popup(event.x_root, event.y_root)

    def run(self) -> None:
        """Start the main event loop."""
        self.root.mainloop()
