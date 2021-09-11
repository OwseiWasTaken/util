#! /usr/bin/python3.9

# util.py imports
from pickle import dump as _PickleDump, load as _PickleLoad, dumps as PickleString, loads as UnpickleString
from json import dump as _JsonDump, load as _JsonLoad
from tty import setraw
from termios import tcgetattr, tcsetattr, TCSADRAIN, TIOCGWINSZ
from fcntl import ioctl

# general imports + util used
from random import randint as rint, choice as ritem
from time import time as tm, sleep as slp, strftime as __ftime__
from sys import argv, exit as exi, getsizeof as sizeof, stdout as sout, stdin as sin, stderr as serr, platform as OS
from os import getcwd as pwd, system as ss, chdir as cd, listdir as _ls, getenv, getlogin, rmdir as _rmdir, get_terminal_size as GetTerminalSize
from os.path import isfile, exists
import re as RegEx

# this file was made by owsei
# this file has a gpl3 lincense or whatever
# you can use it however you want

# REGEXes
# find funcs
# def [a-zA-Z]*
# find typeless funcs
# def .*\(.*\):$
# func class or func
# ^(class|def)
# find double line div
# ^$\n^$

# magic class methods https://www.tutorialsteacher.com/python/magic-methods-in-python

# vars
USER = getlogin()
FuncType = type(lambda a:a )
NoneType = type(None)
iterables = [type(list()), type(set()), type(frozenset())]
class NumberTooBigError(BaseException):pass
infinity = float("inf")
def nop(*a):pass
class noc:pass
ARGV = None# Will be defined later

if OS == "linux":
	# it MAY work in windows, not sure tho
	import gi
	gi.require_version('Notify', '0.7')
	from gi.repository import Notify
	def notify(title="", body="") -> None:
		Notify.init("util.py/func/notify/init")
		Notify.Notification.new(str(title), str(body)).show()
else:
	def notify(*a, **kwa):
		print(f"notify function not yet implemented in uti.py for {OS}\n\
if you want to help, make yout commit at https://github.com/OwseiWasTaken/uti.py")


class time:
	@property
	def sec(this) -> str :
		# _log.add(f'class ( time ) -> sec')
		return __ftime__(f"%S")

	@property
	def min(this) -> str:
		# _log.add(f'class ( time ) -> min')
		return __ftime__(f"%M")

	@property
	def hour(this) -> str:
		# _log.add(f'class ( time ) -> hour')
		return __ftime__("%H")

	@property
	def day(this) -> str:
		# _log.add(f'class ( time ) -> day')
		return __ftime__("%D").split('/')[1]

	@property
	def month(this) -> str:
		# _log.add(f'class ( time ) -> month')
		return __ftime__("%D").split('/')[0]

	@property
	def year(this) -> str:
		# _log.add(f'class ( time ) -> year')
		return __ftime__("%D").split("/")[2]
time = time()

class log:
	def __init__(this, sep=', ', tm=True, file="log") -> object:
		this.tm = tm
		this.sep = sep
		this.LOG = []
		this.add('the log was created')
		this.file = file

	def add(this, *ask) -> None:
		tm = this.tm
		ask=this.sep.join([str(ak) for ak in ask])

		tme = ''
		if tm:tme = f'at {time.day} {time.hour}:{time.min}:{time.sec} : '
		this.LOG.append(f'{tme}{ask}')

	def remove(this, index_or_content:int or str) -> None:

		if type(index_or_content) == int:
			return this.LOG.pop(index_or_content)
		else:
			this.LOG.index(index_or_content)
			return this.LOG.pop(index_or_content)

	def __repr__(this) -> str:
		return f'{this.LOG}'

	def get(this, num:int) -> str:
		return this.LOG[num]

	def __getitem__(this, num:int) -> str:
		return this.LOG[num]

	def __call__(this) -> list:
		return this.LOG

	def __iter__(this) -> None:
		for i in this():
			yield i

	def show(this) -> None:
		for i in this:
			print(i)

	def save(this) -> None:
		with open(this.file, 'w') as SaveFileLog:
			for i in this.LOG:
					SaveFileLog.write(f'{i}\n')

# _log = log()

# formating:
# _log.add(f'[func or class] ([name]) = [{, } args] => [return]')

# e.g.:
# _log.add(f'func (r) = {end, start, jmp} => range')

def r(end:object, start:int=0, jmp:int=1) -> int:
	# _log.add(f'func (r) = {end, start, jmp} => yield')
	try:
		try:
			end = len(end)
		except TypeError:
			end = end.keys()
	except AttributeError:
		end = int(end)

	index = start
	while end > index:
		yield index
		index+=jmp

def AssureType(value:object, types:type, err:bool=True, ErrorMsg=None) -> TypeError or bool:
	# _log.add(f'func (AssureType) = {values, types, err} => TypeError or bool')
	if type(types) != type and type(value) == type:
		value, types = types, value

	if f'{type(value)}' != f'{types}':
		if err:
			if ErrorMsg == None:
					raise TypeError(f"\n\ntype : {type(value)} of {repr(value)} != {types}")
			else:
					raise TypeError(ErrorMsg)
		else:
			return False
	return True

class timer:
	def __init__(this, auto:bool=True) -> object:
		# _log.add(f'class (timer.__init__) = {auto} ')
		this.markers = []
		if auto:this.st = tm()

	def start(this) -> None:
		# _log.add(f'class (timer.start) = None => None')
		this.st = tm()

	def mark(this) -> None:
		# _log.add(f'class (timer.mark) = None => None')
		this.markers.append(this.get())

	def marks(this) -> list[int]:
		# _log.add(f'class (timer.marks) = None => list')
		return this.markers

	def get(this) -> float:
		# _log.add(f'class (timer.get) = None => float')
		return tm() - this.st

	def __call__(this) -> float:
		# _log.add(f'class (timer()) => float')
		if not this.st:
			this.st = tm()
		else:
			return this.get()

	def __iter__(this) -> iter:
		# _log.add(f'class (for i in timer) => yield marks[i]')
		for i in this.markers:
			yield i

	def __repr__(this) -> str:
		# _log.add(f'class (timer) -> __repr__ ')
		return f'{this.get}'

def MakeDict(ls1:[list, tuple], ls2:[list, tuple]) -> dict:
	ls1=list(ls1)
	ls2=list(ls2)

	ret = {x:y for x, y in zip(list(ls1), list(ls2))}
	return ret

def sleep(seg:float=0, sec:float=0, ms:float=0, min:float=0, hour:float=0, day:float=0, IgnoreKBI = True) -> None:
	# _log.add(f'func (sleep) with {seg, min, hour, day}')
	if IgnoreKBI:
		try:
			slp(ms/1000+seg+sec+min*60+hour*3600+day*86400)
		except KeyboardInterrupt:
			exit(0)
	else:
		slp(ms/1000+seg+sec+min*60+hour*3600+day*86400)

def pc(x:int, y:int) -> float:
	# _log.add(f'func (pc) with {x, y}')
	return int(x/100*y)

def even(var:int) -> bool:
	# _log.add(f'func (even) with ({var})')
	return not var%2

def odd(var:int) -> bool:
	# _log.add(f'func (even) with ({var})')
	return var%2

def lst1(lst:object) -> object:
	# _log.add(f'func ( lst1 ) with ({lst})')
	if lst.__len__() == 1:
		return lst[0]
	elif lst.__len__() == 0:
		return None
	return lst

def RngNoRepetition(v_min:int, v_max:int, how_many:int=1) -> list:
	'''
	if how_many is bigger or equal to v_max
	this function will return None
	'''
	# _log.add(f'func (rng_n_rep) with {v_min, v_max, how_many}')
	if how_many>=v_max:
		return None
	ret_list, tmp=[], [x+1 for x in range(v_min, v_max)]
	for _ in r(how_many):
		ret_list.append(tmp.pop(rint(v_min, len(tmp))))
	return ret_list

