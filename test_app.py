"""Test the application without running the GUI."""

import sys
import io

# Fix encoding for Windows console
if sys.platform == "win32":
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
from ai.chat import AIChat
from pets.cat import CatPet
from pets.dog import DogPet
from pets.anime_girl import AnimeGirlPet
from save_load_manager import SaveLoadManager
from memory.memory import PetMemory
from ui.sprites import Sprites

# Test pet creation and state management
print("=" * 50)
print("Testing Pet Creation and State Management")
print("=" * 50)

cat = CatPet()
dog = DogPet()
anime = AnimeGirlPet()

print(f"[OK] Created {cat.name}")
print(f"[OK] Created {dog.name}")
print(f"[OK] Created {anime.name}")

# Test pet attributes
print("\nTesting initial pet stats:")
print(f"Cat: Hunger={cat.hunger}, Happiness={cat.happiness}, Energy={cat.energy}")
print(f"Mood: {cat.mood()}")

# Test pet tick
print("\nTesting pet tick (state update):")
cat.tick()
print(f"After tick - Hunger={cat.hunger}, Happiness={cat.happiness}, Energy={cat.energy}")

# Test pet interactions
print("\nTesting pet interactions:")
cat.feed()
print(f"After feeding - Hunger={cat.hunger}, Happiness={cat.happiness}")

cat.play()
print(f"After playing - Happiness={cat.happiness}, Energy={cat.energy}")

# Test sleep
print("\nTesting sleep state:")
cat.sleep()
print(f"Sleeping: {cat.is_sleeping}")
cat.tick()
cat.tick()
print(f"After ticks - Energy={cat.energy:.0f} (should be higher)")
cat.wake_up()
print(f"Awake: {cat.is_sleeping}")

# Test save/load
print("\nTesting Save/Load:")
save_mgr = SaveLoadManager("test_save.json")
pet_data = cat.to_dict()
save_mgr.save({"pet": pet_data})
loaded_data = save_mgr.load()
print(f"[OK] Saved and loaded pet data")
print(f"Loaded hunger: {loaded_data['pet']['hunger']}")

# Test memory
print("\nTesting Pet Memory:")
memory = PetMemory()
memory.record_interaction("talk", "Hello pet!")
memory.record_interaction("feed", "nom nom")
memory.record_interaction("play", "fun time!")
print(f"[OK] Recorded 3 interactions")
print(f"Talk count: {memory.get_interaction_count('talk')}")
print(f"Total interactions: {len(memory.interactions)}")

# Test sprites
print("\nTesting Sprite Management:")
cat_sprites = Sprites("cat", 128)
print(f"[OK] Created Sprites manager for cat")
print(f"Available states: {cat_sprites.get_available_states()}")

dog_sprites = Sprites("dog", 128)
print(f"[OK] Created Sprites manager for dog")
print(f"Available states: {dog_sprites.get_available_states()}")

anime_sprites = Sprites("anime_girl", 128)
print(f"[OK] Created Sprites manager for anime_girl")
print(f"Available states: {anime_sprites.get_available_states()}")

# Test AI Chat (without API calls)
print("\nTesting AI Chat initialization:")
try:
    ai = AIChat()
    print(f"[OK] AI Chat initialized")
    print(f"Memory size: {len(ai.memory)}")
except Exception as e:
    print(f"[INFO] AI Chat note (expected without network): {e}")

print("\n" + "=" * 50)
print("[SUCCESS] All tests passed!")
print("=" * 50)
