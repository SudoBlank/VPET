"""Create placeholder sprites for all pets with all emotion states."""

from PIL import Image, ImageDraw
from pathlib import Path

# Create directories if they don't exist
Path("assets/dogs").mkdir(parents=True, exist_ok=True)
Path("assets/anime_girl").mkdir(parents=True, exist_ok=True)

def create_placeholder_sprite(color, size=128):
    """Create a simple colored circle as placeholder sprite."""
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple circle
    draw.ellipse([10, 10, size-10, size-10], fill=color, outline="black", width=2)
    
    return img

# Emotion colors for consistency
emotion_colors = {
    "happy": (255, 200, 100, 255),      # Orange
    "sad": (100, 150, 255, 255),        # Blue
    "angry": (255, 100, 100, 255),      # Red
    "shy": (200, 100, 200, 255),        # Purple
    "sleeping": (150, 200, 255, 255),   # Light Blue
    "picked_up": (255, 255, 100, 255),  # Yellow
    "grabed": (255, 255, 100, 255),     # Yellow (same as picked_up)
    "tickling": (255, 150, 200, 255),   # Pink
    "walking": (150, 255, 150, 255),    # Green
}

# Create dog sprites
print("Creating dog sprites...")
for emotion, color in emotion_colors.items():
    img = create_placeholder_sprite(color)
    filepath = f"assets/dogs/dog_{emotion}.png"
    img.save(filepath)
    print(f"  Created {filepath}")

# Create anime_girl sprites
print("Creating anime_girl sprites...")
for emotion, color in emotion_colors.items():
    img = create_placeholder_sprite(color)
    filepath = f"assets/anime_girl/anime_girl_{emotion}.png"
    img.save(filepath)
    print(f"  Created {filepath}")

print("\nSprite creation complete!")
print("Note: These are placeholder sprites. Replace them with actual artwork.")

