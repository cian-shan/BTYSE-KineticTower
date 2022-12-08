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
from score import Score
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import subprocess
import sys
from CountDown_GUI import Ui_Form
from GameRunningGui import GameUi_Form
from Idle_LeaderboardGUI import Ui_MainWindow
from PyQt5 import QtGui, QtWidgets
from csv import writer
import os 


STANDBY = 0
COUNTDOWN = 1
IN_GAME = 2
RESULTS = 3
FULL_BRIGHTNESS = 1
LED_COUNT = 1085
LED_HEIGHT = 180
GAME_WIN_LEVEL = 90

LINE_UP = u"\u001b[1A"
LINE_CLEAR = u"\u001b[1K"
RED = u"\u001b[31m"
MAGENTA= u"\u001b[35m"
YELLOW= u"\u001b[33m"
GREEN = u"\u001b[32m"
RESET = u"\u001b[0m"

class KineticTowerGame:
    def __init__(
        self,
        game_start_pin=23,
        game_status=STANDBY,
        p1_energy=0,
        p2_energy=0,
        tot_energy=0,
        winner=NONE,
        not_winner=NONE,
        game_duration=NONE
    ):

        self.game_start_pin = game_start_pin
        self.game_status = game_status
        self.p1_energy = p1_energy
        self.p2_energy = p2_energy
        self.tot_energy = tot_energy
        self.winner = winner
        self.not_winner = not_winner
        self.game_duration = game_duration

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
            Solid(self.not_winner.pixel_map, color.BLACK),
        )
        print("Game over!")
        print(GREEN, "Winner :", self.winner.player_ID)
        print(GREEN, "Score: ", game.game_duration)
        for i in range(5):
            result_leds.animate()
            time.sleep(1)
        self.game_status = STANDBY
        pass
    def log_interaction():
        interaction = [time.asctime()]
        with open('interactions_kinetic_tower.csv', 'a') as file:

            interations = writer(file)
            interations.writerow(interaction)
            file.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    Countwindow = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Countwindow)
    Countwindow.show()

    for i in range(6):
        ui.lcdNumber.display(i)
        time.sleep(0.5)
    Countwindow.close()
    '''
    print("Kinetic Tower Starting")

    ## Setup Power Sensors
    i2c_bus = board.I2C()

    p1_ina219 = INA219(i2c_bus, addr=0x40)
    p2_ina219 = INA219(i2c_bus, addr=0x44)

    p1_ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p1_ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p1_ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

    p2_ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p2_ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p2_ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

    # Create Strip Objects
    p1 = Player(player_ID=1, input_pin=24, power_sensor=p1_ina219)
    p2 = Player(player_ID=2, input_pin=25, power_sensor=p2_ina219)

    game = KineticTowerGame()

    #  Setup for buttons
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(game.game_start_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(p1.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(p2.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(
        game.game_start_pin,
        GPIO.FALLING,
        callback=game.game_start_button_callback,
        bouncetime=500,
    )
    # GPIO.add_event_detect(
    #     p1.input_pin, GPIO.FALLING, callback=p1.button_power_gen, bouncetime=200
    # )
    # GPIO.add_event_detect(
    #     p2.input_pin, GPIO.FALLING, callback=p2.button_power_gen, bouncetime=200
    # )

    #  Setup for LEDs
    pixels = neopixel.NeoPixel(
        pin=board.D18, n=LED_COUNT, brightness=FULL_BRIGHTNESS, auto_write=True
    )

    #  Create instances of LEDs for each player - Maps LEDs to each player
    p1_pixel_map = helper.PixelMap(
        pixels, KTPixelMap.p1_pixel_map_strips, individual_pixels=True
    )
    p2_pixel_map = helper.PixelMap(
        pixels, KTPixelMap.p2_pixel_map_strips, individual_pixels=True
    )

    #  Create game 'Scenes' - what gets displayed on LEDs at different points in the game
    standby_leds = AnimationGroup(
        Rainbow(p1_pixel_map, 0.1, 10), Rainbow(p2_pixel_map, 0.1, 10)
    )

    clear_leds = AnimationGroup(
        Solid(p1_pixel_map, color.BLACK), Solid(p2_pixel_map, color.BLACK)
    )

    p1_game_leds = PowerLevel(p1_pixel_map, color.ORANGE, max_height=LED_HEIGHT)
    p2_game_leds = PowerLevel(p2_pixel_map, color.BLUE, max_height=LED_HEIGHT)

    test_leds = AnimationGroup(
        Blink(p1_pixel_map, speed=0.3, color=color.RED),
        Blink(p2_pixel_map, speed=0.3, color=color.GREEN),
    )

    # Add the group of LEDs to the game
    game_leds = AnimationGroup(p1_game_leds, p2_game_leds)

    p1.add_leds(p1_game_leds, p1_pixel_map)
    p2.add_leds(p2_game_leds, p2_pixel_map)
    '''
 

    

    #countdown GUI setup
 
