import socket
import argparse
import re


class TCPServer:

    def __init__(self, server, port):
        self.server = server
        self.port = int(port)
        self.address = (self.server, self.port)
        self.socket_server = None

    def create_tcp_server(self) -> None:
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind(self.address)
        self.socket_server.listen()
        print(f'Server is launched at {self.server}:{self.port}')
        print("To stop server press 'Ctrl+C' or receive 'Stop server' from client")

    def check_re(self, data: str) -> re.Match | bool:
        # Формат входных данных "BBBB NN HH:MM:SS.zhq GG\r"
        pattern = """
        (\d\d\d\d)\                 # BBBB (sportsmen_no)
        (\w\d)\                     # NN (channel_id)
        (([2][0-3]|[0-1][0-9]):     # HH (hours)
        [0-5][0-9]:                 # MM (minutes)
        [0-5][0-9]\.\d{3})\         # SS.zhq (seconds)
        (\d\d)                      # GG (group_no)
        \\r                         # carriage return symbol \r
        """
        match_result = re.match(pattern, data, flags=re.VERBOSE)
        if match_result:
            return match_result
        else:
            return False

    def get_data(self) -> bool:
        connection, address = self.socket_server.accept()
        print(f"New connection from {address}")

        data = connection.recv(1024).decode()
        if data == "Stop server":
            return False            # if 'Stop server' message received from client

        result = self.check_re(data)
        if result:
            connection.send('Data is correct'.encode())
            sportsmen_no, channel_id, time, hours, group_no = result.groups()
            if group_no == '00':
                print(f"спортсмен, нагрудный номер {sportsmen_no} прошёл отсечку {channel_id} в {time[:-2]}")
                self.write_to_log(sportsmen_no, channel_id, time, group_no)
                connection.close()
            else:
                self.write_to_log(sportsmen_no, channel_id, time, group_no)
                connection.close()
            return True
        else:
            connection.send('Wrong format data'.encode())
            print("Wrong format data")
            return True

    def write_to_log(self, *data) -> None:
        sportsmen_no, channel_id, time, group_no = data
        with open("log.txt", 'a') as f:
            print(f"{sportsmen_no} {channel_id} {time[:-2]} {group_no}\r"
                  f"спортсмен, нагрудный номер {sportsmen_no} прошёл отсечку {channel_id} в {time[:-2]}", file=f)
