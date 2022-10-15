from adafruit_led_animation.animation import Animation

class PowerLevel(Animation):


    def __init__(self, pixel_object, color, level=0, name=None):
        self._num_pixels = len(pixel_object)
        self.level = level
        super().__init__(pixel_object, speed=1, color=color, name=name)


    def update_level(self, new_level):
        self.level = new_level       

    def reset(self):
        return super().reset()

    def draw(self):
        self.pixel_object[(self._num_pixels-1) - self.level] = self.color
