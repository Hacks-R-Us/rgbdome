import random
from subprocess import call

def main():
    packet = ""
    for i in range(10460):
        for i in range(3):
            packet += str(random.randint(0, 255))
    with open('packet.txt', 'w') as f:
        f.write(packet)

if __name__ == "__main__":
    main()