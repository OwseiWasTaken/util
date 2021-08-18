#! /usr/bin/python3.9
#imports
from util import *


#main
def Main() -> int:

	try:
		CopyFile,ResultFile = get(None).list[0:2]
	except ValueError:
		help()
		exit(2)

	ss(f"echo /home/owsei/Templates/*{CopyFile}* > /tmp/mkf.cache")
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
		if GetCh().lower() != 'y':
			exit(1)

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
	if "help" in argv:
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
