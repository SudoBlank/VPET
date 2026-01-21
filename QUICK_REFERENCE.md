# VPET Quick Reference Guide

## Application Overview
Virtual Pet (VPET) is a desktop application featuring interactive virtual pets with AI chat, animations, and persistent state.

## Quick Start
```bash
python app.py
```

## File Changes Summary

### Critical Fixes Made
1. **ui/chat_window.py** - Fixed completely broken constructor with incorrect variable ordering
2. **settings/manager.py** - Removed duplicate _load() method definition
3. **ui/window.py** - Removed duplicate VPetWindow class definition
4. **app.py** - Fixed initialization order (AI before Window)

### New Files Created
1. **ui/sprites.py** - Complete sprite management system
2. **memory/memory.py** - Pet memory and interaction tracking
3. **save_load_manager.py** - Application state persistence
4. **create_sprites.py** - Sprite asset generation utility
5. **test_app.py** - Comprehensive test suite
6. **FEATURES.py** - Feature showcase
7. **IMPLEMENTATION_SUMMARY.md** - Complete implementation details

### Enhanced Files
1. **pets/base.py** - Added sleep state, serialization, mood system
2. **pets/cat.py** - Already working
3. **pets/dog.py** - Implemented
4. **pets/anime_girl.py** - Implemented
5. **ui/window.py** - Enhanced with drag/drop, sprite management
6. **ui/chat_window.py** - Fixed and enhanced
7. **settings/manager.py** - Fixed duplicates and enhanced

## Key Features

### Pet Management
- **3 Pet Types**: Cat, Dog, Anime Girl
- **State Tracking**: Hunger, Happiness, Energy (0-100)
- **Sleep System**: Pet can sleep to restore energy
- **Mood System**: Happy, Sad, Angry, Sleeping
- **Serialization**: Save/load pet state

### Sprites
- **Happy sprite** - When pet is content
- **Sad sprite** - When pet is unhappy
- **Angry sprite** - When pet is very hungry
- **Sleeping sprite** - When pet is sleeping
- **Picked-up sprite** - When dragging pet

### Interactions
- **Feed** - Reduces hunger, increases happiness
- **Play** - Increases happiness, uses energy
- **Sleep** - Restores energy (right-click menu)
- **Talk** - Chat with AI (requires API key)

### UI Elements
- **Main Window** - Always on top, transparent, draggable
- **Settings Window** - Full configuration
- **Chat Window** - AI conversation interface
- **Context Menu** - Right-click for quick actions
- **Stats Display** - View pet statistics

## Controls

### Mouse
- **Left Click + Drag** - Move pet around screen
- **Right Click** - Show context menu

### Context Menu Options
1. Talk - Open chat window
2. Feed - Feed the pet
3. Play - Play with pet
4. Sleep - Make pet sleep
5. Stats - View statistics
6. Settings - Open settings
7. Quit - Exit application

## Settings Available
- **Always on top** - Keep window on top
- **Transparent** - Transparent window background
- **Pet Scale** - Resize pet (0.5x - 2.0x)
- **Roam Interval** - Pet roaming frequency (10-120s)
- **AI Enabled** - Enable/disable AI chat
- **Reset Stats** - Reset pet to default state

## API Configuration
Create/edit `config.json`:
```json
{
  "openrouter_api_key": "your-key-here",
  "model": "mistralai/mistral-7b-instruct",
  "max_tokens": 200,
  "temperature": 1.0
}
```

## Troubleshooting

### PIL/Pillow Errors
```bash
pip install Pillow
```

### Import Errors
Verify all files exist in correct directories:
- `ai/chat.py`, `ai/personalities.py`
- `pets/base.py`, `pets/cat.py`, `pets/dog.py`, `pets/anime_girl.py`
- `ui/window.py`, `ui/chat_window.py`, `ui/setings_window.py`, `ui/sprites.py`
- `settings/manager.py`
- `memory/memory.py`
- `save_load_manager.py`

### Sprites Not Loading
Sprites are optional - application will use placeholder graphics if sprite files aren't found.

## Testing
```bash
# Run comprehensive tests
python test_app.py

# Show features
python FEATURES.py
```

## Architecture

### Class Hierarchy
```
VirtualPet (base.py)
├── CatPet
├── DogPet
└── AnimeGirlPet

VPetWindow (main window)
├── VirtualPet instance
├── AIChat instance
├── Settings instance
└── Sprites instance

ChatWindow (conversation)
├── VirtualPet reference
└── AIChat reference

SettingsWindow (configuration)
└── Settings instance
```

### Data Flow
```
app.py
  ├─> CatPet()
  ├─> AIChat()
  ├─> SaveLoadManager()
  └─> VPetWindow()
        ├─> Sprites()
        ├─> Settings()
        └─> UI Loop
```

## Performance Notes
- Tick interval: 5 seconds (configurable)
- Roam interval: 30 seconds (configurable)
- Animation refresh: ~30ms per frame
- Memory usage: ~50-100MB typically

## Known Limitations
- Sprite assets need to be provided by user
- Placeholder sprites are simple colored circles
- AI requires internet connection for API calls
- Window always stays above taskbar on Windows

## Future Enhancement Ideas
- Pet customization (colors, accessories)
- Mini-games
- Multiple pets on screen
- Leveling/experience system
- Pet breeding
- Inventory system
- More detailed animation frames
- Sound effects and music
- Mobile companion app

---
**Version**: 0.1
**Status**: Fully Functional
**Last Updated**: January 21, 2026
