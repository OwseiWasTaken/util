#! /usr/bin/python3.10
# imports
from util import *

comment = {
	".py":"#",
	".go":"//",
	".c":"//",
	".cpp":"//",
}

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
			raise Exception(f"Todo ({file}{AT}{i+1}) doesn't have a name")
		else:
			name = ' '+(line[:line.find(':')].lstrip())
			line = " - "+line[line.find(':')+2:]

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
		#TODO(4) Todo on txt: make todos.py's load from .txt add .txt's todoes to file's todo list
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
	if get("--nd").exists:
		for td in todos:
			if td.frm != f:
				f = td.frm
				print(f"\n{f}:")
			print(TAB+f"{td.rank}{AT}{td.at} {td.name}")
	else:
		for td in todos:
			if td.frm != f:
				f = td.frm
				print(f"\n{f}:")
			print(TAB+f"{td.rank}{AT}{td.at} "+str(td))
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
