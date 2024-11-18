from pickle import NONE
import board, neopixel, time
import RPi.GPIO as GPIO
import random
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow
import adafruit_led_animation.color as color
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation import helper
from led_power_level import PowerLevel
from player import Player
from pixel_maps import KTPixelMap
# from score import Score
from scoreClient import ScoreClient
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
from csv import writer
import os 
from itertools import cycle
import threading 
import pygame
import pygame_textinput
from ade9178_driver import Ade9178

STANDBY = 0
GET_INPUT = 1
IN_GAME = 2
RESULTS = 3
FULL_BRIGHTNESS = 1

BLINK_EVENT = pygame.USEREVENT + 0


# When using full length strips
LED_COUNT = 1085
LED_HEIGHT = 180
GAME_WIN_LEVEL = 180

# When using LED Matrix
# LED_HEIGHT = 32
# LED_COUNT = 256
# GAME_WIN_LEVEL = 11

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
        self.score_client = ScoreClient(game_name="Kinetic Tower", client_ip="169.254.102.64", host_ip="169.254.211.56")
        self.game_time = 0

        self.pwr_gen_filename = time.strftime("power_gen_today_%d_%m_%Y.txt") 

        if os.path.exists(self.pwr_gen_filename) is False:
            file = open(self.pwr_gen_filename, 'w')
            print(f"Create power gen file with name {self.pwr_gen_filename}")
            file.write('0')
            file.close()
        else:
            print(f"Using {self.pwr_gen_filename} for today's power gen")
            

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

    def log_interaction():
        interaction = [time.asctime()]
        filename = time.strftime("interactions_kinetic_tower_%d_%m_%Y.csv") 
        print(f"Create file with name {filename}")
        with open(filename, 'a') as file:

            interations = writer(file)
            interations.writerow(interaction)
            file.close()

    def get_game_go_from_console():
        game_go = input()
        return game_go

    def leaderboard_gui():
        pass

    def update_game_status(self, new_status):
        self.game_status = new_status
        
    def gameplay_gui(self):
        """
        This function creates all of the elements of the Kinetic Tower GUI
        It runs in a Thead and stays in sync with the main game code using the games
        game_status 
        """

        ONLINE_MODE = True

        pygame.init()
        width = 1920
        height = 1080
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        dialogue_font = pygame.font.Font('assets/research_remix.ttf', 60)
        score_font = pygame.font.Font('assets/research_remix.ttf', 50)
        adi_logo = pygame.image.load('assets/ADI-Logo-AWP-Tagline-KO-White.png').convert_alpha()
        adi_logo = pygame.transform.scale(adi_logo, (325,200))
        adi_logo_rect = adi_logo.get_rect(topleft=(25,25))
        pygame.display.set_caption('Kinetic Tower')
        pygame.event.set_allowed([pygame.QUIT, pygame.K_RETURN])
        running = True
        color_pool = cycle(color.RAINBOW)

        try:
            while running:
                
                while self.game_status == STANDBY:
                    print("GUI in standby")

                    try:

                        if ONLINE_MODE is False:
                            print("Attempting to get top 10")
                            leaderboard_list = self.score_client.get_top_10()

                            if leaderboard_list is not None:
                        
                                print(str(leaderboard_list))

                                clock = pygame.time.Clock()
                                pwr_today_float = 0
                                with open(self.pwr_gen_filename, 'r+') as pwr_file:
                                    pwr_today = pwr_file.read()
                                    pwr_today_float = float(pwr_today)
                                    print(f"Power Today {pwr_today_float}")
    
                                leaderboard_title = dialogue_font.render('PWR Gen Today: '+ str(round(pwr_today_float, 2)) + ' W', True, color.WHITE)
                                leaderboard_title_rect = leaderboard_title.get_rect(center=(int(width/2), 120))

                                game_start_prompt = dialogue_font.render("Who can generate 180 watts fast!!!", True, color.WHITE)
                                game_start_prompt_rect = game_start_prompt.get_rect(center=(int(width/2), 980))

                                off_text_surface = pygame.Surface(game_start_prompt_rect.size)
                                off_text_surface.fill((0,0,0,0))

                                blink_surfaces = cycle([game_start_prompt, off_text_surface])
                                blink_surface = next(blink_surfaces)
                                pygame.time.set_timer(BLINK_EVENT, 1000)

                                header_name_list = ['Name', 'School', 'Score']
                                header_blit_list = []
                                item_width = width/5
                                for item in header_name_list:

                                    leaderboard_header = dialogue_font.render(item, True, color.WHITE)
                                    leaderboard_header_rect = leaderboard_header.get_rect(center=(int(item_width), int(height/4)))
                                    header_blit_list.append((leaderboard_header, leaderboard_header_rect))
                                    item_width += width/4 + 50

                                score_name_list = ['@EntryName', '@SchoolName', '@Score']
                                score_blit_list = []
                                
                                item_height = height/4 + 75
                                

                                for score in leaderboard_list:
                                    if score is not None:
                                        item_width = width/5
                                        entry_color = next(color_pool)
                                    
                                        for item in score_name_list:
                                            score_element = score_font.render(score.get(item), True, entry_color)
                                            score_element_rect = score_element.get_rect(center=(int(item_width), int(item_height)) )
                                            score_blit_list.append((score_element, score_element_rect))
                                            item_width += width/4 + 50
                                        item_height += 50


                                screen.fill(color.BLACK)
                                screen.blit(leaderboard_title, leaderboard_title_rect)
                                # screen.blit(game_start_prompt, game_start_prompt_rect)
                                
                                screen.blit(adi_logo, adi_logo_rect)
                                screen.blits(header_blit_list)
                                screen.blits(score_blit_list)

                                pygame.display.update()

                                while self.game_status == STANDBY:

                                    # Can only close window from Standby
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.display.quit()
                                            pygame.quit()
                                            print("Got quit")
                                        elif event.type == BLINK_EVENT:
                                            blink_surface = next(blink_surfaces)
                                            clock.tick(60)
                                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f: 
                                            print("Toggle Fullscreen")
                                            pygame.display.toggle_fullscreen()
                                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                            print("Entering game with keyboard input")
                                            game.update_game_status(IN_GAME)
                                    screen.blit(blink_surface, game_start_prompt_rect)
                                    pygame.display.update()
                                    clock.tick(60)
                                    
                        else:
                            raise ConnectionError("Run Offline mode")

                    except ConnectionError:
                        # ONLINE_MODE = False
                        print("Cannot connect to database - continuing with simple mode")
                        leaderboard_title = dialogue_font.render('Ready to showcase Kinetic Tower!', True, color.WHITE)
                        leaderboard_title_rect = leaderboard_title.get_rect(center=(int(width/2), int(height/2)))
                        screen.fill(color.BLACK)
                        
                        screen.blit(leaderboard_title, leaderboard_title_rect)
                        pygame.display.update()

                        while self.game_status == STANDBY:
                            # Can only close window from Standby
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.display.quit()
                                    pygame.quit()
                                    print("Got quit")
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f: 
                                    print("Toggle Fullscreen")
                                    pygame.display.toggle_fullscreen()
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                    print("Entering game with keyboard input")
                                    game.update_game_status(IN_GAME)
                        

                while self.game_status == IN_GAME:
                    
                    player1_txt = dialogue_font.render('Power output (watts)', True, color.BLACK)
                    # player2_txt = dialogue_font.render('Player 2', True, color.BLACK)
                    player1_score = dialogue_font.render(str(self.p1_energy), True, color.BLACK)
                    # player2_score = dialogue_font.render(str(int(self.p2_energy)), True, color.BLACK)
                    
                    player1_txt_rect = player1_txt.get_rect(center=(int(width/2), int(height/2) - 100))
                    # player2_txt_rect = player2_txt.get_rect(center=(int(3*width/4), int(height/2)))

                    player1_score_rect = player1_score.get_rect(center=(int((width/2) - 200), int(height/2) + 100))
                    # player2_score_rect = player2_score.get_rect(center=(int(3*width/4), int(height/2) + 100))

                    # time_txt = dialogue_font.render("Time", True, color.BLACK)
                    # time_txt_rect = time_txt.get_rect(center=(int(width/2), int(height/4)))

                    # game_time = dialogue_font.render(str(round(self.game_time,2)), True, color.BLACK)
                    # time_rect = game_time.get_rect(center=(int(width/2)-60, int(height/4)+100)) 

                    screen.fill(color.BLACK)
                    screen.blit(adi_logo, adi_logo_rect)
                    screen.blit(player1_txt, player1_txt_rect)
                    # screen.blit(player2_txt, player2_txt_rect)
                    # screen.blit(time_txt, time_txt_rect)
                    # screen.blit(game_time, time_rect)
                    
                    pygame.display.update()
                    while self.game_status == IN_GAME:
                        screen.fill(color.GREEN)
                        energy = self.p1_energy

                        if energy > 4: 
                            energy_txt = "max"
                        else:
                            energy_txt = f"{self.p1_energy:8.3f}"
                        player1_score = dialogue_font.render(energy_txt, True, color.BLACK)
                        # player2_score = dialogue_font.render(str(int(self.p2_energy)), True, color.WHITE)
                        # game_time = dialogue_font.render(str(round(self.game_time,2)), True, color.WHITE)
                        screen.fill(color.GREEN)
                        screen.blit(adi_logo, adi_logo_rect)
                        screen.blit(player1_txt, player1_txt_rect)
                        # screen.blit(player2_txt, player2_txt_rect)
                        p1_screen = screen.blit(player1_score, player1_score_rect)
                        # p2_screen = screen.blit(player2_score, player2_score_rect)
                        # screen.blit(player2_txt, player2_txt_rect)
                        # screen.blit(time_txt, time_txt_rect)
                        # screen.blit(game_time, time_rect)
                        screen.blit(player1_score, player1_score_rect)
                        # screen.blit(player2_score, player2_score_rect)
                
                        # screens = [p1_screen, p2_screen]
                        pygame.display.update()
                        time.sleep(0.5)
                        
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                game.update_game_status(STANDBY)
                        
                while game.game_status == RESULTS:
                    print("Showing Results GUI")

                    results_color = next(color_pool)

                    results_title = dialogue_font.render('Results', True, results_color)
                    results_title_rect = results_title.get_rect(center=(int(width/2), 120))

                    results_color = next(color_pool)

                    winner_title = score_font.render("Winner!", True,results_color)
                    winner_title_rect = winner_title.get_rect(center=(int(width/3), int(height/4)))

                    winner_value = score_font.render(str(game.winner.player_ID), True, results_color)
                    winner_value_rect = winner_value.get_rect(center=(int(width/3), int(height/4)+50))

                    results_color = next(color_pool)

                    score_txt = score_font.render("Score (s)", True, results_color)
                    score_txt_rect = score_txt.get_rect(center=(int((2*width)/3), int(height/4)))
                        
                    score_value = score_font.render(f"{game.game_duration:8.2f}", True, results_color)
                    score_value_rect = score_value.get_rect(center=(int((2*width)/3), int(height/4)+50))

                    results_blits = [(results_title, results_title_rect), (winner_title, winner_title_rect), (winner_value, winner_value_rect), (score_txt, score_txt_rect), (score_value, score_value_rect) ]
                    
                    name_color = next(color_pool)
                    school_color = next(color_pool)

                    while game.game_status == RESULTS:

                        # Get info from user
                        input_entry_name = pygame_textinput.TextInputVisualizer(font_color=name_color, font_object=dialogue_font, cursor_color=color.WHITE)
                        input_entry_name.value = 'Entry'
                        input_entry_school = pygame_textinput.TextInputVisualizer(font_color=school_color, font_object=dialogue_font, cursor_color=color.WHITE)
                        input_entry_school.value = 'School'

                        name_rect = input_entry_name.surface.get_rect(center = (int(width/2), int(height/2)))
                        school_rect = input_entry_school.surface.get_rect(center = (int(width/2), int(height/2)+100))
                        
                        screen.fill(color.BLACK)
                        
                        screen.blits(results_blits)
                        screen.blit(adi_logo, adi_logo_rect)
                        
                        # screen.blit(input_entry_school.surface, school_rect)

                        pygame.display.update()

                        if 1:# if ONLINE_MODE is True:
                            get_entry = 1

                            while get_entry == 1:
                                screen.fill(color.BLACK)
                                screen.blit(input_entry_name.surface, name_rect)
                                screen.blits(results_blits)
                                screen.blit(adi_logo, adi_logo_rect)
                                events = pygame.event.get()

                                input_entry_name.update(events)
                                pygame.display.update()

                                for event in events:
                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                        print("GOT Entry name: ", input_entry_name.value)
                                        get_entry = 2
                            

                            while get_entry == 2:
                                screen.fill(color.BLACK)
                                screen.blit(input_entry_name.surface, name_rect)
                                screen.blit(input_entry_school.surface, school_rect)
                                screen.blits(results_blits)
                                screen.blit(adi_logo, adi_logo_rect)
                                events = pygame.event.get()
                                input_entry_school.update(events)
                                pygame.display.update()

                                for event in events:                 
                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                        print("GOT School name: ", input_entry_school.value)
                                        get_entry = 3
                                        try:
                                            new_score = self.score_client.submit_score(entry_name=input_entry_name.value, school_name=input_entry_school.value, score=round(game.game_duration, 2))
                                            time.sleep(0.5)
                                        except ConnectionError:
                                            print("Failed to submit score - continuing")
                                        game.update_game_status(STANDBY)
                        else:
                            while game.game_status == RESULTS:
                                events = pygame.event.get()

                                # Don't print socre entry if in offline mode - press enter to start new game
                                for event in events:                 
                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                        game.update_game_status(STANDBY)
                                                    
                        
        # Clean up GUI displays     
        finally:
            pygame.display.quit()
            pygame.quit()    

