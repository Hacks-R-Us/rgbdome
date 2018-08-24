def main():
	output = ""
	for i in range(10460):
		output += '{"x": "' + str(i * 3) + '", "y": "' + str((i * 3) + 1) + '", "z": "' + str((i * 3) + 2) + '"},\n'
	with open('dummyconf.txt', 'w') as f:
		f.write(output)
main()
