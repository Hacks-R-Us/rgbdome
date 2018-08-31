import json
import logging
import socket

from BigPacketSender import BigPacketSender
from DomeJSSender import DomeJSSender
from DomeConfig import DomeConfig

#############################
#			CONFIG			#
#############################
DOMEJS_URL = "http://localhost:8080/"

CONTROLLER_PORT = 10460

ADDRESSABLE_LED_SERVER_HOST = "5202:2234:1046:0000:0000:0000:0000:0001"
ADDRESSABLE_LED_SERVER_PORT = 4242

log = logging.getLogger('dome-udp-server')

FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)

class DomeHeadendConfig(DomeConfig):
	domejsSender = None
	addressableLEDSender = None
	controllerPort = -1

	def __init__(self, config, domejs_host, domejs_port, addressable_led_server_host, addressable_led_server_port, controller_port):
		super(DomeHeadendConfig, self).__init__(config)
		self.domejsSender = DomeJSSender(DOMEJS_URL)
		# self.addressableLEDSender = BigPacketSender(addressable_led_server_host, addressable_led_server_port)
		self.controllerPort = controller_port

	def process_command(self, command):
		log.debug("%r" % ("LEDS:",))
		if len(command) == (self.numLeds * 3):
			log.debug("%r" % ("Valid",))
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			for currentController in range(self.numControllers):
				start = int(self.controllers[currentController].start_index)
				end = int(self.controllers[currentController].start_index + self.controllers[currentController].num_leds)
				sock.sendto(command[start:end], (self.controllers[currentController].ip, self.controllerPort))

		self.domejsSender.send_command(command)
		# self.addressableLEDSender.send(bytearray("$") + command, socket.AF_INET6)
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
		config = DomeHeadendConfig(data, None, None, ADDRESSABLE_LED_SERVER_HOST, ADDRESSABLE_LED_SERVER_PORT, CONTROLLER_PORT)

	for data in udp_server():
		#config.process_command(data[0], data[1][0])
		config.process_command(data[0])

	return 0

if __name__ == "__main__":
	main()
