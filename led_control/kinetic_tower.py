from turtle import update
import board, neopixel, time
import RPi.GPIO as GPIO
from multiprocessing import Process
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.comet import Comet
import adafruit_led_animation.color as color
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation import helper

# from led_control import standby
from led_power_level import PowerLevel

STANDBY = 0
COUNTDOWN = 1
IN_GAME = 2
RESULTS = 3
FULL_BRIGHTNESS = 1 
LED_COUNT = 256
LED_HEIGHT = 31
   
class KineticTowerGame:
        

    def __init__(
            self,
            game_start_pin = 23,
            game_status = STANDBY,
            p1_tot_power = 0,
            p2_tot_power = 0,
            tot_power = 0,
        ):

        self.game_start_pin = game_start_pin
        self.game_status    = game_status
        self.p1_tot_power   = p1_tot_power
        self.p2_tot_power   = p2_tot_power
        self.tot_power      = tot_power
    
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

    """
    def countdown(self, leds):
        print("Countdown Started")

        print("3")
        red = Solid(leds, color.RED)
        red.animate()
        time.sleep(.5)
        print("2")
        orange = Solid(leds, color.ORANGE)
        orange.animate()
        time.sleep(.5)
        print("1")
        yellow = Solid(leds, color.YELLOW)
        yellow.animate()
        time.sleep(.5)
        yellow.fill((0,0,0))
        self.game_status = IN_GAME
    """

    def show_results(self):
        pass
        


class Player():

    def __init__(self, player_ID, input_pin, player_leds=None, tot_pwr_gen=0 ):
        self.player_ID = player_ID
        self.input_pin = input_pin
        self.player_leds = None
        self.tot_pwr_gen = tot_pwr_gen

    def reset(self):
        self.tot_pwr_gen = 0
        self.player_leds.reset()

    def add_leds(self, leds):
        self.player_leds = leds

    #def update_leds(self, level):
    #    """ Updates LEDs to reflect total power generated """

    def power_gen(self, player):
        """
        Function Runs as Power Generation Button pressed
        Increments LED index, LEDs are illuminated. 
        """
        if not GPIO.input(self.input_pin):
            self.tot_pwr_gen += 1
            self.player_leds.update_level(self.tot_pwr_gen)
            print("Player: %d - Power Gen: %d " % (self.player_ID, self.tot_pwr_gen))

    def get_pwr_gen(self):
        return self.tot_pwr_gen
            


if __name__=="__main__":
    print("Kinetic Tower Starting")

    # Create Strip Objects 
    p1 = Player(player_ID= 1, input_pin=24)
    p2 = Player(player_ID= 2, input_pin=25)

    game = KineticTowerGame()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(game.game_start_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(p1.input_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(p2.input_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(game.game_start_pin, GPIO.FALLING, callback= game.game_start_button_callback, bouncetime=100)
    GPIO.add_event_detect(p1.input_pin, GPIO.FALLING, callback= p1.power_gen, bouncetime=200)
    GPIO.add_event_detect(p2.input_pin, GPIO.FALLING, callback= p2.power_gen, bouncetime=200)

    pixels = neopixel.NeoPixel(pin=board.D18, n=LED_COUNT, brightness=.1, auto_write=True)
    
    p1_pixel_map = helper.PixelMap(pixels, individual_pixels=True, 
    pixel_ranges = [
        (255,254,253,252),(240,241,242,243),
        (239,238,237,236),(224,225,226,227),
        (223,222,221,220),(208,209,210,211),
        (207,206,205,204),(192,193,194,195),
        (191,190,189,188),(176,177,178,179),
        (175,174,173,172),(160,161,162,163),
        (159,158,157,156),(144,145,146,147),
        (143,142,141,140),(128,129,130,131),
        (127,126,125,124),(112,113,114,115),
        (111,110,109,108),(96,97,98,99),
        (95,94,93,92),(80,81,82,83),
        (79,78,77,76),(64,65,66,67),
        (63,62,61,60),(48,49,50,51),
        (47,46,45,44),(32,33,34,35),
        (31,30,29,28),(16,17,18,19),
        (15,14,13,12),(0,1,2,3)
    ])
    p2_pixel_map = helper.PixelMap(pixels, individual_pixels=True, 
    pixel_ranges=[
        (251,250,249,248),(244,245,246,247),
        (235,234,233,232),(228,229,230,231),
        (219,218,217,216),(212,213,214,215),
        (203,202,201,200),(196,197,198,199),
        (187,186,185,184),(180,181,182,183),
        (171,170,169,168),(164,165,166,167),
        (155,154,153,152),(148,149,150,151),
        (139,138,137,136),(132,133,134,135),
        (123,122,121,120),(116,117,118,119),
        (107,106,105,104),(100,101,102,103),
        (91,90,89,88),(84,85,86,87),
        (75,74,73,72),(68,69,70,71),
        (59,58,57,56),(52,53,54,55),
        (43,42,41,40),(36,37,38,39),
        (27,26,25,24),(20,21,22,23),
        (11,10,9,8),(4,5,6,7)
        ])

    

    standby = AnimationGroup(
        #Comet(p1_pixel_map, 0.5,color.MAGENTA, 5),
        #Comet(p2_pixel_map, 0.5,color.CYAN, 5, reverse=True)
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
    
    game_leds = AnimationGroup(p1_game_leds, p2_game_leds)

    p1.add_leds(p1_game_leds)
    p2.add_leds(p2_game_leds)

    while True:

        clear_leds.animate()
        
        """
        for i in range(32):
            p1_game_leds.update_level(i)
            p2_game_leds.update_level(i)
            game_leds.animate()
            time.sleep(1)
        """ 
        
        if game.game_status == STANDBY:
            # Set all LEDs to Standby Animation
            #standby.animate()
            clear_leds.animate()
            # Set players back to start 
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
                pass

        elif game.game_status == RESULTS:
            print("Show Results")
            while game.game_status == RESULTS:
                game.show_results()
                pass
        else:
            print("Exit Program - should not be reached")
        


    