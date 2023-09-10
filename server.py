import socket
import argparse
import re


class TCPServer:

    def __init__(self, server, port):
        self.server = server
        self.port = int(port)
        self.address = (self.server, self.port)
        self.socket_server = None

    def create_tcp_server(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind(self.address)
        self.socket_server.listen()
        print(f'Server is launched at {self.server}:{self.port}')
        print("To stop server press 'Ctrl+C' or receive 'Stop server' from client")

    def check_re(self, data):
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

    def get_data(self):
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

    def write_to_log(self, *data):
        sportsmen_no, channel_id, time, group_no = data
        with open("log.txt", 'a') as f:
            print(f"{sportsmen_no} {channel_id} {time[:-2]} {group_no}\r"
                  f"спортсмен, нагрудный номер {sportsmen_no} прошёл отсечку {channel_id} в {time[:-2]}", file=f)


parser = argparse.ArgumentParser()
parser.add_argument("address", help="Your machine IPv4 address (something like 192.168.100.6)")
parser.add_argument("port", help="Port number, best practice to use number in range 49152-65535")
args = parser.parse_args()


tcp_server = TCPServer(args.address, args.port)
tcp_server.create_tcp_server()
while True:
    if not tcp_server.get_data():
        break
tcp_server.socket_server.close()


# Пример клиента, отсылающего запрос к серверу
"""
import socket

SOCKET_ADDRESS = ('192.168.100.6', 9090)
MESSAGE = "0012 C1 01:13:02.877 00\r"

my_socket = socket.socket()
my_socket.connect(SOCKET_ADDRESS)
my_socket.send(MESSAGE.encode())
my_socket.close() 
"""


# Пример клиента, отсылающего запрос к серверу (используем модуль telnetlib)
"""
from telnetlib import Telnet
MESSAGE_1 = "0012 C1 23:59:59.009 00\r"  # correct data
MESSAGE_2 = "0012 C1 51:13:02.877 00\r"  # incorrect data
MESSAGE_3 = "Stop server"                # command to stop server

telnet = Telnet('192.168.100.6', port=9090)
telnet.write(MESSAGE_1.encode())
print(telnet.read_all().decode()) 
"""
