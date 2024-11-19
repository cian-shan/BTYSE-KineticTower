import RPi.GPIO as GPIO
import time


class Player:
    def __init__(
        self, player_ID, input_channel, power_sensor=None, player_leds=None, energy_gen=0
    ):
        self.player_ID = player_ID
        self.input_channel = input_channel
        self.player_leds = None
        self.energy_gen = energy_gen
        self.power_sensor = power_sensor
        self.game_start_time = None

    def reset(self):
        self.energy_gen = 0
        self.player_leds.reset()

    def add_leds(self, leds, map):
        self.player_leds = leds
        self.pixel_map = map

    # def update_leds(self, level):
    #    """ Updates LEDs to reflect total power generated """

    def button_power_gen(self, player):
        """
        Function Runs as Power Generation Button pressed
        Increments LED index, LEDs are illuminated.
        """
        if not GPIO.input(self.input_pin):
            self.energy_gen += 1
            self.player_leds.update_level(self.energy_gen)
            # print("Player: %d - Power Gen: %d " % (self.player_ID, self.energy_gen))

    def update_power_gen(self):
        """
        Read active power from ADE9178 and update player 
        """
        self.energy_gen = self.power_sensor.get_active_power(self.input_channel)
        print(f"emp Power Reading {self.input_channel}: {self.energy_gen}")
        

    def update_player_leds(self):
        self.player_leds.update_level(int(self.energy_gen)*45)

    
    def get_power_reading(self):
        self.energy_gen = self.power_sensor.get_active_power(self.input_channel)
        print(f"EMP Power Reading {self.input_channel}: {self.energy_gen}")
        # self.player_leds.update_level(int(self.energy_gen)*36)



    def ina219_pwr_gen(self):
        """
        This method is deprecated - using ade9187 for power measurements
        """
        bus_voltage = self.power_sensor.bus_voltage  # voltage on V- (load side)
        shunt_voltage = (self.power_sensor.shunt_voltage)  # voltage between V+ and V- across the shunt
        current = self.power_sensor.current  # current in mA
        power = self.power_sensor.power  # power in watts
        # print("Power Read: ", power)
        load_voltage = bus_voltage + (shunt_voltage / 1000)  # Deviding shunt by 1000 to match units
        self.energy_gen = self.energy_gen + ((load_voltage * current) / 3600)  # Calculate cumulative energy in Wh
        self.player_leds.update_level(int(self.energy_gen)*3)
        # print("Player: %d - Total Energy: %d " % (self.player_ID, self.energy_gen))
        # time.sleep(.5)
        pass

    def get_pwr_gen(self):
        return self.energy_gen

    def start_game_time(self):
        self.game_start_time = time.time()

    def get_game_duration(self):
        return time.time() - self.game_start_time
