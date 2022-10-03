import board, neopixel, sys, time, signal
import RPi.GPIO as GPIO
from multiprocessing import Process
from led_support import LedSupport

led_count = 20
pin = board.D18     #GPIO for LED control

game_start_pin = 23
power_gen_pin = 24

program_exit = False
game_start = False
game_active = False

p1_tot_power = 0
game_leds = []
        

def game_start_button_callback(self):
    """
    Function runs on Game Start/End button press.
    game_start boolean is used to start/stop the game
    """
    global game_start
    global p1_tot_power
    if not GPIO.input(game_start_pin):
        if not game_start:
            print("Game Start")
            game_start = True
            pass
        else:
            print("Game End")
            game_start = False
            p1_tot_power = 0


def power_gen_button_callback(self):
    """
    Function Runs as Power Generation Button pressed
    Increments LED index, LEDs are illuminated. 
    """
    global p1_tot_power
    global game_start
    global game_active
    if game_active:
        if not GPIO.input(power_gen_pin):      
            p1_tot_power += 1
            try:
                # Next LED indexed as power generated
                np[p1_tot_power-1] = (0,255,0)
                print("1W generated! ",p1_tot_power )
            except:
                print("WINNER!! 20W produced")
                for i in range(2):
                    print("flash")
                    np.fill([0,255,0])
                    time.sleep(0.2)

                game_start = False
                game_active = False

            # game_leds.append((0,255,0))
        else:
            print("Button Released")
    

# Run Standby Animations
def standby():
    """
    Runs standby animation
    """
    print("Standby")
    #support.set_color(255,0,0)
    support.rainbow_cycle(5)
    pass

# Game Countdown function
def game_countdown():
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

def run_game():
    """
    Waits inside function for Gameplay to finish once player generates enough power

    """
    global p1_tot_power
    global game_active
    print("Converting values to LEDS")
    game_leds.clear()
    game_active = True
    while game_start:
        pass

    p1_tot_power = 0           

# Defining main function
def main():
    """
    Main loop: Game should not return from this function
    """
    global game_start
    global keyboard_input
    global program_exit
    
    while not program_exit:
        # Standby process allows standby to run as background process
        standby_proc = Process(target=standby)

        while not game_start:
            if not standby_proc.is_alive():
                print("Start Standby Proc")
                standby_proc.start()

        standby_proc.terminate()
        game_countdown()
        run_game()

        print("End Game Session")        
            
    print("Program Exit")
  

if __name__=="__main__":

    np = neopixel.NeoPixel(pin, led_count, brightness=1)
    support = LedSupport(np, led_count, pin)
    # standby_proc = Process(target=standby)

    support.clear()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(game_start_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(power_gen_pin ,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(game_start_pin, GPIO.FALLING, callback=game_start_button_callback, bouncetime=100)
    GPIO.add_event_detect(power_gen_pin, GPIO.FALLING, callback=power_gen_button_callback, bouncetime=100)

    # signal.signal(signal.SIGINT, button_press_handler)
    

    main()