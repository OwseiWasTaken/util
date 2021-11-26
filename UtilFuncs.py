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
				labels[now].append(ln(index, Type.Func, line[4:line.find('(')]))
			elif line[0:5] == "class":
				if '#' in line or "pass" in line:
					labels[now].append(ln(index, Type.Class, line[6:line.find(':')]))
				else:
					labels[now].append(ln(index, Type.Class, line[6:-1]))
			elif line[0] == '#':
				labels[now].append(ln(index, Type.Comment, line[:-1]))
			elif line[:4] == "from" or line[:6] == "import":
				t = line.replace(' ', '\x1b', 1)
				fs = t.find('\x1b')
				ss = t.find(' ')
				labels[now].append(ln(index, Type.Import, line[fs+1:ss]))
	lk = labels.keys()
	ll = list(lk)
	GHelp = get('--help', '-h').exists
	GDefs = get('--defs', '-d').exists
	GArgs = get().list
	if not (GHelp + GDefs + len(GArgs)):
		printf("0 : No Label\n")
		for i in r(lk):
			key = ll[i]
			cont = labels[key]
			if i:
				printf("{i} : {s}\n", i, key)

	out = stdout # -o for out file, stdout is default
	outfile = False
	if get('-o').exists:
		outs = get('-o').first
		outfile = False
		if outs == "stdout":
			out = stdout
		elif outs == "stderr":
			out = stderr
		else:
			out = open(outs, 'w')
			outfile = True

	gl = get().list
	for ga in GArgs:
		if ga.isnumeric():
			if not (len(lk) > int(ga) > -1):
				fprintf(stderr, "{i} > {s} > -1", len(lk), ga)
		else:
			fprintf(stderr, "can't convert \"{s}\" to int\n", ga)
	for gt in GArgs:
		for l in labels[list(lk)[int(gt)]]:
			fprintf(out, l.Text+'\n')

	tosave = labels["IMPORTS"] + labels["STUFF"] + labels["CONSTS"]
	if get('--defs').exists:
		for _ in tosave:
			if _.Text[0] != '_':
				tp = _.Type
				if tp == Type.Import:
					fprintf(out, "include {s}\n", _.Text)
				elif tp == Type.Class:
					fprintf(out, "def cls {s} @ {i}\n", _.Text.removesuffix(':'), _.Line)
				elif tp == Type.Func:
					fprintf(out, "def fct {s} @ {i}\n", _.Text, _.Line)
	if outfile:
		out.close()
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
