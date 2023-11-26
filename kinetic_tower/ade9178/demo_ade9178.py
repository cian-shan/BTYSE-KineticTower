import sys
from time import sleep
import modbus
from TE115_oven_control import read_oven_temp, read_oven_setpoint, write_oven_setpoint
import serial
import Fluke6003A
import pandas as pd
import datetime
import math
from statistics import mean

# constants 
IFS = 44.188
VFS = 707
AUXFS = 707
RMS_CODES = 107310840
POW_CODES = 85829040
PCF_CODES = 6706531
METER_CONSTANT = 10000 # imp/kWh

FREQ = 50 # Hz
PF = 1 # power factor
EGY_TIME = 10 # s

CF_THRES = hex(round((1000*60*60*POW_CODES*4000)/(METER_CONSTANT*IFS*VFS*256)))

cycles = 200 # number of half line cycles captured at each test point
i = 0 # create counter

# configure serial connection to the ADE9178 part
ade9178 = serial.Serial(
    port = 'COM4',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS
)

ade9178.write(b"reset" + b"\r") # reset the registers on the ADE9178
ade9178.readline()
print(ade9178.readline()) # print that part registers reset successfully

ade9178.write(b"loadcal" + b"\r") # load calibration constants
while(i<111): # read out load cal data
    ade9178.readline()
    i=i+1

"""
ade9178.write(b"setreg ADE9178 0B1 10" + b"\r") # Set CF1_CONFIG Register - Enable Pulse
ade9178.readline()
print("set CF1_config...")
print(ade9178.readline())

ade9178.write(b"setreg ADE9178 0B9 " + CF_THRES.encode() + b"\r") # Set CF1_THRES Register
ade9178.readline()
print("set CF1_THRES config...")
print(ade9178.readline())
"""

# configure connection to the temperature oven
oven = modbus.ModbusRTU(
    address=1,
    port='COM3',
    baud=9600,
    timeout=10.0
)

def close(client):
    '''close the connection to the controller'''
    try:
        client.close()
    except AttributeError:
        pass
    client = None  

# configure connection to the Fluke6003A
fluke = serial.Serial(
    port = 'COM8',
    baudrate = 9600,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 1)    

# values
currents = [0.016, 0.0256, 0.32, 0.64, 6.4, 16, 30] # Amps
#currents = [6, 15, 24, 30]
voltage = 230
temperatures = [50, 25, 0, -20, -40] # degrees C
#temperatures = [-40]

dt_temp = 1 # error on temperature

for temp in temperatures:
    
    write_oven_setpoint(oven, 1, temp)
    print('Setting temp to '+str(temp))
    while not((temp-dt_temp)<=int((read_oven_temp(oven,1)))<=(temp+dt_temp)): #waiting for temperature to stabilize
        sleep(10)
        print(read_oven_temp(oven,1))
    print("stabilising...")
    sleep(60*5)
    
    for amp in currents:
        
        Fluke6003A.send_command(fluke, "SYST:REM")
        Fluke6003A.send_command(fluke, "*RST")
        Fluke6003A.send_command(fluke, "PAC:FREQ "+str(FREQ)) # frequency
        Fluke6003A.send_command(fluke, "PAC:VOLT "+str(voltage)) # voltage
        Fluke6003A.send_command(fluke, "PAC:CURR "+str(amp)) # current
        Fluke6003A.send_command(fluke, "OUTP:UNIT COS") # change unit of phase shift to power factor
        Fluke6003A.send_command(fluke, "PAC:PHAS "+str(PF)) # power factor
        sleep(5)
        Fluke6003A.send_command(fluke, "OUTP:STAT ON") # start test
        

        print("Starting test at " + str(amp) + "A, " + str(voltage) + "V and " + str(temp) + "C...")
        # flush input and output buffers
        ade9178.reset_input_buffer()
        ade9178.reset_output_buffer()
        sleep(60*3)

        ade9178.write(b"start " + str(cycles).encode() + b"\r")
        ade9178.readline()

        i=0
        z=0 
        j=0
        results = []
        while(i<cycles*61):
            # read the full response, decode strip and split.
            response = ade9178.readline().decode("utf-8").strip().split("=")
            # print full response
            #print(response)
            i=i+1 # increment counter
            res = {'cycles':z+1,'variable':response[0],'value':response[1]}
            results.append(res) # append to list
            if(j<60): 
                j=j+1
            else: 
                z=z+1 
                j=0

        print("Test completed...")
        Fluke6003A.send_command(fluke, "OUTP:STAT OFF") # end test

        df = pd.DataFrame(results)
        df.to_csv(str(amp) + "A_" + str(voltage) + "V_" + str(temp) + "C_ade9178.csv", encoding='utf-8', index=False)

        results = [] # write to zero.
        if(amp>10):
            print("curr greater than 10A, cooling down fluke for 5 minutes...")
            sleep(60*5)

write_oven_setpoint(oven, 1, 25) # reset temp.
print('Setting temp to '+str(25))
print("Test completed.")

    
