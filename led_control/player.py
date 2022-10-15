import RPi.GPIO as GPIO

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