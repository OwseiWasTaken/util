#! /usr/bin/python3.9
#imports
from util import *


#main
def Main() -> int:

	try:
		ResultFile, CopyFile = get(None).list[0:2]
		print(f"make {ResultFile} from ~/Templates/{CopyFile}")
	except ValueError:
		help()
		exit(2)

	ss(f"echo /home/owsei/Templates/*{CopyFile.lower()}* > /tmp/mkf.cache")
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
			printl(ch)

	ss(f"cp {CopyFile} {ResultFile}")

	return 0

def help():
	print("""
this program will search for template files in ~/Templates, and copy them to the [Result File Name]

the program will search for a template file with a wildcard before and after the file name

$mkf [Result File Name] [File Template name]

e.g. (create a file called program.py)
$mkf program pyt
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