'''
    #GameRunningGUI setup
    Gamewindow = QtWidgets.QWidget()
    GameRunUI = GameUi_Form()
    GameRunUI.setupUi(Gamewindow)

    #Idle screen
    # IdleWindow = QtGui.QMainwindow

    # Sets the game to run indefinetly 
    while True:

        clear_leds.animate()

        if game.game_status == STANDBY:
            # Set all LEDs to Standby Animation
            # standby.animate()
            clear_leds.animate()
            # Set players back to start
            # os.system('clear')
            print("Entering Standby")
            # standby_proc.run
            while game.game_status == STANDBY:
                standby_leds.animate()
                # test_leds.animate()
                pass
            p1.reset()
            p2.reset()
            pass

        elif game.game_status == COUNTDOWN:

            # Set all LEDs to Countdown
            print("COUNTDOWN!")
            countdown_leds = Solid(pixels , color.RED)
            countdown_leds.animate()
            Countwindow.show()
            ui.lcdNumber.display(3)
            Countwindow.repaint()
            print(RED,"----3----", end='')
            time.sleep(.5)
            print(LINE_UP, LINE_CLEAR)
            countdown_leds = Solid(pixels , color.ORANGE)
            countdown_leds.animate()
            ui.lcdNumber.display(2)
            Countwindow.repaint()
            print(MAGENTA,"----2----", end='')
            time.sleep(.5)
            print(LINE_UP, LINE_CLEAR)
            countdown_leds = Solid(pixels , color.YELLOW)
            countdown_leds.animate()
            ui.lcdNumber.display(1)
            Countwindow.repaint()
            print(YELLOW,"----1----", end='')
            time.sleep(.5)
            print(LINE_UP, LINE_CLEAR)
            countdown_leds = Solid(pixels , color.BLACK)
            countdown_leds.animate()
            print(GREEN,"---GO!---", end='')
            time.sleep(.5)
            Countwindow.close()
            print(LINE_UP, LINE_CLEAR, RESET)
            sys.exit(app.exec_())
            game.game_status = IN_GAME
            pass

        elif game.game_status == IN_GAME:
            
            print("In Game")
            clear_leds.animate()
            
            game_start_time = time.time()

            while game.game_status == IN_GAME:
                #Gamewindow.show()
                # Waits in loop as interrupts trigger while game is played
                game_leds.animate()
                p2.ina219_pwr_gen()
                p1.ina219_pwr_gen()

                game_time = time.time() - game_start_time 

                # Print Progress
                print(f'Player 1: {p1.player_leds.level=:.2f} || Player 2: {p2.player_leds.level=:.2f}\n', end = '')
                print(f'Game Score: {game_time=:.2f}', end='')

                print(LINE_UP, LINE_UP, LINE_CLEAR)

                # check for winner
                if p2.energy_gen > GAME_WIN_LEVEL:
                    game.winner = p2
                    game.not_winner = p1
                    game.tot_energy = p1.energy_gen + p2.energy_gen
                    game.game_status = RESULTS
                    game.game_duration = game_time
                    print(LINE_UP, LINE_UP, LINE_CLEAR)

                elif p1.energy_gen > GAME_WIN_LEVEL:
                    game.winner = p1
                    game.not_winner = p2
                    game.tot_energy = p1.energy_gen + p2.energy_gen
                    game.game_status = RESULTS
                    game.duration = game_time
                    print(LINE_UP, LINE_UP, LINE_CLEAR)
                
                #Gamewindow.close()
                pass
        elif game.game_status == RESULTS:
            print("Show Results")
            while game.game_status == RESULTS:
                game.show_results()
                pass
        else:
            print("Exit Program - should not be reached")
    '''        