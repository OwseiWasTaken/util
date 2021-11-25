#! /usr/bin/python3.10
#imports
from util import *


class Type(IntEnum):
	Comment = iota()
	Func = iota()
	Class = iota()
	Import = iota()
	Count = iota()

@dataclass
class ln:
	Line:int
	Type:int # Type.*
 	Text:str
	def __repr__(this):
		return "%d : %s" % (this.Line, this.Text)

#main
def Main() -> int:
	file = open("/usr/lib/python3.9/util.py")
	lines = file.readlines()
	file.close()
	labels:dict[str:list[ln]] = {"":[]}
	now = ""
	for index in r(lines):
		line = lines[index]
		if line == "#!END\n":break
		if line:
			if line[0] == "#" and line[1] in "()":
				if line[1] == '(':
					now = line[2:-1]
					labels[now] = []
				else:
					now = ""
			elif line[0:3] == "def":
				labels[now].append(ln(index, Type_Func, line[4:line.find('(')]))
			elif line[0:5] == "class":
				if '#' in line or "pass" in line:
					labels[now].append(ln(index, Type_Class, line[6:line.find(':')]))
				else:
					labels[now].append(ln(index, Type_Class, line[6:-1]))
			elif line[0] == '#':
				labels[now].append(ln(index, Type_Comment, line[:-1]))
			elif line[:4] == "from" or line[:6] == "import":
				t = line.replace(' ', '\x1b', 1)
				fs = t.find('\x1b')
				ss = t.find(' ')
				labels[now].append(ln(index, Type_Import, line[fs+1:ss]))
	lk = list(labels.keys())

	if get("--help", '-h').exists or not get().list or not get("--defs").exists:
		printf("0 : No Label\n")
		for i in r(labels.keys()):
			key = lk[i]
			cont = labels[key]
			if i:
				printf("{i} : {s}\n", i, key)

	out = sout
	outfile = False
	if get('-o').exists:
		outs = get('-o').first
		outfile = False
		if outs == "sout":out = sout
		elif outs in ["eout", "serr"]:out = eout
		else:
			out = open(outs, 'w')
			outfile = True

	gl = get().list
	assert [int(gt) >= 0 for gt in gl] or not gl, "all (no -) args must be integers, to print labels' line list"
	if [int(gt) < len(lk) for gt in gl]:
		for gt in gl:
			for l in labels[lk[int(gt)]]:
				fprintf(out, l.Text+'\n')
		if outfile:
			out.close()
	tosave = labels["IMPORTS"] + labels["STUFF"] + labels["CONSTS"]
	if get('--defs').exists:
		for _ in tosave:
			if _.Text[0] != '_':
				tp = _.Type
				if tp == Type_Import:
					printf("include {s}\n", _.Text)
				elif tp == Type_Class:
					printf("def cls {s} @ {i}\n", _.Text.removesuffix(':'), _.Line)
				elif tp == Type_Func:
					printf("def fct {s} @ {i}\n", _.Text, _.Line)
	#TODO modiffs (--comments, --imports ...)
	#TODO replace indexes ( --STUFF -> {stuff's lk index}, --LICENSE -> ...)

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