def UseFile(file:str, obj=None) -> object or None:
	"""pickled file btw"""
	# _log.add(f'func ( use_file ) with {file, mode, obj}')
	# if mode[-1] != 'b':
		# mode+='b'

	if obj == None:
		return _PickleLoad(open(file, 'rb'))
	else:
		_PickleDump(obj, open(file, 'wb'))

def json(file:str, obj:object=None) -> dict or None:
	# _log.add(f'func (js) with {file, obj}')
	if obj == None: return _JsonLoad(open(file))
	else:_JsonDump(obj, file)

def GetInt(msg:str, excepts = [], default = None) -> int:
	'''
	will return an integer by inputing a string with {msg, end}
	and converting it to int
	if the user enters an invalid input the function will restart
	'''
	# _log.add(f'func (get_int) with {msg, end}')
	x=input(f'{msg}')
	try:
		if x in excepts:
			return default
		y = int(x)
		return int(x)
	except ValueError:
		return GetInt(msg)

def GetFloat(msg:str, excepts = [], default = None) -> float:
	'''
	will return an float by inputing a string with {msg, end}
	and converting it to int
	if the user enters an invalid input the function will restart
	'''
	# _log.add(f'func (get_float) with {msg, end}')
	x=input(f'{msg}')
	try:
		if x in excepts:
			return default
		y = float(x)
		return float(x)
	except ValueError:
		return GetFloat(msg)

def IsPrime(ask:int) -> bool:
	# _log.add(f'func (is_prime) with ({ask})')
	msg = False
	if ask > 1:
		for i in r(ask, start=2):
			if (ask % i) == 0:
					msg = False
					break
		else:
			msg = True
	else:
		msg = False
	return msg

def case(var:int or float, index:int) -> str:
	return str(var)[index]

def fib(n:int) -> list:
	# _log.add(f'func (fib) with ({n})')
	result = []
	a, b = 0, 1
	while a < n:
		result.append(a)
		a, b = b, a+b
	return result

class rng:
	def new(this) -> int:
		# _log.add(f'class (rng) -> new prop')
		this.var = []
		for _ in range(this.size):
			this.var.append(rint(this.mn, this.mx))
		return this.var

	def get(this) -> int:
		# _log.add(f'class (rng) -> get prop')
		this.var = []
		for _ in range(this.size):
			this.var.append(rint(this.mn, this.mx))
		return this.var

	def __init__(this, mn, mx, size=1) -> object:
		# _log.add(f'class (rng) -> __init__ with {this, mn, mx, size}')
		this.size=size
		this.mn=mn
		this.mx=mx
		this.new

	def __repr__(this) -> str:
		# _log.add(f'class (rng) -> __repr__')
		if len((var:=this.var))==1:
			var=this.var[0]
		this.new
		return f'{var}'

	def NewSize(this, size) -> None:
		# _log.add(f'class (rng) -> new_size with ({size})')
		this.size=size
		this.new

	def NewMin(this, mn) -> None:
		# _log.add(f'class (rng) -> new_min with {this, mn}')
		this.mn=mn
	def NewMax(this, mx) -> None:
		# _log.add(f'class (rng) -> new_max with {this, mx}')
		this.mx=mx

	def __call__(this) -> int:
		return this.get()

def print(*msg, end='\n', sep=", ") -> None:
	# make msg
	# sep.join(...) então os argumentos são "juntados" com o sep
	# [str(m) for m in msg] para transformar todo valor em string
	msg = sep.join([str(m) for m in msg])

	# write msg
	# escrever a msg no terminal
	sout.write(f'{msg}{end}')

	# flush msg
	# escrever o conteúdo do terminal no cmd
	sout.flush()

def printl(*msg, sep=", ") -> None:
	# make msg
	msg = sep.join([str(m) for m in msg])

	# write msg
	sout.write(f'{msg}')

	# flush msg
	sout.flush()

def prints(*msg, sep=", ") -> None:
	# make msg
	msg = sep.join([str(m) for m in msg])

	# write msg
	sout.write(f'{msg}')

def input(*msg, joiner=", ", CallWhenEscape=nop) -> None:
	printl(*msg, sep = joiner)
	for line in sin:
		msg = line[:-1]
		break

	if '\x1b' in msg:
		NewMsg = CallWhenEscape(msg)
		if NewMsg != None:
			return NewMsg

	return msg

def index(ls:list, var, many=False) -> list:
	# _log.add(f'func (index) with {ls, var, many}')
	if var in ls:
		ret =[]
		for i in r(ls):
			if var == ls[i]:
					if many:
							ret.append(i)
					else:
							return [i]

	else:
		return None
	return ret

def GetCh() -> str:
	fd = sin.fileno()
	OldSettings = tcgetattr(fd)
	try:
		setraw(sin.fileno())
		ch = sin.read(1)
	finally:
		tcsetattr(fd, TCSADRAIN, OldSettings)
	return ch

def GCH(TEQ):
	ch = GetCh()
	if type(TEQ) == list:
		return ch in TEQ
	return ch == TEQ

#terminal colors -> None
#\/ \/ \/ \/

color: dict[str] = {
# WARNING! color:dict is no longer in development, use the COLOR class from now on (just under)
# formating: '{name}' : '\003[{mode};{ColorCode}m'
# modes: 0:normal 1:bold? 2:dark 3:italics 4:underline 5:blinking 7:bkground 8:hidden
	'':'',
	'nc':'\033[0m',
	'white':'\033[0;37m',
	'black' : '\033[0;30m',
	'red' : '\033[0;31m',
	'green' : '\033[0;32m',
	'yellow' : '\033[0;33m',
	'blue' : '\033[0;34m',
	'magenta' : '\033[0;35m',
	'cyan' : '\033[0;36m',

	'dark gray' : '\033[0;90m',
	'dark grey' : '\033[0;90m',
	'dark blue' : '\033[0;117m',

	'light gray' : '\033[0;37m',
	'light grey' : '\033[0;37m',
	'light red' : '\033[0;91m',
	'light green' : '\033[0;92m',
	'light yellow' : '\033[0;93m',
	'light blue' : '\033[0;94m',
	'light magenta' : '\033[0;95m',
	'light cyan' : '\033[0;96m',

	'br gray' : '\033[0;37m',
	'br grey' : '\033[0;37m',
	'br red' : '\033[0;91m',
	'br green' : '\033[0;92m',
	'br yellow' : '\033[0;93m',
	'br blue' : '\033[0;94m',
	'br magenta' : '\033[0;95m',
	'br cyan' : '\033[0;96m',

	'bk nc':'\033[7;0m',
	'bk white':'\033[7;37m',
	'bk black' : '\033[7;30m',
	'bk red' : '\033[7;31m',
	'bk green' : '\033[7;32m',
	'bk yellow' : '\033[7;33m',
	'bk blue' : '\033[7;34m',
	'bk magenta' : '\033[7;35m',
	'bk cyan' : '\033[7;36m',
	'bk gray' : '\033[7;90m',
	'bk grey' : '\033[7;90m',

	# for some reason these kinda don't work
	# 'bk light red' : '\033[7;91m',
	# 'bk light green' : '\033[7;92m', #it's darker light cyan!
	# 'bk light yellow' : '\033[7;93m',
	# 'bk light blue' : '\033[7;94m',
	# 'bk light magenta' : '\033[7;95m',
	# 'bk light cyan' : '\033[7;96m',
	# "bk nc" : "\033[0;49m",
	# "bk black" : "\033[0;40m",
	# "bk red" : "\033[0;41m",
	# "bk green" : "\033[0;42m",
	# "bk yellow" : "\033[0;43m",
	# "bk blue" : "\033[0;44m",
	# "bk magenta" : "\033[0;45m",
	# "bk cyan" : "\033[0;46m",
	# "bk light gray" : "\033[0;47m",
	# "bk white" : "\033[0;107m",
	# "bk dark gray" : "\033[0;100m",
	# "bk light red" : "\033[0;101m",
	# "bk light green" : "\033[0;102m",
	# "bk light yellow" : "\033[0;103m",
	# "bk light blue" : "\033[0;104m",
	# "bk light magenta" : "\033[0;105m",
	# "bk light cyan" : "\033[0;106m",
}

