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
from csv import writer
import os 
import threading 
from PyQt5.QtWidgets import *
import pygame

STANDBY = 0
COUNTDOWN = 1
IN_GAME = 2
RESULTS = 3
FULL_BRIGHTNESS = 1
LED_COUNT = 1085
LED_HEIGHT = 180
GAME_WIN_LEVEL = 60

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
                #self.game_status = COUNTDOWN
                self.game_status = IN_GAME
            else:
                print("Game Ended with button press")
                self.game_status = STANDBY

    def show_results(self):
        result_leds = AnimationGroup(
            Blink(self.winner.pixel_map, speed=0.3, color=color.GREEN),
            Solid(self.not_winner.pixel_map, color.BLACK),
        )
        print("\nGame over!")
        print(GREEN, "Winner :", self.winner.player_ID)
        print(GREEN, f"Score  : {self.game_duration:8.2f} s")
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

    def get_game_go_from_console():
        game_go = input()
        return game_go

    def LeaderboadGUI():
        app = QApplication(sys.argv)
        window = QWidget()
        window.label = QLabel("This is a label")
        window.show()
        app.exec()

    def gameplay_gui(self):
        pygame.init()
        width = 1920
        height = 1080
        screen = pygame.display.set_mode((width, height))
        dialogue_font = pygame.font.SysFont('arial', 50)
        adi_logo = pygame.image.load('assets/ADI_logo.png').convert()
        adi_logo = pygame.transform.scale(adi_logo, (202,113))
        adi_logo_rect = adi_logo.get_rect(topleft=(20,20))
        pygame.display.set_caption('Kinetic Tower')
        running = True
        while running:
            # use ctrl + esc to exit fullscreen
            while self.game_status == STANDBY:
                
                leaderboard_txt = dialogue_font.render('Leaderboard', True, color.BLACK)
                leaderboard_rect = leaderboard_txt.get_rect(center=(int(width/2), int(height/2)))

                screen.fill(color.WHITE)
                screen.blit(leaderboard_txt, leaderboard_rect)
                screen.blit( adi_logo, adi_logo_rect)
                pygame.display.update()

                # if pygame.event.get().type == pygame.QUIT:
                #     pygame.quit()
                #     exit()

                #for event in pygame.event.get():
                    #if event.type == pygame.QUIT:
                        #running = False
                        #pygame.quit()
                        #exit()
                        #break
            while self.game_status == IN_GAME:
                player1_txt = dialogue_font.render('Player 1', True, color.BLACK)
                player2_txt = dialogue_font.render('Player 2', True, color.BLACK)
                player1_score = dialogue_font.render(str(int(self.p1_energy)), True, color.BLACK)
                player2_score = dialogue_font.render(str(int(self.p2_energy)), True, color.BLACK)
                
                player1_txt_rect = player1_txt.get_rect(center=(int(width/4), int(height/2)))
                player2_txt_rect = player2_txt.get_rect(center=(int(3*width/4), int(height/2)))

                player1_score_rect = player1_score.get_rect(center=(int(width/4), int(height/2) + 100))
                player2_score_rect = player2_score.get_rect(center=(int(3*width/4), int(height/2) + 100))

                screen.fill(color.GREEN)
                screen.blit( adi_logo, adi_logo_rect)
                screen.blit(player1_txt, player1_txt_rect)
                screen.blit(player2_txt, player2_txt_rect)
                
                pygame.display.update()
                while self.game_status == IN_GAME:
                    screen.fill(color.GREEN)
                    player1_score = dialogue_font.render(str(int(self.p1_energy)), True, color.BLACK)
                    player2_score = dialogue_font.render(str(int(self.p2_energy)), True, color.BLACK)
                    p1_screen = screen.blit(player1_score, player1_score_rect)
                    p2_screen = screen.blit(player2_score, player2_score_rect)
            
                    screens = [p1_screen, p2_screen]
                    pygame.display.update(screens)

                    
            while game.game_status == RESULTS:
                screen.fill(color.BLUE)
                pygame.display.flip()

        
        pygame.display.quit()
        pygame.quit()

