import socket
import sys

def udp_server(host='192.168.100.10', port=10460):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host, port))
    while True:
        data = s.recvfrom(10460*3)
        yield data

def main():
	config = None

	for data in udp_server(sys.argv[1]):
		print data

if __name__ == "__main__":
    main()