class COLOR:
	nc				=			"\033[0;00m"

	black			=			"\033[0;30m"
	red			=			"\033[0;31m"
	green			=			"\033[0;32m"
	magenta		=			"\033[0;35m"
	blue			=			"\033[0;36m"
	white			=			"\033[0;37m"
	GreenishCyan	=			"\033[0;96m" #kinda too complex ()
	orange			=			"\033[0;33m" #bruh
	#orange			=			"\033[0;91m" # bruh
	cyan			=			"\033[0;34m"

	DarkBlue		=			"\033[0;94m"

	BrOrange		=			"\033[0;93m"
	BrMagenta		=			"\033[0;95m"
	BrYellow		=			"\033[0;97m"
	BrGrey2		=			"\033[0;110m"

	DarkGrey		=			"\033[0;90m"
	DarkCyan		=			"\033[0;92m"
	BkDarkGrey		=			"\033[0;100m"

	Bkblack		=			"\033[0;40m"
	BkOrange		=			"\033[0;43m"
	BkOrange2		=			"\033[0;101m"
	BkRed			=			"\033[0;43m"
	BkGreen		=			"\033[0;42m"
	BkCyan			=			"\033[0;44m"
	BkMagenta		=			"\033[0;45m"
	BkCyan			=			"\033[0;46m"
	BkWhite		=			"\033[0;47m"
	BkCyan			=			"\033[0;102m"
	BkBlue			=			"\033[0;104m"
	BkCyan			=			"\033[0;106m"
	BkWhite		=			"\033[0;107m"

	BkBrOrange		=			"\033[0;103m"
	BkBrGrey		=			"\033[0;105m"

def SetColorMode(color:str, mode:str) -> str:
	index = color.find('[')+1
	color = list(color)
	color[index] = mode
	color = ''.join(color)
	return color

def PascalCase(string, remove=' ') -> str:
	if remove in string:
		string = string[0].upper()+string[1:]
		while (ps := string.find(remove)) != -1:
			string = string[:ps] + string[ps+1].upper() + string[ps+2:]
	return string

def attrs(thing:object) -> list[str]:
	return [attr for attr in dir(thing) if attr[0] != '_']

def SplitBracket(string:str, bracket:str, closing_bracket='', Rmdadd="") -> str:
	# _log.add(f'func (split_bracket) with {string, bracket, closing_bracket}')

	if closing_bracket == '':
		r = {
		'(' : ')',
		'[' : ']',
		'{' : '}',
		}
		closing_bracket = r[bracket]
	return closing_bracket.join(str(string).split( bracket )).split(closing_bracket)

def StrToMs(ipt:str) -> int:
	# _log.add(f'func (str_to_ms) with ({ipt})')
	ipt=ipt.split()
	n, ipt = float(ipt[0]), ipt[1]
	TypesToStr = {
	("years", "year", "yrs", "yr", "ys", 'y'):220903200000,
	("weeks", "week", "w"):604800000,
	("days", "day", 'd'):86400000,
	('hours', 'hour', 'hrs', 'hr', 'h'):3600000,
	('minutes', 'minute', 'mins', 'min', 'm'):60000,
	('seconds', 'second', 'secs', 'sec', 's'):1000,
	('milliseconds', 'millisecond', 'msecs', 'msec', 'ms'):1
	}
	for i in TypesToStr.keys():
		if ipt in i:
			return n*TypesToStr[i]
	return None

def bhask(a, b, c) -> tuple[int]:
	# _log.add(f'func ( bhask ) with {a, b, c}')
	delt = ((b**2) - (4*a*c))**.5
	b*=-1
	a*=2
	x = (b + delt)/a
	y = (b - delt)/a
	return x, y

def near(base:float or int, num:float or int, dif_up:float or int, dif_down:float or int=None) -> bool:
	# _log.add(f'func ( near ) with {base, num, dif_up, dif_down}')
	if dif_down == None:dif_down = dif_up
	return base+dif_up >= num >= base-dif_down

def rsymb(size=1) -> str:
	# _log.add(f'func ( rsymb ) with ({ size })')
	#33-47 58-64 160-191
	c=[]
	for _ in r(size):
		tp = rint(1, 3)
		if tp == 1:
			c.append(chr(rint(33, 47)))
		elif tp == 2:
			c.append(chr(rint(58, 64)))
		else:
			c.append(chr(rint(160, 191)))
	return lst1(c)

def rchar(size=1) -> str:
	# _log.add(f' func ( rchar ) with ({ size })')
	#65-90 97-122
	return lst1([(chr(rint(65, 90))) if rint(0, 1) else (chr(rint(97, 122))) for char in r(size)])

def GetWLen(msg:str, ln:int, end:str='\n') -> int:
	AssureType(int, ln, ErrorMsg=f"lengh type != int \n {ln} of type {type(ln)} != int")
	'''
	will return an str by inputing a string with {msg, end}
	if the user enters an invalid input the function will restart
	the valid input has the same size as ln
	snippet:
	len(input) == ln
		ret
	else
		restart
	'''
	# _log.add(f'func (get_w_len) with {msg, end}')
	x=input(f'{msg}{end}')
	if len(x) == ln:
		return x
	else:
		GetWLen(msg, ln, end)

# wtf?
def CallWExcept(func:FuncType, excpts:BaseException, *args:object, call:bool=False, call_f:bool=None) -> object:
	# _log.add(f'func ( call_w_except ) with {funct, excpts, *args, call, call_f }')
	x = func(*args)
	if x in excpts:
		if call:
			call_f()
		else:
			CallWExcept(func, excpts, *args)
	else:
		return x

def count(end:object, start:int=0, jmp:int=1) -> int:
	i=start
	if end == 0:
		while True:
			yield i
			i+=jmp
	else:
		while True:
			yield i
			i+=jmp
			if i >= end:break

def timeit(func:FuncType) -> FuncType:
	def wrapper(*args, **kwargs) -> int:
		timer = tm()
		func(args, **kwargs)
		return round(tm()-timer, 6)
	return wrapper

def mmc(a:int, b:int) -> int:
	if a-1<b or b<a+1:
		return a*b
	AssureType(int, a, ErrorMsg=f"a : {a} != int")
	AssureType(int, b, ErrorMsg=f"b : {b} != int")
	# _log.add(f'func ( mmc/lcm ) with {a, b}')
	greater = max(a, b)
	# s = tm()
	for i in count(0):
		G = greater+i
		if not G % a and not G % b:break
		# if tm()-s>len(f"{greater}")*2:
			# print(f"{color['red']}timed out{color['normal']}")
			# return None
			# rai/se Exception('timed out')
	return G

lcm = mmc

def factorial(n:int) -> int:
	# _log.add(f'func ( fact ) with {n}')
	Fact = 1
	for i in range(1, n+1):
		Fact*=i
	return Fact

def ArgvAssing(argvs:iter) -> dict:
	'''
	this function will loop through all argvs, and will define the ones starting with '-' as indicators
	and the others just normal arguments
	the returning value will be a dictionary like this:
	argv = ['-i', 'input', 'input2', '-o', 'output', 'output2']
	{'-i':['input', 'input2], '-o':['output', 'output2']}
	'''
	indcn=[]
	ret={}
	for i in r(argvs):
		if str(argvs[i])[0] == '-':
			indcn.append(i)

	if indcn == []:
		if argv == []:
			ret[None] = []
		else:
			ret[None] = argvs

	elif indcn[0] > 0:
		ret[None] = argvs[0:indcn[0]]

	for index in r(argvs):
		argvs[index] = argvs[index].replace("/-", '-')

	for i in r(indcn):
		try:
			dif = indcn[i+1]-indcn[i]
			add = argvs[indcn[i]:indcn[i]+dif][1:]
			# for AddIndex in r(add):
					# add[AddIndex] = add[AddIndex].replace("/-", '-')
			ret[argvs[indcn[i]:indcn[i]+dif][0]] = add#argvs[indcn[i]:indcn[i]+dif][1:]
		except IndexError:
			add = argvs[indcn[i]+1:]
			# for AddIndex in r(add):
					# add[AddIndex] = add[AddIndex].replace("/-", '-')
			ret[argvs[indcn[i]]] = add#argvs[indcn[i]+1:]
	return ret
