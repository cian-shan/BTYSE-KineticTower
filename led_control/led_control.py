import board, neopixel, sys, time, signal
import RPi.GPIO as GPIO
from multiprocessing import Process
from led_support import LedSupport
#from pixel_maps import PixelMaps

led_count = 180
pin = board.D18     #GPIO for LED control

class LedStrip():

    def __init__(
        self,
        led_count = 180,
        led_pin = board.D18
            ):
        self.led_count = led_count
        self.led_pin = led_pin
        pass

class KineticTowerGame():

    def __init__(
        self,
        game_start_pin = 23,
        power_gen_pin = 24,
        program_exit = False,
        game_start = False,
        game_active = False,
        p1_tot_power = 0,
        game_leds = [],
        ):
        
        self.game_start_pin = game_start_pin
        self.power_gen_pin  = power_gen_pin 
        self.program_exit   = program_exit  
        self.game_start     = game_start    
        self.game_active    = game_active   
        self.p1_tot_power   = p1_tot_power  
        self.game_leds      = game_leds     
        pass


        

def game_start_button_callback(game):
    """
    Function runs on Game Start/End button press.
    game_start boolean is used to start/stop the game
    """
    if not GPIO.input(game.game_start_pin):
        if not game.game_start:
            print("Game Start")
            game.game_start = True
            pass
        else:
            print("Game End")
            game.game_start = False
            game.p1_tot_power = 0


def power_gen_button_callback(game):
    """
    Function Runs as Power Generation Button pressed
    Increments LED index, LEDs are illuminated. 
    """
    if game.game_active:
        if not GPIO.input(game.power_gen_pin):      
            game.p1_tot_power += 1
            try:
                # Next LED indexed as power generated
                np[game.p1_tot_power-1] = (0,255,0)
                print("1W generated! ", game.p1_tot_power )
            except:
                print("WINNER!! 20W produced")
                for i in range(2):
                    print("flash")
                    np.fill([0,255,0])
                    time.sleep(0.2)

                game.game_start = False
                game.game_active = False

            # game_leds.append((0,255,0))
        else:
            print("Button Released")
    

# Run Standby Animations
def standby(self):
    """
    Runs standby animation
    """
    print("Standby")
    #support.set_color(255,0,0)
    support.rainbow_cycle(5)
    pass

# Game Countdown function
def game_countdown(self):
    """
    Runs Game countdown animation. LEDs flash during countdown
    """
    wait = 0.75
    # RED
    np.fill([255,0,0])
    time.sleep(wait)

    #ORANGE
    np.fill([255,50,0])
    time.sleep(wait)

    #YELLOW
    np.fill([255,255,0])
    time.sleep(wait)

    #GREEN 
    np.fill([0,255,0])
    time.sleep(wait)

    support.clear()

def run_game(self, game):
    """
    Waits inside function for Gameplay to finish once player generates enough power

    """

    print("Converting values to LEDS")
    game.game_leds.clear()
    game.game_active = True
    while game.game_start:
        pass

    game.p1_tot_power = 0           

# Defining main function
def main(game):
    """
    Main loop: Game should not return from this function
    """
    
    while not game.program_exit:
        # Standby process allows standby to run as background process
        standby_proc = Process(target=standby)

        while not game.game_start:
            if not standby_proc.is_alive():
                print("Start Standby Proc")
                print(game)
                standby_proc.start()

        standby_proc.terminate()
        game_countdown()
        run_game(game)

        print("End Game Session")        
            
    print("Program Exit")
  

if __name__=="__main__":

    np = neopixel.NeoPixel(pin, led_count, brightness=1)
    support = LedSupport(np, led_count, pin)
    # standby_proc = Process(target=standby)

    support.clear()

    game = KineticTowerGame()
    strip_1 = LedStrip()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(game.game_start_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(game.power_gen_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(game.game_start_pin, GPIO.FALLING, callback=lambda x: game_start_button_callback(game), bouncetime=100)
    GPIO.add_event_detect(game.power_gen_pin, GPIO.FALLING, callback=lambda x: power_gen_button_callback(game), bouncetime=100)

    # signal.signal(signal.SIGINT, button_press_handler)
    

    main(game)