#! /usr/bin/python3.9
#imports
from util import *


#main
class program:
	def __init__(this,argv,argk):
		# declare vars
		this.argv = argv
		this.argk = argk


	def Main(this):



		return 0






#start
if __name__ == '__main__':
	argv = argv_assing(argv[1:])
	argk = list(argv.keys())
	code = program(argv,argk).Main

	if '--debug' in argk:
		start = tm()
		ExitCode = code()

		if not ExitCode:print(f'{color["green"]}code successfully exited in',end='')
		else:print(f'{color["red"]}code exited with error {exit_code} in',end='')
		print(f' {round(tm()-start,5)} seconds{color["nc"]}')
	else:
		ExitCode = code()
	exit(ExitCode)