argv_assing = ArgvAssing

def exit(num:int=1) -> None:
	# _log.add(f'class ( exit ) = ({num}) => act')
	AssureType(int, num, ErrorMsg=f'var {num} of wrong type, should be int')
	if num < 256:
		exi(num)
	else:
		raise NumberTooBigError("exit num : %d > 255" % num)

def between(x:float or int, min:float or int, max:float or int) -> bool:
	return min < x < max

def ls(dir='.') -> list:
	return [i if isfile(f'{dir}/{i}') else f"{i}/" for i in _ls(dir)]

def rstr(ln:int, chars:bool=True, symbs:bool=True, ints:bool=True, intmin:int=0, intmax:int=9) -> str:
	ret = []
	for _ in r(ln):
		fs = []
		if chars:fs.append(rchar)
		if symbs:fs.append(rsymb)
		if ints:fs.append(rint)
		f = ritem(fs)
		if f == rint:
			ret.append(f(intmin, intmax))
		else:
			ret.append(f())
	return ''.join([str(a) for a in ret])

def clear() -> None:
	ss("clear")

def ANDGroups(g1:set or list or frozenset, g2:set or list or frozenset) -> set or list or frozenset:
	G1 = set(g1)
	G2 = set(g2)
	Gall = *g1, *g2
	Gret = set()
	for i in Gall:
		if i in G1 and i in G2:
			Gret.add(i)
	return Gret

def ORGroups(g1:set or list or frozenset, g2:set or list or frozenset) -> set or list or frozenset:
	Gret = set((*g1, *g2))
	return Gret

def XORGroups(g1:[set, list, frozenset], g2:[set, list, frozenset])-> set or list or frozenset:
	G1 = set(g1)
	G2 = set(g2)
	Gall = *g1, *g2
	Gret = set()
	for i in Gall:
		if i in G1 + i in G2 == 1:
			Gret.add(i)
	return Gret

def NOTGroups(g1:[set, list, frozenset], g2:[set, list, frozenset])-> set or list or frozenset:
	G1 = set(g1)
	G2 = set(g2)
	Gret = set()
	for i in G1:
		if not i in G2:
			Gret.add(i)
	return Gret

class code:
	def __init__(this, *code, name="test", mode="exec") -> object:
		this.name, this.mode, this.code = name, mode, list(code)

	def __add__(this, line) -> object:
		this.code.append(line)
		return this

	def __call__(this) -> None:
		if type(this.code) == str:this.code=this.code.split('\n')
		for line in this.code:
			exec(compile(line, this.name, this.mode))
		return 0

	def __repr__(this) -> str:
		msg = ""
		if type(this.code) == str:
			this.code=this.code.split('\n')

		if len(this.code) > 1:
			for line in this.code:
					msg+=f"{line}\n"
		elif len(this.code) == 1:
			msg = f"{this.code[0]}"
		else:
			msg = ""
		return msg

class var(object):
	'''
	this class should NOT be used for items in iterables! (like lists)

	this class "contains" the other classes in it,
	so you can stop worring about doing this foo=DoShit(foo, args)
	and start doing this foo.DoShit(args)
	and facilitating your life when using dicts

	for i in {'a':1, 'b':2, 'c':3} =  ERROR
	for i in var({'a':1, 'b':2, 'c':3}) = dict.keys()

	"hello world"[3] = '!' = ERROR
	var("hello world")[3] = '!' = "hel!o world"

	[1, 2, 3]+[2, 3, 4] = ERROR
	var([1, 2, 3])+[2, 3, 4] = [1, 2, 3, 2, 3, 4]
	var([1, 2, 3])+var([2, 3, 4]) = [1, 2, 3, 2, 3, 4]
	'''

	# this is bad (like, not well made)
	# should i try this again?

	def __init__(this, Value:object, Type:type=None, PrintMutipleLines=True) -> object:
		if type(Value) == type and type(Type) != type:
			Value, Type = Type, Value

		if Type == None:Type=type(Value)

		this.Type = Type
		this.Value = Value
		# this.PrintMutipleLines=bo/ol(PrintMutipleLines)
		this.PrintMutipleLines=not not (PrintMutipleLines)

		Types = {
			(float, int):"IsNumber",
			(list, set, str):"IsIterable",
			(str, ):"IsString",
			(frozenset, ):"IsFrozenset",
			(dict, ):"IsDict"
		}

		for i in Types.keys():
			exec(f"this.{Types[i]} = {this.Type in i}")

	# math shit start

	def __add__(this, add) -> object:
		try:
			return this.Value.__add__(add)
		except Exception:pass
		# var + var
		ReturnVar = None
		if type(add) == var:add=add.Value

		# frozen set is frozen set!
		if this.IsFrozenSet:
			raise TypeError

		# var != dict
		if not this.IsDict:
			if this.IsIterable:
					ReturnVar = this.Type(ORGroups(this.Value, add))
			else:
					ReturnVar = this.Value+add

		# var = dict
		elif this.IsDict:
			ret = this.Value
			for i in add.keys():
					ret[i] = add[i]
		return ReturnVar

	def __sub__(this, add) -> object:
		# var - var
		ReturnVar, ReturnType = None, this.Type
		if type(add) == var:add=add.Value

		# var != dict
		if not this.IsDict:
			if this.IsIterable:
					ReturnVar = this.Type(NOTGroups(this.Value, add))
			else:
					ReturnVar = this.Value-add

		# var == dict
		else:
			ret = this.Value
			retK = ret.keys()
			if type(add) == dict:
					for i in add.keys():
							del ret[i]
			else:
					for i in add:
							del ret[i]
			ReturnVar = ret

		# return var obj of same type and (probably) different value
		return ReturnVar

	def __mul__(this, add) -> object:
		if type(add) == var:add=add.Value

		if this.IsNumber:
			return this.Value * add
		else:
			raise WrongType(f"var class can't multiply {this.Value} with {add}")

	def __truediv__(this, add) -> object:
		if type(add) == var:add=add.Value

		if this.IsNumber:
			return this.Value / add
		else:
			raise WrongType(f"var class can't divide {this.Value} with {add}")

	def __floordiv__(this, add) -> object:
		if type(add) == var:add=add.Value

		if this.IsNumber:
			return this.Value // add
		else:
			raise WrongType(f"var class can't (floor) divide {this.Value} with {add}")

	# math shit done
	# list/dict stuff start

	def __iter__(this) -> object:
		for i in this.Value:
			yield i

	# calling method
	def __getitem__(this, index_or_content) -> object:
		if type(index_or_content) == var:index_or_content = index_or_content.Value
		ret = this.Value[index_or_content]

		return ret

	# list/dict stuff done
	# (other) magic methods start

	def dict(this, lst:list) -> dict:
		return this.__dict__()

	def __dict__(this, lst:list) -> dict:
		return MakeDict(this.Value, lst)

	def __len__(this) -> int:
		if this.IsDict:
			return len(this.Value.Keys())
		return len(this.Value)

	def __setitem__(this, index, obj) -> None:
		if this.IsFrozenSet:
			raise TypeError(f"can't set value of FrozenSet\nvalue:{this.Value}")
		if this.IsString:
			ret = list(this.Value)
			ret[index] = obj
		else:
			ret = [this.Value]
			ret[index] = obj

		this.Value = ret

	def __repr__(this) -> str:
		msg = ''
		if this.IsIterable and not this.IsString:
			for thingIndex in r(this.Value):
					thing = this.Value[thingIndex].__repr__()
					# if type(thing).find("__main__.") != -1:
							# TypeMsg = f"{type(thing)}".split("__main__.")[1]
					# else:
					TypeMsg = f'{type(thing)}'.split('\'')[1]
					if this.PrintMutipleLines:
							msg += f"{thingIndex} : {TypeMsg} : {thing}\n"
					else:
							msg += f"{TypeMsg}: {thing}, "
			msg = msg[:-1]
		else:
			# if f"{type(this.Value)}".find("__main__.") != -1:
					# TypeMsg = f"{type(this.Value)}".split("__main__.")[1][:-2]
			# else:
			TypeMsg = f'{this.Type}'.split('\'')[1]
			if this.IsString:
					msg+=f"{TypeMsg} : {''.join(this.Value)}"
			else:
					msg += f"{TypeMsg} : {this.Value}"

		return msg

	# magic methods done
	# complex methods start

	def split(this, string:str=None) -> any:
		if type(string) == var:string = string.Value
		if string == None:
			ret = this.Value.split()
		else:
			ret = this.Value.split(string)
		return ret

	def join(this, string:str or var) -> str:
		if type(string) == var:string = string.Value
		ret = ""
		if this.IsIterable:
			for thing in this.Value:
					if type(thing) == var:
							ret+=f"{string}{thing.Value}"
					else:
							ret+=f"{string}{thing}"

			return ret[len(string):]
		else:
			raise TypeError(f"\n{var} is not iterable")

	def SplitBracket(this, bracket, ClosingBracket="default") -> list[str]:
		if type(bracket) == var:bracket = bracket.Value
		if type(ClosingBracket) == var:ClosingBracket = ClosingBracket.Value

		if ClosingBracket == "default":
			ret = SplitBracket(this.Value, bracket)
		else:
			ret = SplitBracket(this.Value, bracket, ClosingBracket)
		if type(ret)!=var:
			ret = ret
		return ret

	def keys(this) -> list:
		return list(this.Value.keys())

	def index(this, content:object) -> int:
		ret = None
		if this.IsIterable:
			ret = this.Value.index(content)
		elif this.IsDict:
			mkdict = {}
			for i in this.keys():
					mkdict[this[i]] = i
			ret = mkdict[content]

		else:
			raise TypeError(f"{this} is not iterable or dictionary")
		return ret

	def pop(this, index) -> any:
		if this.IsString:
			char = this.Value[index]
			if index == -1:
					this.Value = this.Value[:-1]
			else:
					this.Value = this.Value[index+1:]+this.Value[:index]
			return char
		else:
			return this.Value.pop(index)

	def remove(this, content) -> None:
		this.Value.remove(this)

	# that's not how u do it right?
	# def copy(this) -> :
		# return var(this.Value, PrintMutipleLines=this.PrintMutipleLines)

	def find(this, string:str) -> int:
		return this.Value.find(string)

	# complex methods done

