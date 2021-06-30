#! /usr/bin/python3.9
#imports
from util import *


#main
def Main(argv) -> int:
	argk = list(argv.keys())
	def get(*indicators:object) -> list:
		nonlocal argv,argk
		other = []
		for indicator in indicators:
			if indicator in argk:
				other.append(argv[indicator])
		return other

	#CODE HERE#

	return 0






#start
if __name__ == '__main__':
	argv = ArgvAssing(argv[1:])
	start = tm()
	ExitCode = Main(argv)

	if '--debug' in argv.keys():
		if not ExitCode:printl("%scode successfully exited in " % color["green"])
		else:printl("%scode exited with error %d in " % (color["red"],ExitCode))
		print("%.3f seconds%s" % (round(tm()-start,5),color["nc"]))
	exit(ExitCode)
