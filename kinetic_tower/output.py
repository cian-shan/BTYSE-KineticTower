import time

LINE_UP = u"\u001b[1A"
LINE_CLEAR = u"\u001b[1K"
RED = u"\u001b[31m"
MAGENTA= u"\u001b[35m"
YELLOW= u"\u001b[33m"
GREEN = u"\u001b[32m"
RESET = u"\u001b[0m"

def print_countdown():
    print("COUNTDOWN!")
    time.sleep(1)
    print(LINE_CLEAR, LINE_UP)
    print("----3----", end='')
    time.sleep(1)
    print(LINE_UP, LINE_CLEAR)
    print("----2----", end='')
    time.sleep(1)
    print(LINE_UP, LINE_CLEAR)
    print("----1----", end='')
    time.sleep(1)
    print(LINE_UP, LINE_CLEAR)
    print("---GO!---", end='')
    time.sleep(1)
    print(LINE_UP, LINE_CLEAR)