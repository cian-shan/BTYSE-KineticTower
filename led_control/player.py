import RPi.GPIO as GPIO
import time


class Player:
    def __init__(
        self, player_ID, input_pin, power_sensor, player_leds=None, energy_gen=0
    ):
        self.player_ID = player_ID
        self.input_pin = input_pin
        self.player_leds = None
        self.energy_gen = energy_gen
        self.power_sensor = power_sensor

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
            print("Player: %d - Power Gen: %d " % (self.player_ID, self.energy_gen))

    def ina219_pwr_gen(self):
        bus_voltage = self.power_sensor.bus_voltage  # voltage on V- (load side)
        shunt_voltage = (
            self.power_sensor.shunt_voltage
        )  # voltage between V+ and V- across the shunt
        current = self.power_sensor.current  # current in mA
        power = self.power_sensor.power  # power in watts
        print("Power Read: ", power)
        load_voltage = bus_voltage + (
            shunt_voltage / 1000
        )  # Deviding shunt by 1000 to match units
        self.energy_gen = self.energy_gen + (
            (load_voltage * current) / 3600
        )  # Calculate cumulative energy in Wh
        self.player_leds.update_level(int(self.energy_gen))
        print("Player: %d - Total Energy: %d " % (self.player_ID, self.energy_gen))
        # time.sleep(.5)
        pass

    def get_pwr_gen(self):
        return self.energy_gen
