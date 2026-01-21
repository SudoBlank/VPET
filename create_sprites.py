"""Create placeholder sprites for all pets."""

from PIL import Image, ImageDraw
from pathlib import Path

# Create directories if they don't exist
Path("assets/dogs").mkdir(parents=True, exist_ok=True)
Path("assets/anime_girl").mkdir(parents=True, exist_ok=True)

def create_placeholder_sprite(color, name, size=128):
    """Create a simple colored square with text as placeholder sprite."""
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple circle
    draw.ellipse([10, 10, size-10, size-10], fill=color, outline="black", width=2)
    
    return img

# Create dog sprites
dog_happy = create_placeholder_sprite((255, 200, 100, 255), "Dog Happy")
dog_happy.save("assets/dogs/dog_happy.png")

dog_sad = create_placeholder_sprite((200, 150, 100, 255), "Dog Sad")
dog_sad.save("assets/dogs/dog_sad.png")

dog_angry = create_placeholder_sprite((255, 100, 100, 255), "Dog Angry")
dog_angry.save("assets/dogs/dog_angry.png")

dog_sleeping = create_placeholder_sprite((150, 200, 255, 255), "Dog Sleep")
dog_sleeping.save("assets/dogs/dog_sleeping.png")

dog_picked = create_placeholder_sprite((255, 255, 100, 255), "Dog Picked")
dog_picked.save("assets/dogs/dog_picked_up.png")

# Create anime_girl sprites
anime_happy = create_placeholder_sprite((255, 150, 200, 255), "Anime Happy")
anime_happy.save("assets/anime_girl/anime_girl_happy.png")

anime_sad = create_placeholder_sprite((200, 100, 150, 255), "Anime Sad")
anime_sad.save("assets/anime_girl/anime_girl_sad.png")

anime_angry = create_placeholder_sprite((255, 100, 150, 255), "Anime Angry")
anime_angry.save("assets/anime_girl/anime_girl_angry.png")

anime_sleeping = create_placeholder_sprite((150, 150, 255, 255), "Anime Sleep")
anime_sleeping.save("assets/anime_girl/anime_girl_sleeping.png")

anime_picked = create_placeholder_sprite((255, 200, 200, 255), "Anime Picked")
anime_picked.save("assets/anime_girl/anime_girl_picked_up.png")

print("✓ Created all placeholder sprites!")
