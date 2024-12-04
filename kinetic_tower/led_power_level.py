from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.blink import Blink
import adafruit_led_animation.color as color
import board
import neopixel

class PowerLevel(Animation):
    """
    This function is an abstraction of the Animation Class. 
    It controls the level of the LEDs
    """
    
    def __init__(self, pixel_object, color, max_height, level=0, name=None):
        self._num_pixels = len(pixel_object)
        self.max_height = max_height
        self.level = level
        super().__init__(pixel_object, speed=0.05, color=color, name=name)  # Lower speed value for faster animation

    def update_level(self, new_level):
        self.level = new_level 

    def reset(self):
        self.level = 0
        return super().reset()

    def draw(self):
        if self.level <= self.max_height:
            fill_level = [self.color] * (self.level + 1)
            self.pixel_object[-(self.level + 1):] = fill_level
        else:
            self.pixel_object[-self.max_height:] = [self.color] * self.max_height
