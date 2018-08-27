import socket
import logging
import math
from BigPacketSender import BigPacketSender

log = logging.getLogger('dome-udp-server')

class Controller:
	def __init__(self):
		self.id = None
		self.num_leds = None
		self.start_index = None
		self.ip = None

class Led:
	def __init__(self):
		self.x = None
		self.y = None
		self.z = None

class DomeConfig(object):
	def __init__(self, config, controllerIDsToIps):
		self.numControllers = len(config['Controllers'])
		self.numLeds = len(config['led_list'])
		self.controllers = [Controller() for x in range(self.numControllers)]
		self.led_list = {}
		self.controllerIDsToIps = controllerIDsToIps

		for controller in range(self.numControllers):
			self.controllers[controller].id = config['Controllers'][controller]['id']
			self.controllers[controller].num_leds = config['Controllers'][controller]['num_leds']
			self.controllers[controller].start_index = config['Controllers'][controller]['start_index']
			rotation = int(self.controllers[controller].id % 5) + 1
			pattern_num = int(math.floor(self.controllers[controller].id/5) * 1) + 1
			self.controllers[controller].ip = self.controllerIDsToIps[str(pattern_num) + "-" + str(rotation)]

		self.controllers.sort(key=lambda x: x.start_index, reverse = False)
		for controller in self.controllers:
			log.debug("%r" % (controller.id,))

		for led in range(self.numLeds):
			newLed = Led()
			newLed.x = config['led_list'][led][0]
			newLed.y = config['led_list'][led][1]
			newLed.z = config['led_list'][led][2]
			self.led_list[led] = newLed # TODO: Replace with ipv6

	def process_command(self, command):
		return 1