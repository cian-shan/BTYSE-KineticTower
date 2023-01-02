import socket
import json
import time
import xmltodict

# TCP_IP = '127.0.0.1'
# HOST = '169.254.207.119'
HOST = "192.168.0.15"
PORT = 9000
CLIENT_IP = socket.gethostbyname(socket.gethostname())
GAME_NAME = "Kinetic Tower"


class Score:
    def __init__(self, entry_name=None, school_name=None, score=None):
        self.game_name = GAME_NAME
        self.entry_name = entry_name
        self.school_name = school_name
        self.score = score
        self.message_id = id(self)
        self.receiver_ip = str(HOST)
        self.sender_ip = str(CLIENT_IP)
        self.attempt_num = 0

    def submit_score(self):

        score = {
            "NewScoreMessage": {
                "@GameId": self.game_name,
                "@MessageID": (str(self.message_id)),
                "@Type": "NewScoreMessage",
                "@Receiver": self.receiver_ip,
                "@Sender": self.sender_ip,
                "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "NewScore": {
                    "@GameName": self.game_name,
                    "@EntryName": self.entry_name,
                    "@SchoolName": self.school_name,
                    "@Score": str(self.score),
                },
            }
        }

        xml = xmltodict.unparse(score, pretty=True, encoding="UTF-16")

        # define separator between header and data
        # https://github.com/jchristn/WatsonTcp/blob/master/FRAMING.md
        separator = "\r\n\r\n"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = xml.encode()  # data to send
            meta = {}  # any metadata to include
            dic = {"len": len(data), "s": "Normal", "md": meta}
            header = json.dumps(dic)
            # below sendall could combine into one
            s.sendall(header.encode("utf-8"))
            #print("Sent header:", header)
            s.sendall(separator.encode("utf-8"))
            #print("Sent separator")
            s.sendall(data)
            #print("Sent data:", data)
            print("Score data sent")
        # print(xml)

    def get_top_10(self):
        get_top_10 = {
            "RequestScoresMessage": {
                "@GameId": self.game_name,
                "@MessageID": (str(self.message_id)),
                "@Type": "RequestScoresMessage",
                "@Receiver": self.receiver_ip,
                "@Sender": self.sender_ip,
                "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            }
        }

        xml = xmltodict.unparse(get_top_10, pretty=True, encoding="UTF-16")

        # define separator between header and data
        # https://github.com/jchristn/WatsonTcp/blob/master/FRAMING.md
        separator = "\r\n\r\n"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = xml.encode()  # data to send
            meta = {}  # any metadata to include
            dic = {"len": len(data), "s": "Normal", "md": meta}
            header = json.dumps(dic)
            # below sendall could combine into one
            s.sendall(header.encode("utf-8"))
            #print("Sent header:", header)
            s.sendall(separator.encode("utf-8"))
            #print("Sent separator")
            s.sendall(data)
            #print("Sent data:", data)
            print("Request for 10 Top sent")

            # Try to capture top 10 list
            try:
                top_10_header = s.recv(1024)
                top_10_bytes = s.recv(1286)
                print("Bytes Recieved: ", len(top_10_bytes))
                header_xml = top_10_header.decode().strip()
                
                clean_header = header_xml.replace("{\"s\":\"Normal\",\"len\":", "")
                header_length = clean_header.replace("}", "")
                #header = xmltodict.parse(clean_header, encoding="UTF-16")
                #print(clean_header)

                # Make sure all data is collected
                if len(top_10_bytes) < int(header_length):
                    raise Exception("Error Gathering Data - will try again")

                top_10_xml = top_10_bytes.decode().strip()
                s.close()

                # print("\n\nTOP10")
                # print(top_10_xml)

                full_msg = xmltodict.parse(top_10_xml, encoding="UTF-16")

                list_of_scores = full_msg["TopScoreListMessage"]["TopScoresList"]["Score"]

                return list_of_scores

                # self.print_top10(list_of_scores)

            # If not all data is collected try again until try limit is met
            except Exception as e:
                print(e)
                attempt_limit = 2
                if self.attempt_num < attempt_limit:
                    time.sleep(1)
                    self.attempt_num += 1
                    self.get_top_10()
                else:
                    print("Cannot Collect 10 Top data")

        

    def print_top10(self, top_10_list):

        print(top_10_list)

        print("\nLEADERBOARD\n")
        print("Name : \t\t, School:\t\t, Score:")

        for score in top_10_list:
            print("\n")
            print(
                score["@EntryName"], "\t\t", score["@SchoolName"], "\t", score["@Score"]
            )
        pass


if __name__ == "__main__":
    # This program tests adding scores and retriving score from the central leaderboard server

    print(CLIENT_IP)

    # Test creating an XML Score
    # score1 = vars(Score("Jenny", "School NS", 120))
    # Score.create_xml(score1)
    s1 = Score("Kenny", "School NS", 123)
    s2 = Score()
    # Submit new score
    # s1.create_xml()
    # Get to 10 for leaderboard
    s2.get_top_10()
    # Score.log_interaction()

    # Below this was messing with adding colour to the console output
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
