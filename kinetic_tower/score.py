import socket
import json
import time
import xmltodict

# TCP_IP = '127.0.0.1'
HOST = '169.254.207.119'
HOST = '127.0.0.1'
#HOST = "192.168.47.210"
PORT = 9000
CLIENT_IP = socket.gethostbyname(socket.gethostname())
GAME_NAME = "Kinetic Tower"

class Score:
    def __init__(self, score_client, entry_name=None, school_name=None, score=None):
        self.entry_name = entry_name
        self.school_name = school_name
        self.score = score
        self.message_id = id(self)

    list_of_scores = None

    

    

if __name__ == "__main__":
    # This program tests adding scores and retrieving score from the central leaderboard server

    print(CLIENT_IP)

    # Test creating an XML Score
    s1 = Score("Test", "ADI", 5)
    s1.submit_score()
    # leaderboard_list = Score()
    # list = leaderboard_list.get_top_10()
    # leaderboard_list.print_top10(list)

    # print(list)
    #s2 = Score()

    # Submit new score
    #s1.submit_score()
    # Get to 10 for leaderboard
    # s2.get_top_10()
    # Score.log_interaction()

