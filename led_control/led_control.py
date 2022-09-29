import board, neopixel, sys, time, signal
import RPi.GPIO as GPIO
from multiprocessing import Process
from led_support import LedSupport

led_count = 20
pin = board.D18

game_start_pin = 23
power_gen_pin = 24

program_exit = False
game_start = False

p1_tot_power = 0
game_leds = []
        

def game_start_button_callback(self):
    global game_start
    if not GPIO.input(game_start_pin):
        if not game_start:
            print("Game Start")
            game_start = True
            pass
        else:
            print("Game End")
            game_start = False


def power_gen_button_callback(self):
    global p1_tot_power
    global game_start
    if not GPIO.input(power_gen_pin):      
        p1_tot_power += 1
        try:
            np[p1_tot_power-1] = (0,255,0)
            print("1W generated! ",p1_tot_power )
        except:
            print("WINNER!! 20W produced")
            game_start = False
        # game_leds.append((0,255,0))
    else:
        print("Button Released")
    

# Run Standby Animations
def standby():
    print("Standby")
    #support.set_color(255,0,0)
    support.rainbow_cycle(5)
    pass

# Game Countdown function
def game_countdown():
    # RED
    np.fill([255,0,0])
    time.sleep(1)

    #ORANGE
    np.fill([255,50,0])
    time.sleep(1)

    #YELLOW
    np.fill([255,255,0])
    time.sleep(1)

    #GREEN
    np.fill([0,255,0])
    time.sleep(1)

    support.clear()

    

def power_to_led():
    print("Converting values to LEDS")
    p1_tot_power = 0
    game_leds.clear()
    while game_start:
        pass           

# Defining main function
def main():
    global game_start
    global keyboard_input
    global program_exit

    
    while not program_exit:

        standby_proc = Process(target=standby)

        while not game_start:
            if not standby_proc.is_alive():
                print("Start Standby Proc")
                standby_proc.start()

        standby_proc.terminate()
        game_countdown()
        power_to_led()

        print("End Game Session")        
            
    print("Program Exit")
  

if __name__=="__main__":

    np = neopixel.NeoPixel(pin, led_count, brightness=.3)
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