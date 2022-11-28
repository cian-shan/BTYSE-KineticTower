import time
from select import select


class LedSupport:
    def __init__(self, np, led_count, pin):
        self.led_count = led_count
        self.pin = pin
        self.np = np

    def set_color(self, r, g, b):
        for i in range(self.led_count):
            self.np[i] = (r, g, b)

    def clear(self):
        for i in range(self.led_count):
            self.np[i] = (0, 0, 0)

    def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def rainbow_cycle(self, wait):
        while True:
            for j in range(255):
                for i in range(self.led_count):
                    rc_index = (i * 256 // self.led_count) + j
                    self.np[i] = LedSupport.wheel(rc_index & 255)
