import socket

SOCKET_ADDRESS = ('localhost', 9090)
MESSAGE = '0002 C1 01:13:02.877 00\n'

my_socket = socket.socket()
my_socket.connect(SOCKET_ADDRESS)
my_socket.send(MESSAGE.encode())
my_socket.close()


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
