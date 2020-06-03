import socket
import time
import argparse
import math

UDP_IP = "192.168.100.1"
UDP_PORT = 3663
MAX_LED = 10460

OFF = bytearray(0 for i in range(MAX_LED*3))
ON = bytearray(255 for i in range(MAX_LED*3))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def flash(sleep=1):
    sock.sendto(ON, (UDP_IP, UDP_PORT))
    time.sleep(sleep)
    sock.sendto(OFF, (UDP_IP, UDP_PORT))
    time.sleep(sleep)


def chase(r=255, g=255, b=255, sleep=0.01):
    """Chase a single colour around the dome in order"""
    output = bytearray(0 for i in range(MAX_LED*3))
    for i in range(0, MAX_LED):
        output[i * 3] = r
        output[i * 3 + 1] = g
        output[i * 3 + 2] = b

        sock.sendto(output, (UDP_IP, UDP_PORT))
        time.sleep(sleep)

    sock.sendto(OFF, (UDP_IP, UDP_PORT))
    time.sleep(sleep)


def rainbow(sleep=0.05):
    """Construct a sort-of sinusoidal wave pattern"""
    wave_hz = 1
    r_offset = 0
    g_offset = 2 * math.pi / 3
    b_offset = 4 * math.pi / 3

    colours = bytearray(0 for i in range(MAX_LED * 3))

    dome_time = 0

    while True:
        dome_time += sleep
        for i in range(0, MAX_LED):
            relativeTime = dome_time * \
                (2 * math.pi * wave_hz) + \
                (2 * math.pi * i / MAX_LED)

            r_val = int(255 * (math.sin(relativeTime + r_offset) / 2 + 0.5))
            g_val = int(255 * (math.sin(relativeTime + g_offset) / 2 + 0.5))
            b_val = int(255 * (math.sin(relativeTime + b_offset) / 2 + 0.5))

            colours[i * 3] = r_val
            colours[i * 3 + 1] = g_val
            colours[i * 3 + 2] = b_val

        sock.sendto(colours, (UDP_IP, UDP_PORT))
        time.sleep(sleep)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        help="Which mode should we run in? One of flash, chase, rainbow"
    )

    args = parser.parse_args()

    while True:
        if args.mode == "flash":
            flash()
        elif args.mode == "chase":
            chase()
        elif args.mode == "rainbow":
            rainbow()