if __name__ == "__main__":

    print("Kinetic Tower Starting")

    ## Setup Power Sensors

    # Create instance of ADE9178
    ade9187 = Ade9178()

    # Create Strip Objects
    p1 = Player(player_ID='PLAYER 1', input_channel='A', power_sensor=ade9187)
    p2 = Player(player_ID='PLAYER 2', input_channel='A', power_sensor=ade9187)

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

    #  Setup for LEDs
    pixels = neopixel.NeoPixel(
        pin=board.D18, n=LED_COUNT, brightness=FULL_BRIGHTNESS, auto_write=True
    )

    #  Create instances of LEDs for each player - Maps LEDs to each player
    p1_pixel_map = helper.PixelMap(
        pixels, KTPixelMap.combined_pixel_map, individual_pixels=True
    )
    # p2_pixel_map = helper.PixelMap(
    #     pixels, KTPixelMap.p2_pixel_map_strips, individual_pixels=True
    # )

    #  Create game 'Scenes' - what gets displayed on LEDs at different points in the game
    standby_leds = AnimationGroup(
        # Rainbow(p1_pixel_map, 0.1, 10), Rainbow(p2_pixel_map, 0.1, 10)
        Rainbow(p1_pixel_map, 0.1, 10)
    )

    clear_leds = AnimationGroup(
        Solid(p1_pixel_map, color.BLACK)
    )

    p1_game_leds = PowerLevel(p1_pixel_map, color.GREEN, max_height=LED_HEIGHT)
    # p2_game_leds = PowerLevel(p2_pixel_map, color.BLUE, max_height=LED_HEIGHT)

    test_leds = AnimationGroup(
        Blink(p1_pixel_map, speed=0.3, color=color.RED),
        # Blink(p2_pixel_map, speed=0.3, color=color.GREEN),
    )

    # Add the group of LEDs to the game
    # game_leds = AnimationGroup(p1_game_leds, p2_game_leds)
    game_leds = AnimationGroup(p1_game_leds)

    p1.add_leds(p1_game_leds, p1_pixel_map)
    # p2.add_leds(p2_game_leds, p2_pixel_map)
    

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
            #os.system('clear')
            #print(RESET)
            
            print("Entering Standby")
            print("Who can generate the power needed in the stortest time?!")
            while game.game_status == STANDBY:
                standby_leds.animate()
                
                # test_leds.animate()
                pass
            p1.reset()
            # p2.reset()
            pass

        # elif game.game_status == COUNTDOWN:
        # Set power level goals;
        # def generate_power_level(min_value, max_value):
        #     return random.randint(min_value, max_value)

        # # Example usage
        # min_value = 1
        # max_value = 100
        # target_power_level = generate_power_level(min_value, max_value)
        # print(f"The power level to reach is: {target_power_level}")
        # # display power level goal on LED Bar

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
                # clear_leds.animate()
                game_leds.animate()
                p1.get_power_reading()
                print(f"energy {p1.energy_gen}")
                # p2.energy_gen = p1.energy_gen
                p1.update_player_leds()
                # p2.update_player_leds()


                # p2.update_power_gen()

                game.p1_energy = p1.energy_gen

                # game.p2_energy = p2.energy_gen

                # game.game_time = time.time() - game_start_time

                # # Print Progress
                # print(f'Player 1: {p1.player_leds.level:8.2f}\nPlayer 2: {p2.player_leds.level:8.2f}\n', end = '')
                # print(f'Game Score: {game_time:8.2f}', end='')

                # print(LINE_UP, LINE_UP, LINE_UP, LINE_CLEAR)
                

                # check for winner
                # Somewhere the player have gotten mixed up, this will print the correct winner however
                # Show position of target bar again
                # def determine_winner(target_power_level, p1_energy_gen, p2_energy_gen):
                #     if p1_energy_gen > target_power_level and p2_energy_gen > target_power_level:
                #         return "It's a draw", target_power_level  # Both overloaded
                #     Overloaded - flash LEDS & screen hazard....
                #     elif p1_energy_gen > target_power_level:
                #         return "Player 2 wins", p2_energy_gen  # P1 overloaded - Flash their LEDs
                #     elif p2_energy_gen > target_power_level:
                #         return "Player 1 wins", p1_energy_gen  # P2 overloaded - Flash their LEDs
                #     else:
                # Both are under or equal to target power level
                #         if p1_energy_gen > p2_energy_gen:
                #             return "Player 1 wins", p1_energy_gen # P1 Bar goes green, P2 Bar goes red
                #         elif p2_energy_gen > p1_energy_gen:
                #             return "Player 2 wins", p2_energy_gen # P2 Bar goes green, P1 Bar goes red
                #         else:
                #             return "It's a draw", p1_energy_gen  # Both are equal - both bars go green

                # Test
                # target_power_level = 50
                # p1_energy_gen = 45
                # p2_energy_gen = 55
                # winner, energy_used = determine_winner(target_power_level, p1_energy_gen, p2_energy_gen)
                # print(f"{winner} with {energy_used} energy")


                if p1.energy_gen > GAME_WIN_LEVEL:
                    print("PLAYER 1 WIN") 
                    print("\n\n\n")
                    game.winner = p1
                    game.not_winner = p2
                    game.tot_energy = p1.energy_gen #+ p2.energy_gen
                    game.game_status = RESULTS
                    game.game_duration = game.game_time
                    #print(LINE_UP, LINE_UP, LINE_CLEAR)

                elif p2.energy_gen > GAME_WIN_LEVEL:
                    print("PLAYER 2 WIN")
                    print("\n\n\n")
                    game.winner = p2
                    game.not_winner = p1
                    game.tot_energy = p2.energy_gen #+ p2.energy_gen
                    game.game_status = RESULTS
                    game.game_duration = game.game_time
                    #print(LINE_UP, LINE_UP, LINE_CLEAR)
                
                
        elif game.game_status == RESULTS:
            print("Show Results")
            # Define Result LEDs - need to wait till after game has finished to determine leds for winner
            result_leds = AnimationGroup(
                Blink(game.winner.pixel_map, speed=0.5, color=color.GREEN),
                Blink(game.not_winner.pixel_map, speed=0.5, color=color.BLACK)
            )

            total_game_power = p1.energy_gen + p2.energy_gen

            with open(game.pwr_gen_filename, 'r+') as pwr_file:
                pwr_today = pwr_file.read()
                pwr_today_val = float(pwr_today) + total_game_power
                pwr_file.seek(0)
                print(f"New Daily Total Power {pwr_today_val}")
                pwr_file.write(str(pwr_today_val))
                pwr_file.truncate()


            while game.game_status == RESULTS:

                result_leds.animate()   

                # print("\nGame over!")
                # print(GREEN, "Winner :", self.winner.player_ID)
                # print(GREEN, f"Score  : {self.game_duration:8.2f} s")
        
        else:
            print("Exit Program - should not be reached")

    exit()
