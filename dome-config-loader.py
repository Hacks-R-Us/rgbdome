import json

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

def main():
	config = None

	with open('config.json') as config_file:
		data = json.load(config_file)
		config = DomeConfig(data)

	return 0

if __name__ == "__main__":
	main()
