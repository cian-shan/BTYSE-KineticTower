from pickle import NONE
import board, neopixel, time
import RPi.GPIO as GPIO
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.comet import Comet
import adafruit_led_animation.color as color
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation import helper
from led_power_level import PowerLevel
from player import Player
from pixel_maps import KTPixelMap
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import subprocess

STANDBY = 0
COUNTDOWN = 1
IN_GAME = 2
RESULTS = 3
FULL_BRIGHTNESS = .1
LED_COUNT = 1082
LED_HEIGHT = 180
   
class KineticTowerGame:
        

    def __init__(
            self,
            game_start_pin = 23,
            game_status = STANDBY,
            p1_energy = 0,
            p2_energy = 0,
            tot_energy = 0,
            winner = NONE,
            not_winner = NONE
        ):

        self.game_start_pin = game_start_pin
        self.game_status    = game_status
        self.p1_energy   = p1_energy
        self.p2_energy   = p2_energy
        self.tot_energy      = tot_energy
        self.winner         = winner
        self.not_winner     = not_winner
    
    def game_start_button_callback(self, game):
        """
        Function runs on Game Start/End button press.
        game_start boolean is used to start/stop the game
        """
        if not GPIO.input(self.game_start_pin):
            if self.game_status == STANDBY:
                print("Game Start Button Pressed")
                self.game_status = COUNTDOWN
            else:
                print("Game Ended with button press")
                self.game_status = STANDBY

    def show_results(self):
        result_leds = AnimationGroup(
            Blink(self.winner.pixel_map, speed=0.3, color=color.GREEN),
            Solid(self.not_winner.pixel_map, color.BLACK)
        )
        print("Game over!")
        print("Winner :", self.winner.player_ID)
        for i in range(10):
            result_leds.animate()
            time.sleep(1)
        self.game_status = STANDBY
        pass
           


if __name__=="__main__":
    print("Kinetic Tower Starting")

    ## Setup Power Sensors
    i2c_bus = board.I2C()

    p1_ina219 = INA219(i2c_bus, addr = 0x40)
    p2_ina219 = INA219(i2c_bus, addr = 0x44)

    p1_ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p1_ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p1_ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

    p2_ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p2_ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p2_ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

    # Create Strip Objects 
    p1 = Player(player_ID= 1, input_pin=24, power_sensor=p1_ina219)
    p2 = Player(player_ID= 2, input_pin=25, power_sensor=p2_ina219)

    game = KineticTowerGame()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(game.game_start_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(p1.input_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(p2.input_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(game.game_start_pin, GPIO.FALLING, callback= game.game_start_button_callback, bouncetime=100)
    GPIO.add_event_detect(p1.input_pin, GPIO.FALLING, callback= p1.button_power_gen, bouncetime=200)
    GPIO.add_event_detect(p2.input_pin, GPIO.FALLING, callback= p2.button_power_gen, bouncetime=200)

    pixels = neopixel.NeoPixel(pin=board.D18, n=LED_COUNT, brightness=FULL_BRIGHTNESS, auto_write=True)
    
    p1_pixel_map = helper.PixelMap(pixels, KTPixelMap.p1_pixel_map_strips, individual_pixels=True)
    p2_pixel_map = helper.PixelMap(pixels, KTPixelMap.p2_pixel_map_strips, individual_pixels=True)

    standby_leds = AnimationGroup(
        Rainbow(p1_pixel_map, .1, 10),
        Rainbow(p2_pixel_map, .1, 10)
        )

    clear_leds = AnimationGroup(Solid(p1_pixel_map, color.BLACK), Solid(p2_pixel_map, color.BLACK))

    p1_game_leds = PowerLevel(p1_pixel_map, color.PURPLE, max_height=LED_HEIGHT)
    p2_game_leds = PowerLevel(p2_pixel_map, color.BLUE, max_height=LED_HEIGHT)

    countdown_leds = AnimationSequence(
        Solid(pixels, color.RED),
        Solid(pixels, color.ORANGE),
        Solid(pixels, color.YELLOW),
        Solid(pixels, color.BLACK),
    )

    test_leds = AnimationGroup(
        Blink(p1_pixel_map, speed=0.3, color=color.RED),
        Blink(p2_pixel_map, speed=0.3, color=color.GREEN)
        )

    game_leds = AnimationGroup(p1_game_leds, p2_game_leds)

    p1.add_leds(p1_game_leds, p1_pixel_map)
    p2.add_leds(p2_game_leds, p2_pixel_map)

    while True:

        clear_leds.animate()
        
        if game.game_status == STANDBY:
            # Set all LEDs to Standby Animation
            #standby.animate()
            clear_leds.animate()
            # Set players back to start
            print("Entering Standby")
            #standby_proc.run
            while  game.game_status == STANDBY:
                standby_leds.animate()
                #test_leds.animate()
                pass
            p1.reset()
            p2.reset()
            pass

        elif game.game_status == COUNTDOWN:
            # Set all LEDs to Countdown
            print("Countdown!")
            game.game_status = IN_GAME
            for i in range(4):
                countdown_leds.activate(i)
                countdown_leds.animate()
                time.sleep(1)
                print(i)
            countdown_leds.freeze()
            pass
            
        elif game.game_status == IN_GAME:
            print("In Game")
            clear_leds.animate()

            while game.game_status == IN_GAME:
                # Waits in loop as interrupts trigger while game is played
                game_leds.animate()
                p2.ina219_pwr_gen()
                p1.ina219_pwr_gen()
                

                #check for winner
                if p2.energy_gen > LED_HEIGHT:
                    game.winner = p2
                    game.not_winner = p1
                    game.tot_energy =  p1.energy_gen + p2.energy_gen
                    game.game_status = RESULTS
                elif p1.energy_gen > LED_HEIGHT:
                    game.winner = p1
                    game.not_winner = p2
                    game.tot_energy =  p1.energy_gen + p2.energy_gen
                    game.game_status = RESULTS
                pass

        elif game.game_status == RESULTS:
            print("Show Results")
            while game.game_status == RESULTS:
                game.show_results()
                pass
        else:
            print("Exit Program - should not be reached")
        


    