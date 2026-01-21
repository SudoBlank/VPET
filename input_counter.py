from pynput import keyboard, mouse

class GlobalInputCounter:
    def __init__(self, callback):
        self.count = 0
        self.callback = callback

        keyboard.Listener(on_press=self.on_key).start()
        mouse.Listener(on_click=self.on_click).start()

    def on_key(self, key):
        self.count += 1
        self.callback(self.count)

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.count += 1
            self.callback(self.count)