class BDP:
	def __init__(this, name, IgnoreDataSize=False) -> object:
		# for unix like system
		# c:/users/{USER}/BDP
		this.IgnoreDataSize = IgnoreDataSize

		if OS == "linux": # gud os
			if not exists(f"/home/{USER}/BDP"):
					ss("mkdir /BDP/")

			if not name.startswith("~/BDP/"):
				name = f"~/BDP/{name}"

			if not name.endswith(".pog"):
					name += ".pog"

			name = name.replace("//", '/')
			name = name.replace('~', f"/home/{USER}")

		elif OS == "windows": # bad os
			if not exists(f"C:/users/{USER}/BDP/"):
					ss(f"mkdir C:/users/{USER}/BDP/")

			if not name.startswith(f"~/BDP/"):
					name = f"~/BDP/{name}"

			if not name.endswith(".pog"):
					name += ".pog"

						# / -> \ && ~ -> C:\...
			name = name.replace("/", '\\').replace('~', f"C:\\\\users\\{USER}")
		else:
			print(f"Your OS \"{OS}\" is not yet suported by util.BDP\n\
if you can help, please contribute at https://OwseiWasTaken/util.py")

		this.name = name
		this.data = None
		this.exists = exists(name)

	def save(this, data=None) -> str: # not that the string matters
		if data == None:
			data = this.data

		if not this.exists:
			with open(this.name, 'w'):pass
			#ss(f"touch {this.name}")#only for linux

		UseFile(this.name, data)
		return "saved"

	def load(this) -> any:
		if exists(this.name):
			try:
				this.data = UseFile(this.name)
				return this.data
			except EOFError:
				this.data = None
				return None
		else:
			return None

	def __repr__(this) -> str:
		if len(f"{this.data}") < 100 or this.IgnoreDataSize:
			return f"name: {this.name}\ndata: {this.data}"
		else:
			return f"name: {this.name}\n{COLOR.yellow}data too big to display\n\
BDP(IgnoreDataSize=True) to ignore size{color.nc}"

	def __call__(this, data=None) -> any: # this breaks occasionaly

		if data == None and this.data == None:
			return this.load()

		elif this.data == None:
			this.data = data

		this.save()
		return "saved"

def NumberToExponent(number:list[str]) -> str:
	smol = {'0':'⁰', '1':'¹', '2':'²', '3':'³', '4':'⁴', '5':'⁵', '6':'⁶', '7':'⁷', '8':'⁸', '9':'⁹', '.':'.'}

	return ''.join([smol[i] for i in str(number)])

def rbool(OneIn=2) -> int:
	return not rint(0, OneIn-1)

def rcase(word:str, chance=0.5) -> str:
	if chance == None:chance = 0.5
	chance *= 100
	wd = ''
	for case in word:
		if chance >= rint(0, 100):
			case = case.upper()
		else:
			case = case.lower()
		wd+=case
	return wd

def invert(var:list or tuple or str) -> list or tuple or str:
	return var[::-1]

def EncryptS(var, key:int or float) -> list[int]:
	return [ord(char)+key for char in var]
	# ret = []
	# for char in str(var):
		# ret.append(ord(char)+key)
	# return ret

def DecryptS(var:str, key:int or float) -> str:
	return "".join([f"{chr(char-key)}" for char in var])
	# ret = []
	# for char in var:
		# ret.append(f"{chr(char-key)}")
	# return "".join(ret)

def AdvEncryptS(var, key, deep) -> list[int]:
	if deep <= 0:
		deep=1
	elif deep == 1 or deep == 0:
		return EncryptS(var, key)
	else:
		return AdvEncryptS(var, key*deep, deep-1)

def AdvDecryptS(var, key, deep) -> str:
	if deep <= 0:
		deep=1
	elif deep == 1 :
		return DecryptS(var, key)
	else:
		return AdvDecryptS(var, key*deep, deep-1)

def PosOrNeg(num:int) -> int:
	try:
		return 1//num*2+1
	except ZeroDivisionError:
		return 0

def odd(var:int) -> bool:
	return var%2

def numbers(times, nums=0) -> int:
	return eval(f'[{nums}'+f", {nums}"*(times-1)+']')

def ShowTextGif(sprites, SleepTime=0.35, times=-1) -> None:
#if times is negative the loop won't stop || if times = 0, it will be len(sprites)
	if times == 0:
		times = len(sprites)
	if times < 0:
		while True:
			for sprite in sprites:
					clear()
					sout.write(sprite)
					sleep(SleepTime)
	else:
		for tick in r(times):
			for sprite in sprites:
					clear()
					sout.write(sprite)
					sleep(SleepTime)

def JustDecimal(number:float) -> float:
	return number-int(number)

def NoDecimal(number:float) -> int:
	return int(number)

def number(num:str)->int or float or None:
	if num.isnumeric():
		return eval(num)

def TimesInNumber(TimesIn, NumberTo) -> bool:
	return not not (sum([rbool(TimesIn) for x in r(NumberTo)]))
	# return bo/ol(sum([rbool(TimesIn) for x in r(NumberTo)]))

