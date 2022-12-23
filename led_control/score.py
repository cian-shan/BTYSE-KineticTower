import socket
import json
import time
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import os
import xmltodict
TCP_IP = '127.0.0.1'
#TCP_IP = '169.254.207.119'
PORT = 9000
CLIENT_IP = socket.gethostbyname(socket.gethostname())
GAME_NAME = "Kinetic Tower"
class Score():
    def __init__(self, entry_name=None, school_name=None, score=None):
        self.game_name = GAME_NAME
        self.entry_name = entry_name
        self.school_name = school_name
        self.score = score
        self.message_id = id(self)
        self.receiver_ip = str(TCP_IP)
        self.sender_ip = str(CLIENT_IP)
    def create_xml(self):
        # xml = dicttoxml(self, attr_type=True, custom_root='Score')
        # print(xml)
        # dom = parseString(xml)
        # print(dom.toprettyxml())
        score = {
            "NewScoreMessage":
                {
                    '@GameId': self.game_name,
                    '@MessageID': (str(self.message_id)),
                    '@Type': "NewScoreMessage",
                    '@Receiver': self.receiver_ip,
                    '@Sender': self.sender_ip,
                    '@xmlns:xsd': "http://www.w3.org/2001/XMLSchema",
                    '@xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                    "NewScore":
                        {
                            '@GameName': self.game_name,
                            '@EntryName': self.entry_name,
                            '@SchoolName': self.school_name,
                            '@Score': str(self.score)
                        }
                }
        }
        xml = xmltodict.unparse(score, pretty=True, encoding='UTF-16')
        HOST = "127.0.0.1"  # The server's hostname or IP address
        # define separator between header and data
        # https://github.com/jchristn/WatsonTcp/blob/master/FRAMING.md
        separator = '\r\n\r\n'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = xml.encode()  # data to send
            meta = {}  # any metadata to include
            dic = {"len": len(data), "s": "Normal", 'md': meta}
            header = json.dumps(dic)
            # below sendall could combine into one
            s.sendall(header.encode('utf-8'))
            print("Sent header:", header)
            s.sendall(separator.encode('utf-8'))
            print("Sent separator")
            s.sendall(data)
            print("Sent data:", data)
        print(xml)
    def send_score():
        pass
    def get_top_10(self):
        score = {
            "RequestScoreMessage":
                {
                    '@GameId': self.game_name,
                    '@MessageID': (self.message_id),
                    '@Type': "RequestScoreMessage",
                    '@Receiver': TCP_IP,
                    '@Sender': CLIENT_IP,
                    '@xmlns:xsd': "http://www.w3.org/2001/XMLSchema",
                    '@xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                }
        }
        xml = xmltodict.unparse(score, pretty=True, encoding='UTF-16')
        print(xml)
        # s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s1.connect((TCP_IP, PORT))
        # s1.send(xml)
        pass
    def print_gameplay(self):
        pass
if __name__ == "__main__":
    print(CLIENT_IP)
    # Test creating an XML Score
    # score1 = vars(Score("Jenny", "School NS", 120))
    # Score.create_xml(score1)
    s1 = Score("Jenny", "School NS", 120)
    s2 = Score()
    # Submit new score
    s1.create_xml()
    # Get to 10 for leaderboard
    s2.get_top_10()
    # Score.log_interaction()
    """
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
    """