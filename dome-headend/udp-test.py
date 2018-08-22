import socket
import sys

HOST, PORT = "localhost", 3663
data = " ".join(sys.argv[1:])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.send(bytes(data, "utf-8"), (HOST, PORT))