import serial
import re
import time
from collections.abc import Iterable

class Ade9178:

    def __init__(self):
        # Setup serial port
        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, parity=serial.PARITY_NONE, timeout=0.1,
                        bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                        xonxoff=0, rtscts=0, dsrdtr=0)

        self.power_calc_const = (44.188*707)/85829040

        self.ser.flush()
        
        # Disable high pass filter to allow DC values
        self.ser.write(b'setreg ade9178 0AE 20\r\n')
        hpf_disable = self.ser.readlines()
        result = hpf_disable[1].decode("utf-8")
        print(f"HPF Disable result: {result}")

        # Enable ADC
        self.ser.write(b'setreg ade9178 D7 1\r\n')

        adc_enable = self.ser.readlines()
        result = adc_enable[1].decode("utf-8")
        print(f"adc_enable result: {result}")

        # Time for ADC to settle
        time.sleep(1)

        self.ser.flush()
        

    def get_active_power(self, channel: str):
        """
        Query ADE9178 for Active Power channel depending on channel specified in parameter

        Parameters: 
        'A' - Channel A
        'B' - Channel B
        'C' - Channel C

        returns active power from specifed channel
        """

        # Match channel selection to re gister address
        channel_definitions = {
            'A': '254',
            'B': '25F',
            'C': '26A'
        } 

        read_address = channel_definitions.get(channel)
        command = b'getreg ade9178 ' + read_address.encode("utf-8") + b' 1\r'
        # print(f"power comand {command}")

        self.ser.write(command)
        self.ser.readline() # Ignore command sent from readback

        #
        active_power_parsed = self.ser.readline().decode("utf-8").strip().split(" = ")
        # print(active_power_parsed[1])
        active_power_hex = int(active_power_parsed[1], 16)
        active_power_decimal = self.twos_comp_to_dec(active_power_hex, 32)
        active_power_watts = self.power_calc_const * (active_power_decimal * -1)
        
        # print(f"Value = {active_power_watts}")

        return active_power_watts

    def twos_comp_to_dec(self, value, bits):
        """
        This function converts a 2's complement number to decimal

        :param value: Number to be converted.
        :type value: int | list[int]
        :param bits: Number of bits of value.
        :type bits: int.

        :return This function returns a 2's complement number converted to a signed magnitude number
        :rtype: int | list[int]
        """
        if isinstance(value, Iterable):
            return [val if val < (2 ** (bits - 1)) else val - (1 << bits) for val in value]
        else:
            return value if value < (2 ** (bits - 1)) else value - (1 << bits)


if __name__ == "__main__":
    
    ade9178 = Ade9178()
    
    while True:
        active_power_val = ade9178.get_active_power('A')
        # Adding 1 to make sure active_power_val is an int
        # print(f"{time.time()} :  Value{active_power_val[1]}")