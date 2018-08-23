import json
import logging
import socket

#############################
#			CONFIG			#
#############################
DOMEJS_HOST = "localhost"
DOMEJS_PORT = 1444

CONTROLLER_PORT = 10460

log = logging.getLogger('dome-udp-server')

FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)

class BigPacketSender():
    host = None
    port = None
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def send(self, packet):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(packet, (self.host, self.port))

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
	numControllers = -1
	numLeds = -1
	controllers = [Controller()]
	led_list = {Led()}
	domejsSender = None

	def __init__(self, config):
		self.numControllers = len(config['controllers'])
		self.numLeds = len(config['led_list'])
		self.controllers = [Controller() for x in range(self.numControllers)]
		self.led_list = {}
		self.domejsSender = BigPacketSender(DOMEJS_HOST, DOMEJS_PORT)

		for controller in range(self.numControllers):
			self.controllers[controller].id = config['controllers'][controller]['id']
			self.controllers[controller].num_leds = config['controllers'][controller]['num_leds']
			self.controllers[controller].start_index = config['controllers'][controller]['start_index']
			self.controllers[controller].ip = config['controllers'][controller]['ip']

		self.controllers.sort(key=lambda x: x.start_index, reverse = False)
		for controller in self.controllers:
			log.debug("%r" % (controller.id,))

		for led in range(self.numLeds):
			newLed = Led()
			newLed.x = config['led_list'][led]['x']
			newLed.y = config['led_list'][led]['y']
			newLed.z = config['led_list'][led]['z']
			self.led_list[led] = newLed # TODO: Replace with ipv6

	def process_command(self, command):
		log.debug("%r" % ("LEDS:",))
		if len(command) == (self.numLeds * 3):
			log.debug("%r" % ("Valid",))
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			for currentController in range(self.numControllers):
				start = int(self.controllers[currentController].start_index)
				end = int(self.controllers[currentController].start_index + self.controllers[currentController].num_leds)
				#log.debug("%r" % (start,))
				#log.debug("%r" % (end,))
				sock.sendto(command[start:end], (self.controllers[currentController].ip, CONTROLLER_PORT))
				#log.debug("%r" % (command[start:end],))

		self.domejsSender.send(command)
		return 0

def udp_server(host='192.168.100.1', port=3663):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    log.info("Listening on udp %s:%s" % (host, port))
    s.bind((host, port))
    while True:
        data = s.recvfrom(10460*3)
        yield data

def main():
	config = None

	with open('config.json') as config_file:
		data = json.load(config_file)
		config = DomeConfig(data)

	for data in udp_server():
		#config.process_command(data[0], data[1][0])
		config.process_command(data[0])

	return 0

if __name__ == "__main__":
	main()
