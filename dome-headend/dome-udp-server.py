import json
import logging
import socket

from BigPacketSender import BigPacketSender
from DomeConfig import DomeConfig

#############################
#			CONFIG			#
#############################
DOMEJS_HOST = "localhost"
DOMEJS_PORT = 1444

DOMEAPI_HOST = "localhost"
DOMEAPI_PORT = 7778

CONTROLLER_PORT = 10460

ADDRESSABLE_LED_SERVER_HOST = 'localhost'
ADDRESSABLE_LED_SERVER_PORT = 4242

CONTTROLLER_IDS_TO_IPS = {
	"1-1": "192.168.10.101",
	"1-2": "192.168.10.102",
	"1-3": "192.168.10.103",
	"1-4": "192.168.10.104",
	"1-5": "192.168.10.105",
	"2-1": "192.168.10.106",
	"2-2": "192.168.10.107",
	"2-3": "192.168.10.108",
	"2-4": "192.168.10.109",
	"2-5": "192.168.10.110",
	"3-1": "192.168.10.111",
	"3-2": "192.168.10.112",
	"3-3": "192.168.10.113",
	"3-4": "192.168.10.114",
	"3-5": "192.168.10.115",
	"4-1": "192.168.10.116",
	"4-2": "192.168.10.117",
	"4-3": "192.168.10.118",
	"4-4": "192.168.10.119",
	"4-5": "192.168.10.120",
	"5-1": "192.168.10.121",
	"5-2": "192.168.10.122",
	"5-3": "192.168.10.123",
	"5-4": "192.168.10.124",
	"5-5": "192.168.10.125"
}

log = logging.getLogger('dome-udp-server')

FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)

class DomeHeadendConfig(DomeConfig):
	def __init__(self, config, domejs_host, domejs_port, addressable_led_server_host, addressable_led_server_port, controller_port, api_host, api_port, controllerIDsToIps):
		super(DomeHeadendConfig, self).__init__(config, controllerIDsToIps)
		self.domejsSender = BigPacketSender(domejs_host, domejs_port)
		self.addressableLEDSender = BigPacketSender(addressable_led_server_host, addressable_led_server_port)
		self.apiSender = BigPacketSender(api_host, api_port)
		self.controllerPort = controller_port

	def process_command(self, command):
		if len(command) == (self.numLeds * 3):
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			for currentController in range(self.numControllers):
				start = int(self.controllers[currentController].start_index)
				end = int(self.controllers[currentController].start_index + self.controllers[currentController].num_leds)
				sock.sendto(command[start:end], (self.controllers[currentController].ip, self.controllerPort))

			self.domejsSender.send(command, socket.AF_INET)
			self.addressableLEDSender.send(bytearray("$") + command, socket.AF_INET6)
			self.apiSender.send(command, socket.AF_INET)
		return 0

def udp_server(host='localhost', port=3663):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    log.info("Listening on udp %s:%s" % (host, port))
    s.bind((host, port))
    while True:
        data = s.recvfrom(10460*3)
        yield data

def main():
	config = None

	with open('dome.config') as config_file:
		data = json.load(config_file)
		config = DomeHeadendConfig(data, DOMEJS_HOST, DOMEJS_PORT, ADDRESSABLE_LED_SERVER_HOST, ADDRESSABLE_LED_SERVER_PORT, CONTROLLER_PORT, DOMEAPI_HOST, DOMEAPI_PORT, CONTTROLLER_IDS_TO_IPS)

	for data in udp_server():
		#config.process_command(data[0], data[1][0])
		config.process_command(data[0])

	return 0

if __name__ == "__main__":
	main()