def NumSum(numbers:int or float) -> int:
	numbers = str(numbers).replace('.', "")
	numbers = sum([int(num) for num in numbers])
	if len(str(numbers)) != 1:
		return NumSum(numbers)
	else:
		return numbers

def FindAll(StringToSearchIn:str, StringToFind:str) -> list[str]:
	# get replacable string
	StringToFindL = len(StringToFind)
	NotStringToFind = '0'*StringToFindL
	if NotStringToFind == StringToFind:
		NotStringToFind = '1'*StringToFindL
	# StringToFind can't be 000... and 111... at the same time!

	WLen = len(StringToFind)
	TLen = len(StringToSearchIn)
	TLenSmall = len(StringToSearchIn.replace(StringToFind, ""))
	times = (TLen-TLenSmall)/WLen

	ret = []
	for i in r(times):
		ret.append(StringToSearchIn.find(StringToFind))
		StringToSearchIn = StringToSearchIn.replace(StringToFind, NotStringToFind, 1)
	return ret

def CountSubstring(string, substring):
	SStrLen = len(substring)
	SLen = len(string)
	SSLen = len(string.replace(substring, ""))
	return int((SLen-SSLen)/SStrLen)

def DeepSum(args, ParseStringWith=eval, ParseString=False, ReturnDeeph=False) -> int:
	"""
	this function will add everything in the iterable in {args}, even strings!
	this function will return deeph of the iterable in {ReturnDeeph} is True (will calculate deeph any way tho)
	this ReturnDeeph var adds one for every item but iterables (but will count the deeph in side the iterables!)
	"""
	ret = 0
	deeph = 0
	for thing in args:
		deeph+=1
		if type(thing) in (float, int):
			# add number
			ret+=thing
		elif type(thing) == str:
			if ParseString:
					# parse and add string
					ret+=ParseStringWith(thing)
			else:
					# breaks because found string
					raise TypeError("\n%sERROR IN \"DeepSum\" function%s\n\
value %s is of type string (and ParseString = False)" %  (color['br red'], color["nc"], repr(thing)))
		else:
			# recourciveness (it that a word?)
			deeph-=1
			RetA, DeephA=DeepSum(thing, ParseString=ParseString, ParseStringWith=ParseStringWith, ReturnDeeph=True)
			# adds the nums and deeph of recourcive run
			ret += RetA
			deeph += DeephA

	if ReturnDeeph:
		return ret, deeph
	else:
		return ret
	# DUDE DOING THIS MADE ME WANT TO KILL SOMEONE

def average(args, ParseDeepSumString=False, SumFunc=DeepSum) -> int:
	if SumFunc == DeepSum:
		sum, deeph = SumFunc(args, ParseString=ParseDeepSumString, ReturnDeeph=True)
	else:
		sum, deeph = SumFunc(args)
	return sum/deeph

def mid(msg, LenToBe, CanDeleteEnd=True, AddFront=' ', AddAfter=' ', DoToFront="not front") -> str:
	iterate = LenToBe - len(msg)
	if iterate < 0:
		if type(msg) in [float, int]:
			return round(msg, iterate)
		return msg[:iterate]

	front = 1
	while iterate > 0:
		front = eval(DoToFront)
		iterate -= 1
		if front:
			msg = AddFront+msg
		else:
			msg+= AddAfter
	return msg

def IsIterable(obj:object) -> bool:
	return type(obj) in iterables

def SingleList(args:list[...]) -> list[float or int or str or object]:
	ret = []
	for thing in args:
		if IsIterable(thing):
			# recourciveness (it that a word?)
			RetA = SingleList(thing)
			# set ret as *ret and *RetA
			ret = [*ret, *RetA]
		else:
			ret.append(thing)
	return ret

def BiggestLen(lst:list[any]) -> int: #biggest by len
	return max([len(str(thing)) for thing in lst])

def compare(*times:list[int]) -> str:
	times = SingleList(times)

	avg = average(times)
	ret = f"average : {avg:.3f}\n"

	# getting biggest num (len)
	sep = BiggestLen(times)
	# sep = max([len(str(time)) for time in times])

	for time in times:
		ThisColor = color["red"] if time-avg > 0 else color["green"]

		PoM = ('' if (time-avg) < 0 else '+') + str(round(time-avg, sep-1))

		prt = f"{times.index(time)} : {color['magenta']}{' '*(sep-len(str(time)))}{time}{color['nc']} | {ThisColor}{PoM}"

		ret+=prt+color["nc"]+"\n"
	return ret

def graphics(*ints, UnderAvg = color["red"], OverAvg = color["green"]) -> str:
	ints = SingleList(ints)

	avg = average(ints)

	manys = [round(ins/avg, 6) for ins in ints]
	ManysGraph = []

	t={
		6 : "⠿",
		5 : "⠟",
		4 : "⠏",
		3 : "⠇",
		2 : "⠃",
		1 : "⠄",
		0 : " "
	}
	for ManyIndex in r(manys):
		many = manys[ManyIndex]
		scale = round(many/(1/6))# one for each braille ball
		fulls = scale//6
		l = f"{ManyIndex} : "

		if scale > avg:
			l+=OverAvg
		else:
			l+=UnderAvg

		l+=t[6]*fulls
		l+=t[scale%6]
		l+=color["nc"]
		ManysGraph.append(l)

	return ManysGraph

# def CharConverter(Chars:list[str]) -> str:
#	ch = Chars.pop(0)

#	# return None in in esc seq
#	if ch == '\x1b':return None
#	elif ch == '[' and Chars[0] == '\x1b':return None

#	Chars = ''.join(Chars)
#	if Chars == '\x1b[':
#		ch = {
#			'A':"UP",
#			'B':"DOWN",
#			'C':"RIGHT",
#			'D':"LEFT",
#		}.get(ch)
#	elif Chars == '\x1b[1;5':
#		ch = {
#			'A':"CTRL UP",
#			'B':"CTRL DOWN",
#			'C':"CTRL RIGHT",
#			'D':"CTRL LEFT",
#		}.get(ch)
#	elif Chars == '\x1b[1;2':
#		ch = {
#			'A':"SHIFT UP",
#			'B':"SHIFT DOWN",
#			'C':"SHIFT RIGHT",
#			'D':"SHIFT LEFT",
#		}.get(ch)
#	return ch

def pos(y:int, x:int) -> str:
	return "\x1B[%i;%iH" % (y+1, x+1)

def ppos(y, x):
	sout.write("\x1B[%i;%iH" % (y+1, x+1))
	sout.flush()

def ClearLine(y, GetTerminalY="default", char=' ', start=color["nc"], end=color["nc"]) -> None:
	if GetTerminalY == "default":
		x, _ = GetTerminalSize()
	sout.write("%s%s%s%s%s" % (start, pos(y, 0), char*x, pos(y, 0), end))
	sout.flush()

def ClearCollum(x, GetTerminalX="default", char=' ', start=color["nc"], end=color["nc"]) -> None:
	if GetTerminalX == "default":
		_, y = GetTerminalSize()
	for i in r(y):
		sout.write("%s" % (start + pos(i, x) + char + end ))
	sout.flush()

def DrawHLine(x, XTo, y, colo, char = ' ') -> None:
	ps = pos(y, x)
	_x, _y = GetTerminalSize()
	len = (XTo-x)+1
	sout.write(ps + colo + char * len + color["nc"] + char*(_x-len))  # if optmizing change XTO -> msg lenght
	sout.flush()

def DrawVLine(y, YTO, x, colo, char = ' ') -> None:
	for i in range(0, YTO+1)[y:]:
		sout.write("%s" % pos(i, x) + colo + char + color["nc"])
	sout.flush()

def HideCursor() -> None:
	sout.write("\x1b[?25l")
	sout.flush()

def ShowCursor() -> None:
	sout.write("\x1b[?25h")
	sout.flush()

