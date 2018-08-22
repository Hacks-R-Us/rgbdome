import socket
import time

UDP_IP = "localhost"
UDP_PORT = 3663
MAX_LED = 30

for led in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
	for rgb in led:
		print rgb

OFF = bytearray(0 for i in range(MAX_LED*3))
ON = bytearray(255 for i in range(MAX_LED*3))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def chase(r=255, g=255, b=255, sleep = 0.01):
	for i in range(0, MAX_LED):
		output = bytearray(0 for i in range(MAX_LED*3))
		col = (r << 16) + (g << 8) + (b)
		output[i*3:(i*3)+6] = col.to_bytes(6,byteorder='big')
		sock.sendto(output, (UDP_IP, UDP_PORT))
		time.sleep(sleep)
	sock.sendto(OFF, (UDP_IP, UDP_PORT))
	
def rainbow(sleep = 0.2):
	pass

while True:
	sock.sendto(ON, (UDP_IP, UDP_PORT))
	time.sleep(1)
	sock.sendto(OFF, (UDP_IP, UDP_PORT))
	time.sleep(1)