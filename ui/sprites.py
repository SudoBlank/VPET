# Sprites for different animations

class Sprites:
    def __init__(self):
        self.walking_sprite = "path/to/walking_sprite.png"
        self.picked_up_sprite = "path/to/picked_up_sprite.png"
        self.sleeping_sprite = "path/to/sleeping_sprite.png"

    def get_sprite(self, state):
        if state == 'walking':
            return self.walking_sprite
        elif state == 'picked_up':
            return self.picked_up_sprite
        elif state == 'sleeping':
            return self.sleeping_sprite
        return None
