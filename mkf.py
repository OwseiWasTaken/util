#! /usr/local/bin/python3.11
# imports
from util import *


# main
def Main() -> int:
	try:
		gn = get("").list
		if len(gn) == 2:
			ResultFile, CopyFile = gn[0], gn[1]
		elif len(gn) == 1:
			ResultFile = gn[0]
			if '.' in ResultFile:
				CopyFile = '.'+ResultFile.split('.')[-1]
			else:
				help()
				return 3
		else:
			help()
			return 4
	except ValueError:
		help()
		return 2

	ss(f"echo ~/Templates/*{CopyFile.lower()}* > /tmp/mkf.cache")
	if get("-v").exists:
		ss(f"echo make {ResultFile} from ~/Templates/*{CopyFile.lower()}*")
	with open("/tmp/mkf.cache", "r") as fl:
		FileData = fl.readline().split()

	if len(FileData) > 1:
		print("To many options!\n")
		print("0 : quit")
		[
			print(f"{i+1} : {FileData[i].split('/')[-1].split('.')[-1]}")
			for i in r(FileData)
		]
		msg = GetInt(">")
		if msg == 0:
			return 0
		CopyFile = FileData[msg - 1]
	else:
		CopyFile = FileData[0]

	ending = "." + CopyFile.split(".")[-1]

	if not ResultFile.endswith(ending):
		ResultFile += ending

	if exists(f"./{ResultFile}"):
		print(f"{ResultFile} already exists, overwrite? [y] :", end="")
		ch = GetCh()
		if not ch in ["y", "Y"]:
			return 1
		else:
			print(ch)

	ss(f"cp {CopyFile} {ResultFile}")

	return 0


def help():
	print(
		"""
this program will search for template files in ~/Templates, and copy them to the [Result File Name]

%s [Result File Name] [File Template name (not complete name)]

e.g. (create a file called program.py)
%s program ytho
"""[
			1:-1
		]
		% (argv[0], argv[0])
	)
	return 0


#start
if __name__ == '__main__':
	start = tm()
	ExitCode = Main()

	if get('--debug').exists:
		if not ExitCode:
			printl("%scode successfully exited in " % COLOR.green)
		else:
			printl("%scode exited with error %d in " % (COLOR.red,ExitCode))
		print("%.3f seconds%s" % (tm()-start,COLOR.nc))
	exit(ExitCode)
