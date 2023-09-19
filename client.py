import socket

SOCKET_ADDRESS = ('localhost', 9090)
MESSAGE = '0002 C1 01:13:02.877 00\n'

my_socket = socket.socket()
my_socket.connect(SOCKET_ADDRESS)
my_socket.send(MESSAGE.encode())
my_socket.close()



