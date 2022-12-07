import socket 
import time
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import os

TCP_IP = '127.0.0.1'


class Score():

    def __init__(self, entry_name, school_name, score):
        self.game_name = "kinetic_tower"
        self.entry_name =  entry_name
        self.school_name = school_name
        self.score = score

    def create_xml(self):
        xml = dicttoxml(self, attr_type=False, custom_root='Score')
        #print(xml)

        dom = parseString(xml)
        # print(dom.toprettyxml())

    def send_score():
        pass

    def get_top_10():
        pass

    def print_gameplay(self):

        pass
        

if __name__ == "__main__":

    

    # Test creating an XML Score 
    # score1 = vars(Score("Jenny", "School NS", 120))
    # Score.create_xml(score1)
    # Score.log_interaction()

    LINE_UP = u"\u001b[1A"
    LINE_CLEAR = u"\u001b[1K"
    RED = u"\u001b[31m"
    MAGENTA= u"\u001b[35m"
    YELLOW= u"\u001b[33m"
    GREEN = u"\u001b[32m"
    RESET = u"\u001b[0m"

    print("COUNTDOWN!")
    time.sleep(1)
    print(LINE_CLEAR, LINE_UP)
    print(RED,"----3----", end='')
    time.sleep(1)
    print(LINE_UP, LINE_CLEAR)
    print(MAGENTA,"----2----", end='')
    time.sleep(1)
    print(LINE_UP, LINE_CLEAR)
    print(YELLOW,"----1----", end='')
    time.sleep(1)
    print(LINE_UP, LINE_CLEAR)
    print(GREEN,"---GO!---", end='')
    time.sleep(1)
    print(LINE_UP, LINE_CLEAR, RESET)
    
    start_time = time.time()
    print(f'{start_time=}')

    game_time = 0

    for itr in range(0, 90):

        game_time = time.time() - start_time 

        print(f'Player 1: {itr=} || Player 2: {itr=}\n', end = '')
        print(f'Game Score: {game_time=}', end='')

        print(LINE_UP, LINE_UP, LINE_CLEAR)

        time.sleep(.2)

    
    



