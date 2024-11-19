from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.blink import Blink
import adafruit_led_animation.color as color


class PowerLevel(Animation):
    """
    This function is an abstraction of the Animation Class. 
    It controls the level of the LEDs

    """
    
    def __init__(self, pixel_object, color, max_height, level=0, name=None):
        self._num_pixels = len(pixel_object)
        self.max_height = max_height
        self.level = level
        super().__init__(pixel_object, speed=1, color=color, name=name)

    def update_level(self,new_level):
        self.level = new_level 

    def reset(self):
        self.level = 0
        return super().reset()

    def draw(self):
        print("LEVEL: ", self.level)
        if self.level < self.max_height:
            fill_level = [self.color for i in range(self.level)]
            black_level = [color.MAGENTA for i in range(self.max_height - self.level)]

            black_level.extend(fill_level)
            print(f"fill len {len(fill_level)} - black {len(black_level)}")
            print(fill_level)
            self.pixel_object[:] = black_level

            

        else:
            max_level = [self.color] * 180
            self.pixel_object[:] = max_level
