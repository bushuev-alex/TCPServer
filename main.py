import argparse
from server import TCPServer


parser = argparse.ArgumentParser()
parser.add_argument("--address",
                    default="192.168.0.16",
                    help="Your machine IPv4 address (something like 192.168.100.6)")
parser.add_argument("--port",
                    default="8888",
                    help="Port number, best practice to use number in range 49152-65535")
args = parser.parse_args()


my_server = TCPServer(args.address, args.port)
my_server.create_tcp_server()
while True:
    if not my_server.get_data():
        break
my_server.socket_server.close()
