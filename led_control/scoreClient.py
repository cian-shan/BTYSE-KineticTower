import socket
import json
import time
import xmltodict
from score import Score
import time


class ScoreClient:
    def __init__(self, game_name="Kinetic Tower", port=9000, host_ip='127.0.0.1',
                 client_ip=socket.gethostbyname(socket.gethostname()) ):
        self.game_name = game_name
        self.port = port
        self.host_ip = host_ip
        self.client_ip = client_ip
        self.attempt_num = 0
        # If the server does not accept a score add it to the queue, try send queue
        self.score_queue = []

    def submit_score(self, entry_name, school_name, score):

        new_score = Score(score_client=self, entry_name=entry_name, school_name=school_name, score=score)

        score = {
            "NewScoreMessage": {
                "@GameId": self.game_name,
                "@MessageId": (str(new_score.message_id)),
                "@Type": "NewScoreMessage",
                "@Receiver": self.host_ip,
                "@Sender": self.client_ip,
                "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "NewScore": {
                    "@GameName": self.game_name,
                    "@EntryName": new_score.entry_name,
                    "@SchoolName": new_score.school_name,
                    "@Score": str(new_score.score),
                },
            }
        }
        xml = xmltodict.unparse(score, pretty=True, encoding="UTF-16")

        # define separator between header and data
        # https://github.com/jchristn/WatsonTcp/blob/master/FRAMING.md
        separator = "\r\n\r\n"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((self.host_ip, self.port))
            data = xml.encode()  # data to send
            meta = {}  # any metadata to include
            dic = {"len": len(data), "s": "Normal", "md": meta}
            header = json.dumps(dic)
            # below sendall could combine into one
            s.sendall(header.encode("utf-8"))
            s.sendall(separator.encode("utf-8"))
            s.sendall(data)
            print(f"Score data sent:\n {xml}")

            # Get ack from server
            ack_header = s.recv(1024)
            ack_header_xml = ack_header.decode().strip()
            clean_ack_header = ack_header_xml.replace("{\"s\":\"Normal\",\"len\":", "")
            ack_header_len = clean_ack_header.replace("}", "")
            ack = s.recv(int(ack_header_len))

            ack_xml = ack.decode().strip()
            ack_msg = xmltodict.parse(ack_xml, encoding="UTF-16")
            ack_decode = ack_msg["MessageReceived"]
            rx_msg_id = ack_decode["@Id"].replace("(", "")
            rx_msg_id = rx_msg_id.replace(")", "")

            if int(rx_msg_id) == int(new_score.message_id):
                print("Ack received from server")
            else:
                raise ConnectionError("No ack from server")


    def get_top_10(self):
        """
        Gets list of top ten results for a game
        """
        get_top_10 = {
            "RequestScoresMessage": {
                "@GameId": self.game_name,
                "@MessageID": (id(self)),
                "@Type": "RequestScoresMessage",
                "@Receiver": self.host_ip,
                "@Sender": self.client_ip,
                "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            }
        }

        xml = xmltodict.unparse(get_top_10, pretty=True, encoding="UTF-16")
        print(xml)
        # define separator between header and data
        # https://github.com/jchristn/WatsonTcp/blob/master/FRAMING.md
        separator = "\r\n\r\n"
        # Try to capture top 10 list
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((self.host_ip, self.port))
                data = xml.encode()  # data to send
                meta = {}  # any metadata to include
                dic = {"len": len(data), "s": "Normal", "md": meta}
                header = json.dumps(dic)
                # below sendall could combine into one
                s.sendall(header.encode("utf-8"))
                s.sendall(separator.encode("utf-8"))
                s.sendall(data)
                print("Request for 10 Top sent")
                # Expecting 1024 bytes back from server
                
                top_10_header = s.recv(1024)
                header_xml = top_10_header.decode().strip()
                clean_header = header_xml.replace("{\"s\":\"Normal\",\"len\":", "")
                header_length = clean_header.replace("}", "")

                print("Bytes to get in 10 TOP: ", int(header_length))
                top_10_bytes = s.recv(int(header_length))
                print("Bytes Recieved in 1st req: ", len(top_10_bytes))
                # Make sure all data is collected
                while len(top_10_bytes) != int(header_length):
                    recv_more = s.recv(int(header_length))
                    top_10_bytes = top_10_bytes + recv_more
                
                if len(top_10_bytes) != int(header_length):
                    s.close()
                    raise Exception("Error Gathering Data - will try again")
                else:
                    top_10_xml = top_10_bytes.decode().strip()
                    # print(f"top_10_xml\n\n {top_10_xml}")
                    full_msg = xmltodict.parse(top_10_xml, encoding="UTF-16")
                    # print("full_msg" + str(full_msg))
                    list_of_scores = full_msg["TopScoreListMessage"]["TopScoresList"]["Score"]
                    self.print_top10(list_of_scores)
                    s.close()
                    return list_of_scores

            s.close()
        # If not all data is collected try again until try limit is met
        except Exception as e:
            attempt_limit = 0
            if self.attempt_num < attempt_limit:
                print(self.attempt_num)
                time.sleep(1)
                self.attempt_num += 1
                return self.get_top_10()
            else:
                raise ConnectionError("Cannot Collect 10 Top data")


    def print_top10(self, top_10_list):
        """
            Prints out top 10 list for console
        """
        print("\nLEADERBOARD\n")
        print("Name : \t\t, School:\t\t, Score:")
        for score in top_10_list:
            print(
                score["@EntryName"], "\t\t", score["@SchoolName"], "\t", score["@Score"]
            )
        pass



    list_of_scores = None

if __name__ == "__main__":
    demo_client = ScoreClient(game_name="Kinetic Tower", client_ip="192.168.7.40", host_ip="192.168.7.210")

    # demo_client.submit_score(entry_name="Test", school_name="ADI", score=10)
    for i in range(0, 10):
        time.sleep(1)
        demo_client.get_top_10()
    