if __name__ == "__main__":

    print("Kinetic Tower Starting")

    #os.putenv('SDL_VIDEODRIVER', 'fbcon')

    ## Setup Power Sensors
    i2c_bus = board.I2C()

    p2_ina219 = INA219(i2c_bus, addr=0x40)
    p1_ina219 = INA219(i2c_bus, addr=0x44)

    p1_ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p1_ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p1_ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

    p2_ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p2_ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    p2_ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

    # Create Strip Objects
    p2 = Player(player_ID='PLAYER 2', input_pin=24, power_sensor=p2_ina219)
    p1 = Player(player_ID='PLAYER 1', input_pin=25, power_sensor=p1_ina219)

    game = KineticTowerGame()

    #  Setup for buttons
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(game.game_start_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(p1.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(p2.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(
        game.game_start_pin,
        GPIO.BOTH,
        callback=game.game_start_button_callback,
        bouncetime=350
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
    

    countdown_leds = AnimationSequence(
        Solid(pixels, color.RED),
        Solid(pixels, color.ORANGE),
        Solid(pixels, color.GREEN),
        Solid(pixels, color.BLACK),
    )
    
    gui_thread = threading.Thread(target=game.gameplay_gui)

    # Start GUI thread outsde loop. Can only be started once
    gui_thread.start()

    # Sets the game to run indefinetly 
    while True:

        clear_leds.animate()
        
        if game.game_status == STANDBY:
            # Set all LEDs to Standby Animation
            # standby.animate()
            clear_leds.animate()
            
            # Set players back to start
            os.system('clear')
            print(RESET)
            
            print("Entering Standby")
            print("Who can generate the power needed in the stortest time?!")
            while game.game_status == STANDBY:
                standby_leds.animate()
                
                # test_leds.animate()
                pass
            p1.reset()
            p2.reset()
            pass

        # elif game.game_status == COUNTDOWN:
        #     # Set all LEDs to Countdown
        #     print("Countdown!")
        #     game.game_status = IN_GAME
        #     for i in range(0,3):
        #         countdown_leds.activate(i)
        #         countdown_leds.animate()
        #         print(4-(i+1))
        #         time.sleep(.75)
        #     countdown_leds.freeze()
        #     pass
        #     pass

        elif game.game_status == IN_GAME:
            print("GO!!!")
            KineticTowerGame.log_interaction()
            clear_leds.animate()
            game_start_time = time.time()

            while game.game_status == IN_GAME:
                #Gamewindow.show()
                # Waits in loop as interrupts trigger while game is played
                game_leds.animate()
                p2.ina219_pwr_gen()
                p1.ina219_pwr_gen()

                game.p1_energy = p1.energy_gen
                game.p2_energy = p2.energy_gen

                game_time = time.time() - game_start_time 

                # Print Progress
                print(f'Player 1: {p1.player_leds.level:8.2f}\nPlayer 2: {p2.player_leds.level:8.2f}\n', end = '')
                print(f'Game Score: {game_time:8.2f}', end='')

                print(LINE_UP, LINE_UP, LINE_UP, LINE_CLEAR)
                

                # check for winner
                # Somewhere the player have gotten mixed up, this will print the correct winner however
                if p1.energy_gen > GAME_WIN_LEVEL:
                    print("PLAYER 1 WIN") 
                    print("\n\n\n")
                    game.winner = p1
                    game.not_winner = p2
                    game.tot_energy = p1.energy_gen + p2.energy_gen
                    game.game_status = RESULTS
                    game.game_duration = game_time
                    #print(LINE_UP, LINE_UP, LINE_CLEAR)

                elif p2.energy_gen > GAME_WIN_LEVEL:
                    print("PLAYER 2 WIN")
                    print("\n\n\n")
                    game.winner = p2
                    game.not_winner = p1
                    game.tot_energy = p1.energy_gen + p2.energy_gen
                    game.game_status = RESULTS
                    game.game_duration = game_time
                    #print(LINE_UP, LINE_UP, LINE_CLEAR)
                
                
                pass
        elif game.game_status == RESULTS:
            print("Show Results")
            while game.game_status == RESULTS:
                game.show_results()
                pass
        else:
            print("Exit Program - should not be reached")

    exit()
