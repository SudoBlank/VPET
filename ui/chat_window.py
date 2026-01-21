from __future__ import annotations

import asyncio
import threading
import tkinter as tk
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ai.chat import AIChat
    from pets.cat import CatPet


class ChatWindow:
    """Chat window for talking to the virtual pet using AI."""

    def __init__(self, pet: CatPet, ai: AIChat) -> None:
        self.pet = pet
        self.current_sprite = self.sprites.get_sprite('walking')  # Set initial sprite
        self.sprites = Sprites()  # Initialize sprites for animations
        self.sprites = Sprites()  # Initialize sprites for animations
        self.ai = ai

        self.win = tk.Toplevel()
        self.current_sprite = self.sprites.get_sprite('walking')  # Set initial sprite
        self.win.title(f"Talk to {pet.name}")
        self.win.geometry("400x500")
        self.win.attributes("-topmost", True)

        # Chat display

    def on_drag(self):
        self.current_sprite = self.sprites.get_sprite('picked_up')  # Change sprite when dragged

    def on_sleep(self):
        self.current_sprite = self.sprites.get_sprite('sleeping')  # Change sprite when sleeping
        self.text = tk.Text(self.win, state="disabled", wrap="word")
        self.text.pack(expand=True, fill="both", padx=5, pady=5)

        # Input field
        self.entry = tk.Entry(self.win)
        self.entry.pack(fill="x", padx=5, pady=5)
        self.entry.bind("<Return>", self.send)
        self.win.bind("<Button-3>", self.show_context_menu)  # Right-click for context menu
        self.entry.focus()

        # Welcome message

    def show_context_menu(self, event):
        menu = tk.Menu(self.win, tearoff=0)
        menu.add_command(label="Sleep", command=self.on_sleep)
        menu.post(event.x_root, event.y_root)  # Show menu at cursor position
        self.write(self.pet.name, f"Meow! I'm {self.pet.name}. What's up?")

    def write(self, who: str, msg: str) -> None:
        """Write a message to the chat display."""
        self.text.config(state="normal")
        self.text.insert("end", f"{who}: {msg}\n\n")
        self.text.config(state="disabled")
        self.text.see("end")

    def send(self, event: tk.Event[Any] | None = None) -> None:
        """Send user message and get AI response."""
        msg = self.entry.get().strip()
        if not msg:
            return

        self.entry.delete(0, "end")
        self.write("You", msg)

        # Show typing indicator
        self.entry.config(state="disabled")
        self.entry.insert(0, f"{self.pet.name} is typing...")

        def run() -> None:
            """Run async AI chat in background thread."""
            try:
                reply = asyncio.run(
                    self.ai.ask(
                        self.pet.personality,
                        msg,
                        {
                            "hunger": self.pet.hunger,
                            "happiness": self.pet.happiness,
                            "energy": self.pet.energy,
                            "mood": self.pet.mood(),
                        },
                    )
                )
                # Schedule GUI update in main thread
                self.win.after(0, lambda: self._show_reply(reply))
            except Exception as e:
                self.win.after(0, lambda: self._show_reply(f"*meow?* (Error: {e})"))

        threading.Thread(target=run, daemon=True).start()

    def _show_reply(self, reply: str) -> None:
        """Show AI reply and re-enable input (must run in main thread)."""
        self.write(self.pet.name, reply)
        self.entry.config(state="normal")
        self.entry.delete(0, "end")
        self.entry.focus()