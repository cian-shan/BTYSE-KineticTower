from adafruit_led_animation.animation import Animation
from adafruit_led_animation.animation.blink import Blink
import adafruit_led_animation.color as color


class GameWinLevel(Animation):
    """
    This function is an abstraction of the Animation Class. 
    It controls the level of the LEDs

    """
    
    def __init__(self, pixel_object, color, max_height, level=0, name=None):
        self._num_pixels = len(pixel_object)
        self.max_height = max_height
        self.level = level
        super().__init__(pixel_object, speed=1, color=color, name=name)

    def update_gamewinlevel(self, new_level):
        self.level = new_level 

    def reset(self):
        self.level = 0
        return super().reset()

    def draw(self):
        # print("LEVEL: ", self.level)
        fill_level = [self.color for i in range(self.level + 1)]
        self.pixel_object[self.level] = [self.color, self.color, self.color]


                # def activate_countdown_leds(level):
                #     for i in range(level):
                #         if i < len(KTPixelMap.p1_pixel_map_strips):
                #             pixels[KTPixelMap.p1_pixel_map_strips[i]] = color.GREEN
                #             if i < len(KTPixelMap.p2_pixel_map_strips):
                #                 pixels[KTPixelMap.p2_pixel_map_strips[i]] = color.GREEN
                #                 activate_countdown_leds(GAME_WIN_LEVEL)