import serial
import re
import codecs


# def slashescape(err):
#     """ codecs error handler. err is UnicodeDecode instance. return
#     a tuple with a replacement for the unencodable part of the input
#     and a position where encoding should continue"""
#     #print err, dir(err), err.start, err.end, err.object[:err.start]
#     thebyte = err.object[err.start:err.end]
#     repl = u'\\x'+hex(ord(thebyte))[2:]
#     return repl, err.end


if __name__ == "__main__":
    # codecs.register_error('slashescape', slashescape)

    print("Open serial connection to ADE9178")
    ser = serial.Serial(port='COM13', baudrate=115200, parity=serial.PARITY_NONE, timeout=0.2,
                        bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE,
                        xonxoff=0, rtscts=0, dsrdtr=0)
    print(ser.name)
    # ser.write(b'version\r')
    ser.write(b'getreg ade9178 bc 1\r')
    lines = ser.readlines()
    value = re.search("0x....", str(lines[1]))
    print(f'ZXTHRSH {value}')
    # output = line.decode('cp1250')
    # output = bytes(lines).decode('utf-8')
    # print(f'raw output: {line}')
    # print(f'data returned: {lines}')
    ser.close()

