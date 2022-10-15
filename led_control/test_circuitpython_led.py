import board
import neopixel
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.comet import Comet
import adafruit_led_animation.color as color

# Works on Circuit Playground Express and Bluefruit.
# For other boards, change board.NEOPIXEL to match the pin to which the NeoPixels are attached.
pixel_pin = board.D18
# Change to match the number of pixels you have attached to your board.
num_pixels = 150

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.5)
blink = Blink(pixels, 1, color.PURPLE)
rainbow = Rainbow(pixels, speed=.075, period=5, step=1)
comet = Comet(pixels, speed=0.1, tail_length=5, reverse=False, color=color.AMBER, bounce=True)

while True:
    # blink.animate()
    # rainbow.animate()
    comet.animate()

