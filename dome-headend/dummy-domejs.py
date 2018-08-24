import socket

def udp_server(host='', port=1444):
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host, port))
    while True:
        data = s.recvfrom(10460*3)
        yield data

def main():
    for data in udp_server():
        print(data[0])

    return 0

if __name__ == "__main__":
    main()