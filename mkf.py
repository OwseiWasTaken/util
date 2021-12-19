#! /usr/bin/python3.10
#imports
from util import *


#main
def Main() -> int:
	db = BDP('mkf')
	verbose = db.load()
	if verbose == None:
		verbose = false
	if get('-ev').exists:
		verbose = true
	elif get('-dv').exists:
		verbose = false
	db.save(verbose)

	try:
		ResultFile, CopyFile = get(None).list[0:2]
	except ValueError:
		help()
		exit(2)

	ss(f"echo /home/owsei/Templates/*{CopyFile.lower()}* > /tmp/mkf.cache")
	if verbose:
		ss(f"echo make {ResultFile} from /home/owsei/Templates/*{CopyFile.lower()}*")
	with open("/tmp/mkf.cache",'r') as fl:
		FileData = fl.readline().split()

	if len(FileData) > 1:
		print("To many options!\n")
		print('0 : quit')
		[print(f"{i+1} : {FileData[i].split('/')[-1].split('.')[-1]}") for i in r(FileData)]
		msg = GetInt(">")
		if msg == 0:
			exit(0)
		CopyFile = FileData[msg-1]
	else:
		CopyFile = FileData[0]

	ending = '.' + CopyFile.split('.')[-1]

	if not ResultFile.endswith(ending):
		ResultFile += ending

	if exists(f"./{ResultFile}"):
		print(f"{ResultFile} already exists, overwrite? [y] :",end='')
		ch = GetCh()
		if not ch in ['y','Y']:
			exit(1)
		else:
			print(ch)

	ss(f"cp {CopyFile} {ResultFile}")

	return 0

def help():
	print("""
this program will search for template files in ~/Templates, and copy them to the [Result File Name]

$mkf [File Template name (not complete name)] [Result File Name]

e.g. (create a file called program.py)
$mkf py program
"""[1:-1])
	return 0




#start
if __name__ == '__main__':
	start = tm()
	if "help" in argv and len(argv) == 1:
		ExitCode = help()
	else:
		try:
			ExitCode = Main()
		except KeyboardInterrupt:
			pass



	if get('--debug').exists:
		if not ExitCode:printl("%scode successfully exited in " % color["green"])
		else:printl("%scode exited with error %d in " % (color["red"],ExitCode))
		print("%.3f seconds%s" % (tm()-start,color["nc"]))
	exit(ExitCode)
