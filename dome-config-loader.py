import json
import logging
import socket

log = logging.getLogger('dome-udp-server')

FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)

class Controller:
	id = -1
	num_leds = -1
	start_index = -1
	ip = ""

class Led:
	x = -1
	y = -1
	z = -1

class DomeConfig:
	controllers = [Controller()]
	led_list = [Led()]

	def __init__(self, config):
		numControllers = len(config['controllers'])
		numLeds = len(config['led_list'])
		self.controllers = [Controller() for x in range(numControllers)]
		self.led_list = [Led() for x in range(numLeds)]

		for controller in range(numControllers):
			self.controllers[controller].id = config['controllers'][controller]['id']
			self.controllers[controller].num_leds = config['controllers'][controller]['num_leds']
			self.controllers[controller].start_index = config['controllers'][controller]['start_index']
			self.controllers[controller].ip = config['controllers'][controller]['ip']

		for led in range(numLeds):
			self.led_list[led].x = config['led_list'][led]['x']
			self.led_list[led].y = config['led_list'][led]['y']
			self.led_list[led].z = config['led_list'][led]['z']

	def process_command(self, command, target):
		log.debug("%r" % (command,))
		log.debug("%r" % (target,))

def udp_server(host='', port=3663):
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    log.info("Listening on udp %s:%s" % (host, port))
    s.bind((host, port))
    while True:
        data = s.recvfrom(4096)
        yield data

def main():
	config = None

	with open('config.json') as config_file:
		data = json.load(config_file)
		config = DomeConfig(data)

	for data in udp_server():
		config.process_command(data[0], data[1][0])

	return 0

if __name__ == "__main__":
	main()