def DrawRectangle(UpLeft, DownRight, BkColor, DoubleWidthVerticalLine=False) -> None:
	x1, y1 = UpLeft
	x2, y2 = DownRight
	# |x1, -y1
	#
	#	|x2, -y2

	# DrawVLine(y, YTO, x, colo)
	DrawVLine(y1, y2, x1, BkColor)
	DrawVLine(y1, y2, x2, BkColor)
	if DoubleWidthVerticalLine:
		DrawVLine(y1, y2, x1+1, BkColor)
		DrawVLine(y1, y2, x2-1, BkColor)

	# DrawHLine(x, XTo, y, colo)
	DrawHLine(x1, x2, y1, BkColor)
	DrawHLine(x1, x2, y2, BkColor)

#can also be used as RemoveStringByIndex if result:str = ''
def ReplaceStringByIndex(string:str, index:int, result:str) -> str:
	return string[:index] + result + string[index+1:]

class TextBox:

	def __init__(this, StartString="", DrawRect=True, DoClear=True) -> object:
		this.DrawRect = DrawRect
		this.DoClear = DoClear
		this.PrintableChars = " óíáàéç!\"#$%&'()*+, -./0123456789:;<=>\
?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_´`abcdefghijklmnopqrstuvwxyz{|}~"
		this.HSize, this.VSize = GetTerminalSize()
		this.TextSixe = this.HSize-2
		this.STRING = StartString
		this.CURSOR = len(this.STRING)-1
		this.STRING += " "*(this.TextSixe - len(this.STRING))

	def __call__(this):
		return this.loop()

	def IsPrintableChar(this, char) -> bool:
		return char in this.PrintableChars

	def SetChar(this, char) -> None:
		if char == "\x1b": # espace key
			if GetCh() == '[': # escape code
				ch = GetCh()

				if ch == 'C' and this.CURSOR < len(this.STRING)-2: # go right
					this.CURSOR+=1
				elif ch == 'D' and this.CURSOR > -1: # go left
					this.CURSOR-=1

				elif ch == '3': # may be del
					ch = GetCh()
					if ch == '~': # delete key
						this.STRING = list(this.STRING)
						this.STRING.pop(this.CURSOR+1)
						this.STRING = ''.join(this.STRING)+ ' '

				# elif ch == '2': # may be insert
					# ch = GetCh()
					# if ch == '~': # insert key
						# pass

		elif char == '\x7f' and this.CURSOR > -1: # backspace
			if (not this.CURSOR == len(this.STRING)-2 or not this.IsOverChar): # "normal" delete
				this.STRING = list(this.STRING)
				this.STRING.pop(this.CURSOR)
				this.STRING = ''.join(this.STRING)+' '
				this.CURSOR-=1
			else: # if @ $ of line del not backspace
				this.STRING = list(this.STRING)
				this.STRING[this.CURSOR+1] = ' '
				this.STRING = ''.join(this.STRING)

		else:
			if this.IsPrintableChar(char):
				if this.CURSOR < len(this.STRING)-2: # if char is going to be added move cursor right
					this.CURSOR+=1
				if this.CURSOR >= len(this.STRING): # if cursor if off screen get it back
					this.CURSOR-=1

				# strg = this.STRING.strip()
				# if len(strg)-1 <= this.CURSOR:
					# strg = this.STRING[:this.CURSOR]
				# ClearLine(1)
				# sout.write(f"{pos(1, 1)}{repr(strg)}{len(strg)-1 == this.CURSOR}|{len(strg)}|{this.CURSOR}")
				# if not len(strg)-1 == this.CURSOR: # place not replace

				if this.STRING[-1] == ' ': # move string right to add char to CURSOR's spot
					this.STRING = list(this.STRING)[:-1]
					this.STRING.insert(this.CURSOR, char)
					this.STRING = ''.join(this.STRING)
				else:
					this.STRING = ReplaceStringByIndex(this.STRING, this.CURSOR, char) # create or replace
	@property
	def IsOverChar(this) -> bool:
		return this.STRING[this.CURSOR+1] != ' '

	def loop(this) -> str:
		ShowCursor()
		if this.DoClear:
			clear()
		if this.DrawRect:
			DrawRectangle((0, this.VSize-3), (this.HSize-1, this.VSize), BkColor=color['bk grey'])
		char=''

		# chars = []

		while True:
			# sout.write(pos(this.VSize-1, this.HSize))

			# chars.append(repr(char))

			if char == '\r': # <Enter> to send
				return this.STRING.strip()

			this.SetChar(char)

			# sout.write(f"{pos(1, 1)}{chars}") # debug line
			# ClearLine(4)
			# sout.write(f"{pos(4, 4)} \
# {this.CURSOR == len(this.STRING)-2} { this.IsOverChar}|\
# {this.CURSOR == len(this.STRING)-2 or this.IsOverChar}|\
# {not (not this.CURSOR == len(this.STRING)-2 or not this.IsOverChar)}")

			if this.DrawRect:
				sout.write(f"{pos(this.VSize-2, 1)}{color['nc']}{this.STRING}")
				sout.write(pos(this.VSize-2, this.CURSOR+2))
			else:
				sout.write(f"{pos(this.VSize-1, 1)}{color['nc']}{this.STRING}")
				sout.write(pos(this.VSize-1, this.CURSOR+2))

			sout.flush()

			char = GetCh()

# class AdvTextBox:

#	def __init__(this, YLINE, XLINE, StartString="", DrawRect=True, DoClear=True) -> object:
#		this.YLINE = YLINE
#		this.XLINE = XLINE
#		this.DrawRect = DrawRect
#		this.DoClear = DoClear
#		this.PrintableChars = " áàéç!\"#$%&'()*+, -./0123456789:;<\
# =>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_´`abcdefghijklmnopqrstuvwxyz{|}~"
#		this.HSize, this.VSize = GetTerminalSize()
#		this.TextSixe = this.XLINE-2
#		this.STRING = StartString
#		this.CURSOR = -1
#		this.STRING += " "*(this.TextSixe - len(this.STRING))

#	def IsPrintableChar(this, char) -> bool:
#		return char in this.PrintableChars

#	def SetChar(this, char) -> None:
#		if char == "\x1b": # espace key
#			if GetCh() == '[': # escape code
#				ch = GetCh()

#				if ch == 'C' and this.CURSOR < len(this.STRING)-2: # go right
#					this.CURSOR+=1
#				elif ch == 'D' and this.CURSOR > -1: # go left
#					this.CURSOR-=1

#				elif ch == '3': # may be del
#					ch = GetCh()
#					if ch == '~': # delete key
#						this.STRING = list(this.STRING)
#						this.STRING.pop(this.CURSOR+1)
#						this.STRING = ''.join(this.STRING)+ ' '

#				# elif ch == '2': # may be insert
#					# ch = GetCh()
#					# if ch == '~': # insert key
#						# pass

#		elif char == '\x7f' and this.CURSOR > -1: # backspace
#			if (not this.CURSOR == len(this.STRING)-2 or not this.IsOverChar): # "normal" delete
#				this.STRING = list(this.STRING)
#				this.STRING.pop(this.CURSOR)
#				this.STRING = ''.join(this.STRING)+' '
#				this.CURSOR-=1
#			else: # if @ $ of line del not backspace
#				this.STRING = list(this.STRING)
#				this.STRING[this.CURSOR+1] = ' '
#				this.STRING = ''.join(this.STRING)

#		else:
#			if this.IsPrintableChar(char):
#				if this.CURSOR < len(this.STRING)-2: # if char is going to be added move cursor right
#					this.CURSOR+=1
#				if this.CURSOR >= len(this.STRING): # if cursor if off screen get it back
#					this.CURSOR-=1

#				# strg = this.STRING.strip()
#				# if len(strg)-1 <= this.CURSOR:
#					# strg = this.STRING[:this.CURSOR]
#				# ClearLine(1)
#				# sout.write(f"{pos(1, 1)}{repr(strg)}{len(strg)-1 == this.CURSOR}|{len(strg)}|{this.CURSOR}")
#				# if not len(strg)-1 == this.CURSOR: # place not replace

