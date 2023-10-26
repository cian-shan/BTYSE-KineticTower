import serial
import re
import time

if __name__ == "__main__":
    # codecs.register_error('slashescape', slashescape)

    print("Open serial connection to ADE9178")
    # Stup serial port
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, parity=serial.PARITY_NONE, timeout=0.2,
                        bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                        xonxoff=0, rtscts=0, dsrdtr=0)
    print(ser.name)
    # ser.write(b'version\r')
    # AWATT 0x254
    start_time = time.time_ns()
    ser.write(b'getreg ade9178 254 1\r')
    awatt_lines = ser.readlines()
    print(f'aline {awatt_lines}\n')
    awatt_value = re.findall(r'0x(\d)', str(awatt_lines[1]))
    print(f"awatt_value {awatt_value}\n\n")

    ser.write(b'getreg ade9178 25F 1\r')
    bwatt_lines = ser.readlines()
    print(f'bline {bwatt_lines}\n')
    bwatt_value = re.findall(r'0x(\d)', str(bwatt_lines[1]))
    print(f"bwatt_value {bwatt_value}\n\n")

    end_time = time.time_ns()
    
    print(f'AWATT {awatt_value[0]}')
    print(f'BWATT {bwatt_value[0]}\n\n')

    print(f'time taken: {end_time - start_time}')

    ser.close()