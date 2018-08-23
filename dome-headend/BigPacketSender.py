import socket

class BigPacketSender():
    host = None
    port = None
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def send(self, packet, type):
        sock = socket.socket(type, socket.SOCK_DGRAM)
        sock.sendto(packet, (self.host, self.port))