#				if this.IsOverChar: # move string right to add char to CURSOR's spot
#					this.STRING = list(this.STRING)[:-1]
#					this.STRING.insert(this.CURSOR, char)
#					this.STRING = ''.join(this.STRING)
#				else:
#					this.STRING = ReplaceStringByIndex(this.STRING, this.CURSOR, char) # create or replace
#	@property
#	def IsOverChar(this) -> bool:
#		return this.STRING[this.CURSOR+1] != ' '

#	def loop(this) -> str:
#		ShowCursor()
#		if this.DoClear:
#			clear()
#		if this.DrawRect:
#			DrawRectangle((0, this.YLINE-1), (this.XLINE-1, this.YLINE+1), BkColor=color['bk grey'])
#		char=''

#		# chars = []

#		while True:
#			# sout.write(pos(this.VSize-1, this.HSize))

#			# chars.append(repr(char))

#			if char == '\r': # <Enter> to send
#				return this.STRING.strip()

#			this.SetChar(char)

#			# sout.write(f"{pos(1, 1)}{chars}") # debug line
#			# ClearLine(4)
#			# sout.write(f"{pos(4, 4)} \
# # {this.CURSOR == len(this.STRING)-2} { this.IsOverChar}|\
# # {this.CURSOR == len(this.STRING)-2 or this.IsOverChar}|\
# # {not (not this.CURSOR == len(this.STRING)-2 or not this.IsOverChar)}")

#			# if this.DrawRect:
#				# sout.write(f"{pos(this.VSize-2, 1)}{color['nc']}{this.STRING}")
#				# sout.write(pos(this.VSize-2, this.CURSOR+2)) # cursor
#			# else:
#				# sout.write(f"{pos(this.VSize-1, 1)}{color['nc']}{this.STRING}")
#				# sout.write(pos(this.VSize-1, this.CURSOR+2)) # cursor
#			sout.write(f"{pos(this.YLINE, 1)}{color['nc']}{this.STRING}{pos(this.YLINE, this.CURSOR+2)}")
#			# content + cursor

#			sout.flush()

#			char = GetCh()

def GetPrimeFactors(number:int) -> list[int]:
	factor = 2
	ret = []
	while factor <= number:
		if not number % factor:
			ret.append(factor)
			number /= factor
			factor += 1
		else:
			factor+=1
	return ret

class FancyIOStream:
	def __lshift__(this, msg:str) -> object:
		sout.write(msg)

		if '\n' in msg:
			sout.flush()
		return this

ARGV = ArgvAssing(argv[1:])

class get:
	def __init__(this, *gets, argvs=None, default = None) -> object:
		for index in r(gets):
			if type(gets[index]) != NoneType and gets[index][0] != '-':
				gets[index] = '-'+gets[index]
		global ARGV
		if argvs == None:
			argvs = ARGV
		this.argvs = argvs
		this.gets = gets

		stuff = this._get()
		this.list = stuff[0]
		this.first = default
		this.last = default
		if not this.list == None and len(this.list):
			this.first = this.list[0]
			this.last = this.list[-1]
		this.bool = stuff[1]
		this.exists = stuff[2]

	def _get(this) -> list:
		ret = []
		other = []
		this.argvs

		for indicator in SingleList(this.gets): # list

			other = [*other, *this.argvs.get(indicator, [])]
		if other:
			ret.append(other)
		else:
			ret.append([])

		if other: # MakeBool
			if other[0].isnumeric():
				# ret.append( bo/ol(eval(other[0])) )
				ret.append( not not (eval(other[0])) )
			else:
				# ret.append( bo/ol(other[0]) )
				ret.append( not not (other[0]) )
		else:
			ret.append(False)

		ret.append( any( [x for x in this.gets if x in this.argvs.keys()]) ) # exists

		return ret

def _RmDirLinux(dir:str) -> int:
	return ss(f"rm -rf {dir}")

def _RmDirWindows(dir:str) -> int: # not sure if works
	for file in ls(dir):
		if file.endswith('/'):
			_RmDirWindows(file)
		else:
			ss("del file")
	else:
		_rmdir(dir)

	return 0

def RmDir(dir:str) -> None:
	if OS == "linux":
		_RmDirLinux(dir)
	elif OS == "windows":
		_RmDirWindows(dir)
	else:
		print(f"Your OS {OS} is not yet suported by util.RmDir\n\
if you can help, please contribute at https://OwseiWasTaken/util.py")

def TrimSpaces(string:str) -> str:
	while '  ' in string:
		string = string.replace('  ', ' ')
	return string

def Hamiltons(benefit, probability, cost) -> bool:
	return benefit*probability/cost>0

def ReplaceAll(StringList:list[str], FromString:str, ToString:str) -> list[str]:
	if type(StringList) in [list, set, tuple]:
		for index in r(StringList):
			if type(StringList[index]) == str:
				StringList[index] = StringList[index].replace(FromString, ToString)
			elif type(String[index]) in [list, set, tuple]:
				StringList[index] = ReplaceAll(StringList[index], FromString, ToString)
	return StringList

def MakeString(line, char='"', leader="\\"):
	pos = 0
	string = []
	current = ""
	NotCurrent = ""
	ret = []
	InString = False
	line += ' '
	while pos < len(line):
		letter = line[pos]
		if InString:
			if letter == char and line[pos-1] != leader:
				InString = False
				ret.append(char+current+char)
				current = ""
			else:
				if letter != leader:
					current += letter
		else:
			if len(line) == pos+1:
				# print(line, pos, len(line))
				ret.append(NotCurrent.strip())
			elif line[pos] == char and line[pos-1] != leader:
				InString = True
				ret.append(NotCurrent.strip())
				NotCurrent = ""
			else:
				NotCurrent += letter
		pos+=1
	nret = []
	for rt in ret:
		if rt:
			nret.append(rt)
	return nret

def IsListSorted(lst:list, reverse:bool = False):
	return lst == sorted(lst, reverse = reverse)

if __name__=="__main__":
	for i in get('-c').list:
		print(eval(i))

# funcs/classes
"""
const USER
const FuncType
const NoneType
const iterables
class NumberTooBigError
const infinity
funct nop
class nocpass
const ARGV
class time
const time
class log
funct r
funct AssureType
class timer
funct MakeDict
funct sleep
funct pc
funct even
funct odd
funct lst1
funct RngNoRepetition
funct UseFile
funct json
funct GetInt
funct GetFloat
funct IsPrime
funct case
funct fib
class rng
funct print
funct printl
funct prints
funct input
funct index
funct GetCh
funct GCH
class COLOR
funct SetColorMode
funct PascalCase
funct attrs
funct SplitBracket
funct StrToMs
funct bhask
funct near
funct rsymb
funct rchar
funct GetWLen
funct CallWExcept
funct count
funct timeit
funct mmc
const lcm
funct factorial
funct ArgvAssing
const argv_assing
funct exit
funct between
funct ls
funct rstr
funct clear
funct ANDGroups
funct ORGroups
funct XORGroups
funct NOTGroups
class code
class var
class BDP
funct NumberToExponent
funct rbool
funct rcase
funct invert
funct EncryptS
funct DecryptS
funct AdvEncryptS
funct AdvDecryptS
funct PosOrNeg
funct odd
funct numbers
funct ShowTextGif
funct JustDecimal
funct NoDecimal
funct number
funct TimesInNumber
funct NumSum
funct FindAll
funct CountSubstring
funct DeepSum
funct average
funct mid
funct IsIterable
funct SingleList
funct BiggestLen
funct compare
funct graphics
funct pos
funct ppos
funct ClearLine
funct ClearCollum
funct DrawHLine
funct DrawVLine
funct HideCursor
funct ShowCursor
funct DrawRectangle
funct ReplaceStringByIndex
class TextBox
funct GetPrimeFactors
class FancyIOStream
const ARGV
class get
funct RmDir
funct TrimSpaces
funct Hamiltons
funct ReplaceAll
funct MakeString
funct IsListSorted
"""