#! /usr/bin/python3.10
# imports
from util import *


comment = {
	".py":"#",
	".go":"//",
	".c":"//",
	".cpp":"//",
}
rankcolor = {
	'1':RGB(255,0,0),
	'2':RGB(250,100,100),
	'3':RGB(250,80,10),
	'4':RGB(100,200,100),
	'5':RGB(0,255,0),
	'6':RGB(40,150,180),
	'7':RGB(100,100,255),
}
nodesc = RGB(140,140,140)+"No Descriotion"+RGB(255,255,255)

class Todo:
	def __init__(this, frm, at, name, rank, desc):
		this.frm = frm
		this.at = at
		this.name = name
		this.rank = rank
		this.desc = desc
	def __str__(this):
		return f"{this.name}{this.desc}"

def GetTodos(file:str) -> list[Todo]:
	cmnt = comment[file[file.find('.'):]]
	cmntl = len(cmnt)
	todos:list[Todo] = []
	fs:str
	line:str
	rank:int
	nm:bool
	name:str
	with open(file, "r") as f:
		fs=f.readlines()
	for i in r(fs):
		line = fs[i].lstrip()
		if not line:
			continue
		if not line[0:cmntl] == cmnt:
			continue
		if not line[0:5+cmntl] == cmnt+"TODO(":
			continue
		if line.endswith("\n"):
			line = line[:-1]
		line = line[5+cmntl:]
		rank = line[:line.find(')')]
		line = line[line.find(')')+1:]
		if line.find(':') == 0:
			name = line[2:]
			line = ": "+nodesc
		else:
			if ':' in line:
				name = (line[:line.find(':')].lstrip())
				line = ": "+line[line.find(':')+2:]
			else:
				name = line[1:]
				line = ": "+nodesc

		todos.append(Todo(file, i+1, name, rank, line))

	return sorted(todos, key=lambda x: x.rank)

TABSIZE	= 2
TAB = " "*TABSIZE
AT = RGB(100,100,255)+'@'+RGB(255,255,255)

def LoadFL(fl) -> list[str]:
	ret:list[str] = []
	with open(fl, "r") as f:
		fs=f.readlines()
	for line in fs:
		line = line.strip()
		if not line:
			continue
		if line[0] == "/":
			ret.append(line)
		elif line[0:2] == "./":
			ret.append(line[2:])
	return ret


# main
def Main() -> int:
	files = get("").list
	if len(files) == 0:
		if exists("todos.txt"):
			files = ["todos.txt"]
	fls:list[str] = []


	for file in files:
		if file.endswith(".txt"):
			fls += LoadFL(file)
		else:
			fls.append(file)

	todos:list[Todo] = []
	for file in fls:
		todos += GetTodos(file)

	if len(todos) == 0:
		return 1

	f = todos[0].frm
	print(f"{f}:")
	if get("--sd").exists:
		for td in todos:
			if td.frm != f:
				f = td.frm
				print(f"\n{f}:")
			print(TAB+f"{rankcolor.get(td.rank,'')}{td.rank}{RGB(255,255,255)}{AT}{td.at} "+str(td))
	else:
		for td in todos:
			if td.frm != f:
				f = td.frm
				print(f"\n{f}:")
			print(TAB+f"{rankcolor.get(td.rank,'')}{td.rank}{RGB(255,255,255)}{AT}{td.at} {td.name}")
	return 0


# start
if __name__ == "__main__":
	start = tm()
	ExitCode = Main()

	if get("--debug").exists:
		if not ExitCode:
			printl("%scode successfully exited in " % COLOR.green)
		else:
			printl("%scode exited with error %d in " % (COLOR.red, ExitCode))
		print("%.3f seconds%s" % (tm() - start, COLOR.nc))
	exit(ExitCode)
