#! /usr/bin/python3.9
#imports
from util import *


#main
def Main(argv):
	argk = list(argv.keys())
	def	get(indicators):
		nonlocal argv,argk
		other = []
		for indicator in indicators:
			if indicator in argk:
				other.append(argv[indicator])
		return other




	return 0






#start
if __name__ == '__main__':
	argv = ArgvAssing(argv[1:])
	start = tm()
	ExitCode = Main(argv)

	if '--debug' in argv.keys():
		if not ExitCode:print(f'{color["green"]}code successfully exited in',end='')
		else:print(f'{color["red"]}code exited with error {ExitCode} in',end='')
		print(f' {round(tm()-start,5)} seconds{color["nc"]}')
	exit(ExitCode)
