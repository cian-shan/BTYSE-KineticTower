from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.blink import Blink
import adafruit_led_animation.color as color

class PowerLevel(Animation):


    def __init__(self, pixel_object, color, max_height, level=0, name=None):
        self._num_pixels = len(pixel_object)
        self.max_height = max_height
        self.level = level
        super().__init__(pixel_object, speed=1, color=color, name=name)


    def update_level(self, new_level):
        self.level = new_level       

    def reset(self):
        self.level = 0
        return super().reset()

    def draw(self):
        print("LEVEL: ", self.level)
        if self.level <= self.max_height:
            fill_level = [self.color for i in range(self.level+1)]       
            self.pixel_object[((self._num_pixels-1) - self.level):] = fill_level
    
