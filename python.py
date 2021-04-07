#! /usr/bin/python3.9
#imports
from util import *

#main
class Program:
	def __init__(this,argv):
		# declare vars
		this.argv = argv
		this.argk = list(argv.keys())


	def Main(this):



		return 0

#start
if __name__ == '__main__':
	argv.pop(0)
	argv = argv_assing(argv)

	if (debug:='--debug' in argv.keys()):
		start = tm()

	exit_code = Program(argv).Main()

	if debug:
		if not exit_code:print(f'{color["green"]}code successfully exited in',end='')
		else:print(f'{color["red"]}code exited with error {exit_code} in',end='')
		print(f' {round(tm()-start,5)} seconds{color["nc"]}')
	exit(exit_code)
