import socket
import logging

log = logging.getLogger('dome-udp-server')

class BigPacketSender():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def send(self, packet, type):
        sock = socket.socket(type, socket.SOCK_DGRAM)
        sock.sendto(packet, (self.host, self.port))
        log.debug("%r" % (self.host,))