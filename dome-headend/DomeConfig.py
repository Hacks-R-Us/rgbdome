import socket
import logging
from BigPacketSender import BigPacketSender

log = logging.getLogger('dome-udp-server')

class Controller:
	id = -1
	num_leds = -1
	start_index = -1
	ip = ""

class Led:
	x = -1
	y = -1
	z = -1

class DomeConfig(object):
	numControllers = -1
	numLeds = -1
	controllers = [Controller()]
	led_list = {Led()}

	def __init__(self, config):
		self.numControllers = len(config['controllers'])
		self.numLeds = len(config['led_list'])
		self.controllers = [Controller() for x in range(self.numControllers)]
		self.led_list = {}

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
		return 1