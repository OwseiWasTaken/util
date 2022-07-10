#! /usr/bin/python3.10
# imports
from util import *

class Todo:
	def __init__(this, frm, at, name, rank, desc):
		this.frm = frm
		this.at = at
		this.name = name
		this.rank = rank
		this.desc = desc
	def __str__(this):
		return f"{this.name} - {this.desc}"

##TODO(3): fix this
def GetTodos(file:str) -> list[Todo]:
	todos:list[Todo] = []
	fs:str
	line:str
	rank:int
	name:str
	with open(file, "r") as f:
		fs=f.readlines()
	for i in r(fs):
		line = fs[i]
		if not line:
			continue
		if not line[0] == '#':
			continue
		if not line[0:6] == "#TODO(":
			continue
		if line.endswith("\n"):
			line = line[:-1]
		line = line[6:]
		rank = line[:line.find(')')]
		line = line[line.find(')')+1:]
		name = line[:line.find(':')]
		line = line[line.find(':')+2:]

		todos.append(Todo(file, i+1, name, rank, line))
	return sorted(todos, key=lambda x: x.rank)

TABSIZE	= 2
TAB = " "*TABSIZE
AT = RGB(100,100,255)+'@'+RGB(255,255,255)

# main
def Main() -> int:
	files = get("").list
	todos:list[Todo] = []
	for file in files:
		todos += GetTodos(file)
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
