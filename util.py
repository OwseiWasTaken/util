#! /usr/bin/python3.10
# TODO:
#	test pos (and other cursor) funcs in windows
#	sshkeyboard?, it's slow, but VERY easy to work with

# (IMPORTS

from time import strftime as __ftime__
from json import dump as _JsonDump, load as _JsonLoad
from pickle import dump as _PickleDump, load as _PickleLoad
from os import listdir as _ls, getlogin as _getlogin, rmdir as _rmdir


from functools import cache
from time import time as tm, sleep as slp
from os.path import isfile, exists, abspath
from typing import Callable, Any, Optional, Iterator, Iterable
from random import randint as rint, choice as ritem
from os import (
	getcwd as pwd,
	system as ss,
	chdir as cd,
	getenv,
	get_terminal_size as GetTerminalSize,
)

from sys import (
	argv,
	exit as exi,
	getsizeof as sizeof,
	stdout as sout,
	stdin as sin,
	stderr as eout,
	platform as OS,
)

from sys import stdout, stdin, stderr
from dataclasses import dataclass
from enum import IntEnum, Enum, auto as iota  # (1, 2, 3, ...), fafo, go's iota

from re import compile as comreg

# )IMPORTS
# (LINKS
# __ class methods https://www.tutorialsteacher.com/python/magic-methods-in-python
# https://regex101.com/
# )LINKS

# (LICENSE
# this is a general python lib that aims to make fast (fast as in "python fast")
# usefull functions, classes and constants, such as IsBitSet, get class, USER
# const and other things
# 2022, by Pedro "owsei" Romero Manse
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not get it here https://www.gnu.org/licenses/gpl-3.0.en.html
# )LICENSE

# (STUFF
# OS especific func
if OS in ["linux", "darwin"]:
	try:
		import gi

		gi.require_version("Notify", "0.7")
		from gi.repository import Notify

		def notify(title="", body=""):
			Notify.init("util.py/func/notify/init")
			Notify.Notification.new(str(title), str(body)).show()

	except ModuleNotFoundError:

		def notify(title="", body=""):
			print(f"the gi and notify modules where not found")

	from tty import setraw
	from termios import tcgetattr, tcsetattr, TCSADRAIN, TIOCGWINSZ
	from fcntl import ioctl
	sfo = sin.fileno() # get fd
	OldSettings = tcgetattr(sfo) # get fd state

	def GetCh(charlen = 1) -> str:
		try:
			setraw(sfo)
			ch = sin.read(charlen)
		finally:
			tcsetattr(sfo, TCSADRAIN, OldSettings)
		return ch

	def ClearLine(y):
		stdout.write(pos(y, 0) + "\x1b[K")

	def rClearLine(y):
		stdout.write("\n\x1b[F")
		if y:
			stdout.write(frpos(abs(y), ("A" if y < 0 else "B")) + "\x1b[K")
		else:
			stdout.write("\x1b[K")

	def clear():
		stdout.write("\x1b[0H")


else:  # (prolly) windows
	import msvcrt

	def notify(title="", body=""):
		stdout.write(
			f"""notify function not yet implemented in util.py for {OS}
if you want to help, make your commit at https://github.com/OwseiWasTaken/uti.py"""
		)

	sfo = None
	def GetCh() -> str:
		char = msvcrt.getch()
		while msvcrt.kbhit():
			char += msvcrt.getch()
		return char

	def ClearLine(y):
		stderr.write(
			f"""ClearLine function not yet implemented in util.py for {OS}
if you want to help, make your commit at https://github.com/OwseiWasTaken/uti.py"""
		)

	def rClearLine(y):
		eprint(
			f"""rClearLine function not yet implemented in util.py for {OS}
if you want to help, make your commit at https://github.com/OwseiWasTaken/uti.py"""
		)

	def clear():
		ss("cls")


class __time:
	@property
	def sec(this) -> str:
		return __ftime__(f"%S")

	@property
	def min(this) -> str:
		return __ftime__(f"%M")

	@property
	def hour(this) -> str:
		return __ftime__("%H")

	@property
	def day(this) -> str:
		return __ftime__("%D").split("/")[1]

	@property
	def month(this) -> str:
		return __ftime__("%D").split("/")[0]

	@property
	def year(this) -> str:
		return __ftime__("%D").split("/")[2]


time = __time()


class log:
	def __init__(this, sep=", ", tm=True, autosave=False):
		this.autosave: bool = autosave
		this.tm: bool = tm
		this.sep: str = sep
		this.LOG: list[str] = []

	def clear(this):
		this.LOG = []

	def add(this, *ask):
		ask = this.sep.join([str(ak) for ak in ask])
		tme = ""
		if this.tm:
			tme = f"at {time.day} {time.hour}:{time.min}:{time.sec} : "

		this.LOG.append(f"{ask}")
		if this.autosave:
			this.save()

	def PopByIndex(this, index: int):
		return this.LOG.pop(index)

	def PopByContent(this, content: str):
		return this.LOG.pop(this.LOG.index(content))

	def __repr__(this) -> str:
		return f"{this.LOG}"

	def get(this, num: int) -> str:
		return this.LOG[num]

	def __getitem__(this, num: int) -> str:
		return this.LOG[num]

	def __call__(this, *ask):
		this.add(*ask)	# defined in __init__

	def __add__(this, *ask):
		this.add(*ask)
		return this

	def __iter__(this):
		for i in this.LOG:
			yield i

	def show(this):
		for i in this:
			print(i)


def r(end, start: int = 0, jmp: int = 1):
	try:
		end = len(end)
	except TypeError:
		end = int(end)

	index = start
	while end > index:
		yield index
		index += jmp


class timer:
	def __init__(this, auto: bool = True):
		this.markers: list[float] = []
		if auto:
			this.st = tm()

	def start(this):
		this.st = tm()

	def mark(this):
		this.markers.append(this.get())

	def marks(this) -> list[float]:
		return this.markers

	def get(this) -> float:
		return tm() - this.st

	def __call__(this) -> float:
		if not this.st:
			this.st = tm()
			return 0.0
		else:
			return this.get()

	def __iter__(this):
		for i in this.markers:
			yield i

	def __repr__(this) -> str:
		return f"{this.get}"


def MakeDict(ls1: list | tuple, ls2: list | tuple) -> dict:
	ls1 = list(ls1)
	ls2 = list(ls2)
	ret = {x: y for x, y in zip(list(ls1), list(ls2))}
	return ret


def sleep(
	seg: float = 0,
	sec: float = 0,
	ms: float = 0,
	min: float = 0,
	hour: float = 0,
	day: float = 0,
	IgnoreKBI=True,
):
	if IgnoreKBI:
		try:
			slp(ms / 1000 + seg + sec + min * 60 + hour * 3600 + day * 86400)
		except KeyboardInterrupt:
			exit(0)
	else:
		slp(ms / 1000 + seg + sec + min * 60 + hour * 3600 + day * 86400)


def pc(x: int, y: int) -> float:
	return int(x / 100 * y)


def even(var: int) -> bool:
	return not var % 2


def odd(var: int) -> bool:
	return not not var % 2


def lst1(lst: list | tuple):
	if len(lst) == 1:
		return lst[0]
	elif not len(lst):
		return None
	else:
		return lst


def RngNoRepetition(min: int, max: int, HowMany: int = 1) -> list:
	ret = []
	all = [x + 1 for x in r(min, max)]
	if len(all) <= HowMany:
		return all
	else:
		for i in r(HowMany):
			ret.append(all.pop(rint(min, max - i)))
		return ret


def UseFile(file: str, obj=None):
	if obj == None:
		return _PickleLoad(open(file, "rb"))
	else:
		_PickleDump(obj, open(file, "wb"))
		return None


def json(file: str, obj: object = None) -> dict | None:
	if obj is None:
		return _JsonLoad(open(file, "r"))
	else:
		_JsonDump(obj, open(file, "w"))
		return None


def GetInt(msg: str, excepts=[], default=None) -> int:
	"""
	will return an integer by inputing a string with {msg, end}
	and converting it to int
	if the user enters an invalid input the function will restart
	"""
	x = input(f"{msg}")
	try:
		if x in excepts:
			return default
		y = int(x)
		return int(x)
	except ValueError:
		return GetInt(msg)


def GetFloat(msg: str, excepts=[], default=None) -> float:
	"""
	will return an float by inputing a string with {msg, end}
	and converting it to int
	if the user enters an invalid input the function will restart
	"""
	x = input(f"{msg}")
	try:
		if x in excepts:
			return default
		y = float(x)
		return float(x)
	except ValueError:
		return GetFloat(msg)


def IsPrime(ask: int) -> bool:
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


def fib(n: int) -> list[int]:
	result: list[int] = []
	a, b = 0, 1
	while a < n:
		result.append(a)
		a, b = b, a + b
	return result


class rng:
	def new(this) -> list[int]:
		this.var = []
		for _ in range(this.size):
			this.var.append(rint(this.mn, this.mx))
		return this.var

	def get(this) -> list[int]:
		if this.norep:
			return RngNoRepetition(this.mn, this.mx, this.size)
		else:
			this.var = []
			for _ in range(this.size):
				this.var.append(rint(this.mn, this.mx))
			return this.var

	def __init__(this, mn, mx, size=1, norep=False):
		this.size = size
		this.mn = mn
		this.mx = mx
		this.new
		this.norep = norep
		this.var: list[int] = []

	def __repr__(this) -> str:
		if len((var := this.var)) == 1:
			var = this.var[0]
		this.new
		return f"{var}"

	def NewSize(this, size):
		this.size = size
		this.new

	def NewMin(this, mn):
		this.mn = mn

	def NewMax(this, mx):
		this.mx = mx

	def __call__(this, size: int = -1) -> list[int]:
		if size != -1:
			this.NewSize(size)
		return this.get()


def print(*msg, end="\n", sep=", "):
	# make msg
	# sep.join(...) então os argumentos são "juntados" com o sep
	# [str(m) for m in msg] para transformar todo valor em string
	msg = sep.join([str(m) for m in msg])

	# write msg
	# escrever a msg no terminal
	stdout.write(f"{msg}{end}")

	# flush msg
	# escrever o conteúdo do terminal no cmd
	stdout.flush()


def printl(*msg, sep=", "):
	# make msg
	msg = sep.join([str(m) for m in msg])

	# write msg
	stdout.write(f"{msg}")

	# flush msg
	stdout.flush()


def prints(*msg, sep=", "):
	# make msg
	msg = sep.join([str(m) for m in msg])

	# write msg
	stdout.write(f"{msg}")


def sprint(msg):  # simple print
	stdout.write(msg)


def input(*msg, sep=", "):
	printl(*msg, sep=sep)
	for line in sin:
		msg = line[:-1]
		break

	return msg


def GCH(TEQ):
	ch = GetCh()
	if type(TEQ) == list:
		return ch in TEQ
	return ch == TEQ


class COLOR:
	nc = "\033[0;00m"

	black = "\033[0;30m"
	red = "\033[0;31m"
	green = "\033[0;32m"
	magenta = "\033[0;35m"
	blue = "\033[0;34m"
	cyan = "\033[0;36m"
	white = "\033[0;37m"
	GreenishCyan = "\033[0;96m"  # kinda too complex
	orange = "\033[0;33m"  # bruh
	# orange			=			"\033[0;91m" # bruh

	DarkBlue = "\033[0;94m"

	BrOrange = "\033[0;93m"
	BrMagenta = "\033[0;95m"
	BrYellow = "\033[0;97m"
	BrGrey2 = "\033[0;110m"

	DarkGrey = "\033[0;90m"
	DarkCyan = "\033[0;92m"
	BkDarkGrey = "\033[0;100m"

	Bkblack = "\033[0;40m"
	BkOrange = "\033[0;43m"
	BkOrange2 = "\033[0;101m"
	BkRed = "\033[0;43m"
	BkGreen = "\033[0;42m"
	BkCyan = "\033[0;44m"
	BkMagenta = "\033[0;45m"
	BkCyan = "\033[0;46m"
	BkWhite = "\033[0;47m"
	BkCyan = "\033[0;102m"
	BkBlue = "\033[0;104m"
	BkCyan = "\033[0;106m"
	BkWhite = "\033[0;107m"

	BkBrOrange = "\033[0;103m"
	BkBrGrey = "\033[0;105m"

	MODE_LIGHT = 1
	MODE_DIM = 2
	MODE_ITALICS = 3
	MODE_UNDERLINED = 4
	MODE_BLINK = 5
	MODE_SIX = 6  # idk what it is
	MODE_BKGROUND = 7
	MODE_HIDDEN = 8
	MODE_CROSSED = 9


# Regular Colors


class color:
	Black = "\x1b[0;30m"
	Red = "\x1b[0;31m"
	Green = "\x1b[0;32m"
	Yellow = "\x1b[0;33m"
	Blue = "\x1b[0;34m"
	Purple = "\x1b[0;35m"
	Cyan = "\x1b[0;36m"
	White = "\x1b[0;37m"
	# Reset
	Reset = "\x1b[0m"

	class Regular:
		Black = "\x1b[0;30m"
		Red = "\x1b[0;31m"
		Green = "\x1b[0;32m"
		Yellow = "\x1b[0;33m"
		Blue = "\x1b[0;34m"
		Purple = "\x1b[0;35m"
		Cyan = "\x1b[0;36m"
		White = "\x1b[0;37m"

	class Bold:
		Black = "\x1b[1;30m"
		Red = "\x1b[1;31m"
		Green = "\x1b[1;32m"
		Yellow = "\x1b[1;33m"
		Blue = "\x1b[1;34m"
		Purple = "\x1b[1;35m"
		Cyan = "\x1b[1;36m"
		White = "\x1b[1;37m"

	class Underline:
		Black = "\x1b[4;30m"
		Red = "\x1b[4;31m"
		Green = "\x1b[4;32m"
		Yellow = "\x1b[4;33m"
		Blue = "\x1b[4;34m"
		Purple = "\x1b[4;35m"
		Cyan = "\x1b[4;36m"
		White = "\x1b[4;37m"

	class Background:
		Black = "\x1b[40m"
		Red = "\x1b[41m"
		Green = "\x1b[42m"
		Yellow = "\x1b[43m"
		Blue = "\x1b[44m"
		Purple = "\x1b[45m"
		Cyan = "\x1b[46m"
		White = "\x1b[47m"

	class HighIntensty:
		Black = "\x1b[0;90m"
		Red = "\x1b[0;91m"
		Green = "\x1b[0;92m"
		Yellow = "\x1b[0;93m"
		Blue = "\x1b[0;94m"
		Purple = "\x1b[0;95m"
		Cyan = "\x1b[0;96m"
		White = "\x1b[0;97m"

	class BoldHighIntensty:
		Black = "\x1b[1;90m"
		Red = "\x1b[1;91m"
		Green = "\x1b[1;92m"
		Yellow = "\x1b[1;93m"
		Blue = "\x1b[1;94m"
		Purple = "\x1b[1;95m"
		Cyan = "\x1b[1;96m"
		White = "\x1b[1;97m"

	class HighIntenstybackgrounds:
		Black = "\x1b[0;100m"
		Red = "\x1b[0;101m"
		Green = "\x1b[0;102m"
		Yellow = "\x1b[0;103m"
		Blue = "\x1b[0;104m"
		Purple = "\x1b[0;105m"
		Cyan = "\x1b[0;106m"
		White = "\x1b[0;107m"


def RGB(r:int | str, g : int | str, b: int | str) -> str:
	return "\x1b[38;2;%s;%s;%sm" % (r, g, b)

def _RGB(z, x, r, g, b) -> str: # what is z and x?!?!
	return "\x1b[%s;%s;%s;%s;%sm" % (z, x, r, g, b)

# color modes:
# 1:light, 2:dim, 3:italics, 4:underline, 5:blink
# 7:bkground, 8:hidden, 9: crossed
def SetColorMode(Color: str, mode: str | int) -> str:
	index = Color.find("[") + 1
	Colorl = list(Color)
	Colorl[index] = str(mode)
	Color = "".join(Colorl)
	return Color


def PascalCase(string, remove=" ") -> str:
	if remove in string:
		string = string[0].upper() + string[1:]
		while (ps := string.find(remove)) != -1:
			string = string[:ps] + string[ps + 1].upper() + string[ps + 2 :]
	return string


def attrs(thing: object) -> list[str]:
	return [attr for attr in dir(thing) if attr[0] != "_"]


def SplitBracket(string: str, bracket: str, closing_bracket="", Rmdadd="") -> str:

	if closing_bracket == "":
		r = {
			"(": ")",
			"[": "]",
			"{": "}",
		}
		closing_bracket = r[bracket]
	return closing_bracket.join(str(string).split(bracket)).split(closing_bracket)


def StrToMs(ipts: str) -> int:
	ipt = ipts.split()
	n, ipts = float(ipt[0]), ipt[1]
	TypesToStr = {
		("years", "year", "yrs", "yr", "ys", "y"): 220903200000,
		("weeks", "week", "w"): 604800000,
		("days", "day", "d"): 86400000,
		("hours", "hour", "hrs", "hr", "h"): 3600000,
		("minutes", "minute", "mins", "min", "m"): 60000,
		("seconds", "second", "secs", "sec", "s"): 1000,
		("milliseconds", "millisecond", "msecs", "msec", "ms"): 1,
	}
	for i in TypesToStr.keys():
		if ipts in i:
			return int(n * TypesToStr[i])
	return -1


def bhask(a, b, c) -> tuple[int, int]:
	delt = ((b ** 2) - (4 * a * c)) ** 0.5
	b *= -1  # can be anyware before x,y
	a *= 2
	x: int = (b + delt) / a
	y: int = (b - delt) / a
	return x, y


def near(
	base: float | int, num: float | int, DifUp: float | int, DifDown: float | int = 0
) -> bool:
	if not DifDown:
		DifDown = DifUp
	return (base + DifUp) >= num >= (base - DifDown)


def rsymb(size=1) -> str:
	# 33-47 58-64 160-191
	c = []
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
	# 65-90 97-122
	return lst1(
		[
			(chr(rint(65, 90))) if rint(0, 1) else (chr(rint(97, 122)))
			for char in r(size)
		]
	)


def GetWLen(msg: str, ln: int, end: str = "\n") -> int:
	assert type(ln) == int, f"lengh type != int \n {ln} of type {type(ln)} != int"
	"""
	will return an str by inputing a string with {msg, end}
	if the user enters an invalid input the function will restart
	the valid input has the same size as ln
	snippet:
	len(input) == ln
		ret
	else
		restart
	"""
	x = input(f"{msg}{end}")
	if len(x) == ln:
		return x
	else:
		return GetWLen(msg, ln, end)


def count(end: int, start: int = 0, jmp: int = 1) -> Iterator[int]:
	i = start
	if end == 0:
		while True:
			yield i
			i += jmp
	else:
		while True:
			yield i
			i += jmp
			if i >= end:
				break


# decorator
def timeit(func):
	def wrapper(*args, **kwargs) -> float:
		timer = tm()
		func(args, **kwargs)
		return round(tm() - timer, 6)

	return wrapper


def mmc(a: int, b: int) -> int:
	if not (isinstance(a, int) and isinstance(b, int)):
		raise ValueError(f"values from lcm need to be int!, a:{type(a)}, b:{type(b)}")
	if a - 1 < b or b < a + 1:
		return a * b
	G = max(a, b)
	for _ in count(0):
		G += 1
		if not G % a and not G % b:
			return G
	return -1


lcm = mmc


def factorial(n: int) -> int:
	Fact = 1
	for i in range(1, n + 1):
		Fact *= i
	return Fact


def exit(num: int = 1):
	assert type(num) == int, f"var {num} of wrong type, should be int"
	assert num < 256, f"var {num} too big, should be smaller then 256"
	exi(num)


def between(x: float | int, min: float | int, max: float | int) -> bool:
	return min < x < max


def ls(dir=".") -> list:
	return [i if isfile(f"{dir}/{i}") else f"{i}/" for i in _ls(dir)]


def rstr(
	ln: int,
	chars: bool = True,
	symbs: bool = True,
	ints: bool = True,
	intmin: int = 0,
	intmax: int = 9,
) -> str:
	ret = []
	fs: list[Callable] = []
	if chars:
		fs.append(rchar)
	if symbs:
		fs.append(rsymb)
	if ints:
		fs.append(rint)
	for _ in r(ln):
		f = ritem(fs)
		if f == rint:
			ret.append(f(intmin, intmax))
		else:
			ret.append(f())
	return "".join([str(a) for a in ret])


def ANDGroups(g1: Iterable, g2: Iterable) -> Iterable:
	G1 = set(g1)
	G2 = set(g2)
	Gall = *g1, *g2
	Gret = set()
	for i in Gall:
		if i in G1 and i in G2:
			Gret.add(i)
	return Gret


def ORGroups(
	g1: list | tuple | set | frozenset, g2: list | tuple | set | frozenset
) -> set:
	Gret = set((*g1, *g2))
	return Gret


def XORGroups(
	g1: list | tuple | set | frozenset, g2: list | tuple | set | frozenset
) -> set:
	G1 = set(g1)
	G2 = set(g2)
	Gall = *g1, *g2
	Gret = set()
	for i in Gall:
		if i in G1 + i in G2 == 1:
			Gret.add(i)
	return Gret


def NOTGroups(
	g1: list | tuple | set | frozenset, g2: list | tuple | set | frozenset
) -> set:
	G1 = set(g1)
	G2 = set(g2)
	Gret = set()
	for i in G1:
		if not i in G2:
			Gret.add(i)
	return Gret


class code:
	def __init__(this, *code, name="test", mode="exec"):
		this.name, this.mode, this.code = name, mode, list(code)

	def __add__(this, line):
		this.code.append(compile(line, this.name, this.mode))
		return this

	def __call__(this):
		if type(this.code) == str:
			this.code = this.code.split("\n")
		for line in this.code:
			exec(line)
		return 0

	def __repr__(this) -> str:
		msg = ""
		if type(this.code) == str:
			this.code = this.code.split("\n")

		if len(this.code) > 1:
			for line in this.code:
				msg += f"{line}\n"
		elif len(this.code) == 1:
			msg = f"{this.code[0]}"
		else:
			msg = ""
		return msg


class BDP:
	def __init__(this, name, autoload=True, IgnoreDataSize=False):
		# for unix like system
		# c:/users/{USER}/BDP
		this.autoload = autoload
		this.IgnoreDataSize = IgnoreDataSize
		if OS == "linux":  # gud os
			if not exists(f"/home/{USER}/BDP"):
				ss("mkdir /BDP/")
			if not name.startswith("~/BDP/"):
				name = f"~/BDP/{name}"
			name = name.replace("//", "/").replace("~", f"/home/{USER}")
		elif OS == "windows":  # bad os
			if not exists(f"C:/users/{USER}/BDP/"):
				ss(f"mkdir C:/users/{USER}/BDP/")
			if not name.startswith(f"~/BDP/"):
				name = f"~/BDP/{name}"
				# / -> \ && ~ -> C:\...
			name = name.replace("/", "\\").replace("~", f"C:\\\\users\\{USER}")
		else:
			print(
				f"""Your OS "{OS}" is not yet suported by util.BDP
if you can help, please contribute at https://OwseiWasTaken/util.py"""
			)
		this.name = name
		this.data = None
		this.exists = exists(name)
		if this.autoload and this.exists:
			this.load()

	def save(this, data=None) -> str:
		if data == None:
			data = this.data
			if data == None:
				return "no data to save"
		if not this.exists:
			with open(this.name, "w"):
				pass
		UseFile(this.name, data)
		return "saved"

	def load(this):
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
			return f"""name: {this.name}\n{COLOR.orange}data too big to display
BDP(IgnoreDataSize=True) to ignore size{COLOR.nc}"""

	def __call__(this, data=None) -> Any:  # this breaks occasionaly

		if data == None and this.data == None:
			return this.load()

		elif this.data == None:
			this.data = data

		this.save()
		return "saved"


def NumberToExponent(number: list[str]) -> str:
	smol = {
		"0": "⁰",
		"1": "¹",
		"2": "²",
		"3": "³",
		"4": "⁴",
		"5": "⁵",
		"6": "⁶",
		"7": "⁷",
		"8": "⁸",
		"9": "⁹",
		".": ".",
	}

	return "".join([smol[i] for i in str(number)])


def rbool(OneIn=2) -> int:
	return not rint(0, OneIn - 1)


def rcase(word: str, chance: float = 0.5) -> str:
	if chance == None:
		chance = 0.5
	chance *= 100
	wd = ""
	for char in word:
		if chance >= rint(0, 100):
			char = char.upper()
		else:
			char = char.lower()
		wd += char
	return wd


# TODO(#5): test EncryptS func
def EncryptS(var: str, key: int) -> list[int]:
	return [ord(char) + key for char in var]
	# ret = []
	# for char in str(var):
	# ret.append(ord(char)+key)
	# return ret


# TODO(#6): test DecryptS func
def DecryptS(var: list[int], key: int) -> str:
	return "".join([f"{chr(char-key)}" for char in var])
	# ret = []
	# for char in var:
	# ret.append(f"{chr(char-key)}")
	# return "".join(ret)


def AdvEncryptS(var, key, deep) -> list[int]:
	if deep <= 0:
		deep = 1
	if deep == 1 or deep == 0:
		return EncryptS(var, key)
	else:
		return AdvEncryptS(var, key * deep, deep - 1)


def AdvDecryptS(var, key, deep) -> str:
	if deep <= 0:
		deep = 1
	if deep == 1:
		return DecryptS(var, key)
	else:
		return AdvDecryptS(var, key * deep, deep - 1)


def numbers(times, nums=0) -> int:
	return eval(f"[{nums}" + f", {nums}" * (times - 1) + "]")


def ShowTextGif(sprites, SleepTime=0.35, times=-1):
	# if times is negative the loop won't stop || if times = 0, it will be len(sprites)
	if times == 0:
		times = len(sprites)
	if times < 0:
		while True:
			for sprite in sprites:
				clear()
				stdout.write(sprite)
				sleep(SleepTime)
	else:
		for tick in r(times):
			for sprite in sprites:
				clear()
				stdout.write(sprite)
				sleep(SleepTime)


def JustDecimal(number: float) -> float:
	return number - int(number)


def NoDecimal(number: float) -> int:
	return int(number)


def number(num: str) -> int | float | None:
	if all([char in "0987654321+-.*/" for char in num]):
		return eval(num)
	return None


def TimesInNumber(TimesIn, NumberTo) -> bool:
	return not not (sum([rbool(TimesIn) for x in r(NumberTo)]))
	# return bo/ol(sum([rbool(TimesIn) for x in r(NumberTo)]))


def NumSum(numbers: int | float) -> int:
	snumbers = str(numbers).replace(".", "")
	inumbers = int(snumbers)
	if len(snumbers) != 1:
		return NumSum(inumbers)
	else:
		return inumbers


def FindAll(StringToSearchIn: str, StringToFind: str) -> list[int]:
	# get replacable string
	NotStringToFind = StringToFind[1:] + chr(ord(StringToFind[-1]) + 1)
	times = StringToSearchIn.count(StringToFind)

	ret = []
	for i in r(times):
		ret.append(StringToSearchIn.find(StringToFind))
		StringToSearchIn = StringToSearchIn.replace(StringToFind, NotStringToFind, 1)
	return ret


def RDDeepSum(args, ParseStringWith=eval, ParseString=False) -> tuple[int, int]:
	ret = 0
	deeph = 0
	for thing in args:
		deeph += 1
		if type(thing) in (float, int):
			# add number
			ret += thing
		elif type(thing) == str:
			if ParseString:
				# parse and add string
				ret += ParseStringWith(thing)
			else:
				# breaks because found string
				raise TypeError(
					"""
%sERROR IN "DeepSum" function%s
value %s is of type string (and ParseString = False)"""
					% (COLOR.red, COLOR.nc, repr(thing))
				)
		else:
			# recourciveness (it that a word?)
			deeph -= 1
			RetA, DeephA = RDDeepSum(
				thing,
				ParseStringWith=ParseStringWith,
				ParseString=ParseString,
			)
			# adds the nums and deeph of recourcive run
			ret += RetA
			deeph += DeephA

	return ret, deeph


def DeepSum(args, ParseStringWith=eval, ParseString=False) -> int:
	"""
	this function will add everything in the iterable in {args}, even strings!
	this function will return deeph of the iterable in {ReturnDeeph} is True (will calculate deeph any way tho)
	this ReturnDeeph var adds one for every item but iterables (but will count the deeph in side the iterables!)
	"""
	ret = 0
	deeph = 0
	for thing in args:
		deeph += 1
		if type(thing) in (float, int):
			# add number
			ret += thing
		elif type(thing) == str:
			if ParseString:
				# parse and add string
				ret += ParseStringWith(thing)
			else:
				# breaks because found string
				raise TypeError(
					"""
%sERROR IN "DeepSum" function%s
value %s is of type string (and ParseString = False)"""
					% (COLOR.red, COLOR.nc, repr(thing))
				)
		else:
			# recourciveness (it that a word?)
			deeph -= 1
			RetA, DeephA = RDDeepSum(
				thing,
				ParseStringWith=ParseStringWith,
				ParseString=ParseString,
			)
			# adds the nums and deeph of recourcive run
			ret += RetA
			deeph += DeephA

	return ret


def average(args, SumFunc=RDDeepSum) -> int:
	sum, deeph = SumFunc(args)
	return sum / deeph


def mid(
	msg, LenToBe, CanDeleteEnd=True, AddFront=" ", AddAfter=" ", DoToFront="not front"
) -> str:
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
			msg = AddFront + msg
		else:
			msg += AddAfter
	return msg


def IsIterable(obj: object) -> bool:
	return type(obj) in Iterables


def SingleList(args: list[Any]) -> list[Any]:
	ret: list[Any] = []
	for thing in args:
		if IsIterable(thing):
			# recourciveness (it that a word?)
			RetA = SingleList(thing)
			# set ret as *ret and *RetA
			ret = [*ret, *RetA]
		else:
			ret.append(thing)
	return ret


def BiggestLen(lst: list[Any]) -> int:	# biggest by len
	return max([len(str(thing)) for thing in lst])


def compare(*timest: tuple[list[int]]) -> str:
	times: list[int] = SingleList(list(times))

	avg = average(times)
	ret = f"average : {avg:.3f}\n"

	# getting biggest num (len)
	sep = BiggestLen(times)
	# sep = max([len(str(time)) for time in times])

	for i in r(times):
		time = times[i]
		ThisColor = COLOR.red if time - avg > 0 else COLOR.green

		PoM = ("" if (time - avg) < 0 else "+") + str(round(time - avg, sep - 1))

		prt = f"{i} : {COLOR.magenta}{' '*(sep-len(str(time)))}{time}{COLOR.nc} | {ThisColor}{PoM}"

		ret += prt + COLOR.nc + "\n"
	return ret


def graphics(*intst: list[int], UnderAvg=COLOR.red, OverAvg=COLOR.green) -> list[str]:
	ints: list[int] = SingleList(list(intst))

	avg = average(ints)

	manys = [round(ins / avg, 6) for ins in ints]
	ManysGraph = []

	t = {6: "⠿", 5: "⠟", 4: "⠏", 3: "⠇", 2: "⠃", 1: "⠄", 0: " "}
	for ManyIndex in r(manys):
		many = manys[ManyIndex]
		scale = round(many / (1 / 6))  # one for each braille ball
		fulls = scale // 6
		l = f"{ManyIndex} : "

		if scale > avg:
			l += OverAvg
		else:
			l += UnderAvg

		l += t[6] * fulls
		l += t[scale % 6]
		l += COLOR.nc
		ManysGraph.append(l)

	return ManysGraph


def pos(y: int, x=0) -> str:
	return "\x1B[%i;%iH" % (y + 1, x + 1)


def ppos(y, x):
	stdout.write("\x1B[%i;%iH" % (y + 1, x + 1))
	stdout.flush()


def ClearCollum(x, GetTerminalX="default", char=" ", start=COLOR.nc, end=COLOR.nc):
	if GetTerminalX == "default":
		_, y = GetTerminalSize()
	else:
		y = GetTerminalX()
	for i in r(y):
		stdout.write("%s" % (start + pos(i, x) + char + end))
	stdout.flush()


def DrawHLine(x, XTo, y, Color, char=" "):
	ps = pos(y, x)
	_x, _y = GetTerminalSize()
	len = (XTo - x) + 1
	stdout.write(
		ps + Color + char * len + COLOR.nc + char * (_x - len)
	)  # if optmizing change XTO -> msg lenght
	stdout.flush()


def DrawVLine(y, YTO, x, colo, char=" "):
	for i in range(0, YTO + 1)[y:]:
		stdout.write("%s" % pos(i, x) + colo + char + COLOR.nc)
	stdout.flush()


def DrawSpot(y, x, char):
	stdout.write(pos(y, x) + char)


def ColorSpot(y, x, Color):
	stdout.write(pos(y, x) + Color + " " + COLOR.nc)


def HideCursor():
	stdout.write("\x1b[?25l")
	stdout.flush()


def ShowCursor():
	stdout.write("\x1b[?25h")
	stdout.flush()


def DrawRectangle(UpLeft, DownRight, BkColor, DoubleWidthVerticalLine=False):
	y1, x1 = UpLeft
	y2, x2 = DownRight
	# |x1, -y1
	#
	#	|x2, -y2

	# DrawVLine(y, YTO, x, colo)
	DrawVLine(y1, y2, x1, BkColor)
	DrawVLine(y1, y2, x2, BkColor)
	if DoubleWidthVerticalLine:
		DrawVLine(y1, y2, x1 + 1, BkColor)
		DrawVLine(y1, y2, x2 - 1, BkColor)

	# DrawHLine(x, XTo, y, colo)
	DrawHLine(x1, x2, y1, BkColor)
	DrawHLine(x1, x2, y2, BkColor)


def ReplaceStringByIndex(string: str, index: int, result: str) -> str:
	return string[:index] + result + string[index + 1 :]


class TextBox:
	def __init__(this, StartString="", DrawRect=True, DoClear=True):
		this.DrawRect = DrawRect
		this.DoClear = DoClear
		this.PrintableChars = " óíáàéç!\"#$%&'()*+, -./0123456789:;<=>\
?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_´`abcdefghijklmnopqrstuvwxyz{|}~"
		this.HSize, this.VSize = GetTerminalSize()
		this.TextSixe = this.HSize - 2
		this.STRING = StartString
		this.CURSOR = len(this.STRING) - 1
		this.STRING += " " * (this.TextSixe - len(this.STRING))

	def __call__(this) -> str:
		return this.loop()

	def IsPrintableChar(this, char) -> bool:
		return char in this.PrintableChars

	def SetChar(this, char):
		if char == "\x1b":	# escape key
			if GetCh() == "[":	# escape code
				ch = GetCh()

				if ch == "C" and this.CURSOR < len(this.STRING) - 2:  # go right
					this.CURSOR += 1
				elif ch == "D" and this.CURSOR > -1:  # go left
					this.CURSOR -= 1

				elif ch == "3":  # may be del
					ch = GetCh()
					if ch == "~":  # delete key
						this.STRING = list(this.STRING)
						this.STRING.pop(this.CURSOR + 1)
						this.STRING = "".join(this.STRING) + " "

				# elif ch == '2': # may be insert
				# ch = GetCh()
				# if ch == '~': # insert key
				# pass

		elif char == "\x7f" and this.CURSOR > -1:  # backspace
			if (
				not this.CURSOR == len(this.STRING) - 2 or not this.IsOverChar
			):	# "normal" delete
				this.STRING = list(this.STRING)
				this.STRING.pop(this.CURSOR)
				this.STRING = "".join(this.STRING) + " "
				this.CURSOR -= 1
			else:  # if @ $ of line del not backspace
				this.STRING = list(this.STRING)
				this.STRING[this.CURSOR + 1] = " "
				this.STRING = "".join(this.STRING)

		else:
			if this.IsPrintableChar(char):
				if (
					this.CURSOR < len(this.STRING) - 2
				):	# if char is going to be added move cursor right
					this.CURSOR += 1
				if this.CURSOR >= len(
					this.STRING
				):	# if cursor if off screen get it back
					this.CURSOR -= 1

				# strg = this.STRING.strip()
				# if len(strg)-1 <= this.CURSOR:
				# strg = this.STRING[:this.CURSOR]
				# ClearLine(1)
				# stdout.write(f"{pos(1, 1)}{repr(strg)}{len(strg)-1 == this.CURSOR}|{len(strg)}|{this.CURSOR}")
				# if not len(strg)-1 == this.CURSOR: # place not replace

				if (
					this.STRING[-1] == " "
				):	# move string right to add char to CURSOR's spot
					this.STRING = list(this.STRING)[:-1]
					this.STRING.insert(this.CURSOR, char)
					this.STRING = "".join(this.STRING)
				else:
					this.STRING = ReplaceStringByIndex(
						this.STRING, this.CURSOR, char
					)  # create or replace

	@property
	def IsOverChar(this) -> bool:
		return this.STRING[this.CURSOR + 1] != " "

	def loop(this) -> str:
		ShowCursor()
		if this.DoClear:
			clear()
		if this.DrawRect:
			DrawRectangle(
				(this.VSize - 3, 0),
				(this.VSize, this.HSize - 1),
				BkColor=COLOR.BkBrGrey,
			)
		char = ""

		# chars = []

		while True:
			# stdout.write(pos(this.VSize-1, this.HSize))

			# chars.append(repr(char))

			if char == "\r":  # <Enter> to send
				return this.STRING.strip()

			this.SetChar(char)

			# stdout.write(f"{pos(1, 1)}{chars}")
			# ClearLine(4)
			# stdout.write(f"{pos(4, 4)} \

			if this.DrawRect:
				stdout.write(f"{pos(this.VSize-2, 1)}{COLOR.nc}{this.STRING}")
				stdout.write(pos(this.VSize - 2, this.CURSOR + 2))
			else:
				stdout.write(f"{pos(this.VSize-1, 1)}{COLOR.nc}{this.STRING}")
				stdout.write(pos(this.VSize - 1, this.CURSOR + 2))

			stdout.flush()

			char = GetCh()


def GetPrimeFactors(number: int) -> list[int]:
	factor = 2
	ret = []
	while factor <= number:
		if not number % factor:
			ret.append(factor)
			number //= factor
			factor += 1
		else:
			factor += 1
	return ret


class OStream:
	def __init__(this, OutHandler=stdout, InHandler=stdin):
		this.outs = OutHandler
		this.ins = InHandler

	def __lshift__(this, msg: str):
		return (this, this.outs.write("%s" % msg))[0]

	def __rshift__(this, msg: str):
		if this.ins.readable():
			this.outs.write(msg)
			this.outs.flush()
			for line in this.ins:
				msg = line[:-1]
				break
			return msg
		else:
			raise ValueError(f"{{{this}}}\ncan't read from out read steam!")


class get:
	def __init__(this, *gets, argvs=None):
		if not gets:
			gets = [None]
		gets = list(gets)
		for index in r(gets):
			if gets[index] == "":
				gets[index] = None
			if type(gets[index]) != NoneType and gets[index][0] != "-":
				gets[index] = "-" + gets[index]
		if argvs == None:
			global ARGV
			argvs = ARGV
		this.argvs = argvs
		this.gets = gets

		stuff = this._get()
		this.list = stuff[0]
		this.first = None
		this.last = None
		if not this.list == None and len(this.list):
			this.first = this.list[0]
			this.last = this.list[-1]
		this.bool = stuff[1]
		this.eval = stuff[2]
		this.exists = stuff[-1]
		this.stuff = stuff

	def __getitem__(this, index):
		return this.list[index]

	def _get(this) -> list:
		ret: list[list[str] | str | bool | None] = []
		other: list[str] = []
		this.argvs

		for indicator in SingleList(this.gets):  # list

			other = [*other, *this.argvs.get(indicator, [])]
		if other:
			ret.append(other)
		else:
			ret.append([])

		if other:  # MakeBool
			if other[0] in "-+0987654321":
				ret.append(not not eval(other[0]))
			else:
				ret.append(True)
		else:
			ret.append(None)

		if other and other[0] in "-+987654321":  # MakeEval
			ret.append(eval(other[0]))
		else:
			ret.append(None)

		al = list(this.argvs.keys())
		ret.append(any([x in al for x in this.gets]))  # exists

		return ret

	def __len__(this):
		return len(this.list)


def _RmDirLinux(dir: str) -> int:
	return ss(f"rm -rf {dir}")


def _RmDirWindows(dir: str) -> int:  # not sure if works
	for file in ls(dir):
		if file.endswith("/"):
			_RmDirWindows(file)
		else:
			ss("del file")
	else:
		_rmdir(dir)

	return 0


def RmDir(dir: str):
	if OS == "linux":
		_RmDirLinux(dir)
	elif OS == "windows":
		_RmDirWindows(dir)
	else:
		print(
			f"""Your OS {OS} is not yet suported by util.RmDir
if you can help, please contribute at https://OwseiWasTaken/util.py"""
		)


def TrimSpaces(string: str) -> str:
	while "  " in string:
		string = string.replace("  ", " ")
	return string


def TrimChar(string: str, remove="	", replace=" ") -> str:
	while remove in string:
		string = string.replace(remove, replace)
	return string


def Hamiltons(benefit, probability, cost) -> bool:
	return benefit * probability / cost > 0


def ReplaceAll(StringList: list[str], FromString: str, ToString: str) -> list[str]:
	if type(StringList) in [list, set, tuple]:
		for index in r(StringList):
			if type(StringList[index]) == str:
				StringList[index] = StringList[index].replace(FromString, ToString)
			elif type(StringList[index]) in [list, set, tuple]:
				StringList[index] = ReplaceAll(StringList[index], FromString, ToString)
	return StringList


def MakeString(
	line: str,
	sep: str = " ",
	quote: str = '"',
	escape="\\",
	MaintainQuotes: bool = True,
) -> list[str]:
	InString = False
	ret: list[str] = []
	now = ""
	for pos in r(line):
		char = line[pos]
		if char == quote and pos > 0 and line[pos - 1] != escape:
			if MaintainQuotes:
				now += '"'
			InString ^= InString  # invert
		else:
			# " start or end string
			if char == sep and not InString:
				ret.append(now)
				now = ""
			else:
				now += line[pos]
	if now:
		ret.append(now)
	return ret


def IsListSorted(lst: list, reverse: bool = False):
	return lst == sorted(lst, reverse=reverse)


class window:
	def __init__(
		this,
		MinY,
		MinX,
		MaxY,
		MaxX,
		UpdateFunc=lambda *x: x,
		AvoidDrawedinBorder=True,
		DrawBottom=True,
		DrawTop=True,
		DrawLeft=True,
		DrawRight=True,
	):
		this.MaxX = MaxX
		this.DrawBottom, this.DrawTop, this.DrawLeft, this.DrawRight = (
			DrawBottom,
			DrawTop,
			DrawLeft,
			DrawRight,
		)
		this.MaxY = MaxY
		this.MinY = MinY
		this.MinX = MinX
		this.XDif = MaxX - MinX
		this.YDif = MaxY - MinY
		this.PX = this.XDif - 1
		this.PY = this.YDif - 1
		this.tl = (MinY, MinX)
		this.tr = (MinY, MaxX - 1)
		this.br = (MaxY - 1, MaxX - 1)
		this.bl = (MaxY - 1, MinX)
		this.UpdateFunc = UpdateFunc
		this.DrawedBorder = False
		this.AvoidDrawedinBorder = AvoidDrawedinBorder
		this.BorderColor = "\033[7;90m"
		this.y = 0
		this.x = 0

	def __call__(this, args=None):
		return this.update(this, args)

	def write(this, msg: str):
		stdout.write(pos(this.y, this.x) + msg)

	def wprint(this, y, x, msg):
		this.y = y
		this.x = x
		stdout.write(pos(y, x) + msg)

	def print(this, y, x, msg, relative=True):
		if this.AvoidDrawedinBorder:
			x += this.DrawedBorder
			y += this.DrawedBorder
		if relative:
			y += this.MinY
			x += this.MinX
			if this.MinY < y < this.MaxY:
				raise ValueError(
					f"y {y} is {'bigger' if x > this.MaxX else 'smaller'} then window's y size {this.MaxY}"
				)
			elif this.MinX < x < this.MaxX:
				raise ValueError(
					f"x {x} is {'bigger' if x > this.MaxX else 'smaller'} then window's x size {this.MaxX}"
				)
		stdout.write(f"{pos(y, x)}{msg}")
		stdout.flush()

	def ClearLine(this, y, char=" ", start=COLOR.nc, end=COLOR.nc, relative=True):
		if relative:
			y += this.MinY
			if y > this.MaxY:
				raise ValueError(f"y {y} is bigger then window's y size {this.MaxY}")
			elif y < this.MinY:
				raise ValueError(f"y {y} is smaller then window's y size {this.MinY}")
		ClearLine(y, char=char, start=start, end=end)

	def DrawOutline(this, Color=-1):
		if Color == -1:
			Color = this.BorderColor
		# def DrawRectangle(UpLeft, DownRight, BkColor, DoubleWidthVerticalLine=False):
		# DrawBottom, DrawTop, DrawLeft, DrawRigh
		x1, y1 = this.MinX - 1, this.MinY - 1
		x2, y2 = this.MaxX, this.MaxY + 1  # may do -1 @ MaxX
		if this.DrawBottom:
			DrawHLine(x1, x2, y2, Color)  # bottom
		if this.DrawTop:
			DrawHLine(x1, x2, y1, Color)  # top
		if this.DrawLeft:
			DrawVLine(y1, y2, x1, Color)  # left
		if this.DrawRight:
			DrawVLine(y1, y2, x2, Color)  # right

		# DtrawRectangle(
		#	(this.MinX-1, this.MinY-1),
		#	(this.MaxX+1, this.MaxY+1),
		#	COLOR.BkDarkGrey
		# )

	def DrawBorder(this, Color=-1):
		if Color == -1:
			Color = this.BorderColor
		this.DrawedBorder = True
		DrawRectangle(this.tl, this.bl, Color)

	def move(this, y, x, relative=True):
		if relative:
			y += this.MinY
			x += this.MinX
			if y > this.MaxY:
				raise ValueError(f"y {y} is bigger then window's y size {this.MaxY}")
			elif y < this.MinY:
				raise ValueError(f"y {y} is smaller then window's y size {this.MinY}")
			elif x > this.MaxX:
				raise ValueError(f"x {x} is bigger then window's x size {this.MaxX}")
			elif x < this.MinX:
				raise ValueError(f"x {x} is smaller then window's x size {this.MinX}")
		this.y = y
		this.x = x

	def update(this, *args):
		return this.UpdateFunc(this, args)


def TestAll(lst: list[Any], test=lambda x: not not x):
	WK = True
	for item in lst:
		if not test(item):
			WK = False
	return WK


def TestAny(lst: list[Any], test=lambda x: not not x):
	WK = False
	for item in lst:
		if test(item):
			WK = True
	return WK


def GetQuadrant(x, y):
	x = PosOrNeg(x)
	y = PosOrNeg(y)
	return {(1, 1): 1, (1, -1): 4, (-1, 1): 2, (-1, -1): 3}.get((x, y), 0)


def CursorMode(mode: str):
	stdout.write(
		"\033["
		+ {
			"blinking block": "1",
			"block": "2",
			"blinking underline": "3",
			"underline": "4",
			"blinking I-beam": "5",
			"I-beam": "6",
		}.get(mode, "0")
		+ " q"
	)
	stdout.flush()


class _AdvTextBox:
	def __init__(this, tl, br, content, DrawSides, update, UpperMode, CustomStatusBar):
		this.update = update
		this.win = window(*tl, *br, this.loop, *DrawSides)
		if UpperMode:
			this.win.YMode = this.win.MinY - 2
		else:
			this.win.YMode = this.win.MaxY + 1
		this.tadd = lambda x: ""
		if CustomStatusBar:
			if type(CustomStatusBar) == list:
				this.tadd = CustomStatusBar[0]
			else:
				this.ShowMode = CustomStatusBar
		this.AvaliableChars = " óòíìáàéèúùç!#$%&'\"(*)+-.,/0123456789:;<=>\
?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_´`abcdefghijklmnopqrstuvwxyz{|}~"
		this.cursor = 0
		this.line = 0
		this.ContSize = this.win.YDif + 1
		this.cont = list(content)
		if len(content) <= this.ContSize:
			this.cont = content
			for i in r(this.ContSize - len(content)):
				this.cont.append("")
		this.InNormalMode = True
		this.InReplace = False
		CursorMode("block")
		ShowCursor()
		this.CtrlChar = {
			"\x01": "A",
			"\x02": "B",
			"\x03": "C",
			"\x04": "D",
			"\x05": "E",
			"\x06": "F",
			"\x07": "G",
			"\x08": "H",
			"\x09": "I",
			"\x0A": "J",
			"\x0B": "K",
			"\x0C": "L",
			"\x0D": "M",
			"\x0E": "N",
			"\x0F": "O",
			"\x10": "P",
			"\x11": "Q",
			"\x12": "R",
			"\x13": "S",
			"\x14": "T",
			"\x15": "U",
			"\x16": "V",
			"\x17": "W",
			"\x18": "X",
			"\x19": "Y",
			"\x1A": "Z",
		}
		this.DrawRect = any(DrawSides)
		this.CharList = []
		this.CommandChars = "aixhlRjkr"
		this.SpecialInserChars = [
			"ESC",
			"DEL",
			"RIGHT",
			"LEFT",
			"BACKSPACE",
			"DOWN",
			"UP",
			"TIO",
		]

	def SpecialChar(this, default):
		CL = "".join(this.CharList)
		debug(this.CharList)
		if len(this.CharList) > 6:
			this.CharList = this.CharList[:-5]
		if CL[-4:] == "\x1b[3~":
			return "DEL"
		elif CL[-3:] == "\x1b[D":
			return "LEFT"
		elif CL[-3:] == "\x1b[C":
			return "RIGHT"
		elif CL[-3:] == "\x1b[A":
			return "UP"
		elif CL[-3:] == "\x1b[B":
			return "DOWN"
		elif CL[-1] == "\x1b":
			return "ESC"
		elif CL[-1] == "\x7f":
			return "BACKSPACE"
		elif CL[-1] in this.CtrlChar.keys():
			return "^" + this.CtrlChar[CL[-1]]
		elif CL[-1] == "~":
			return "TIO"
		else:
			return default

	def normal(this, char):
		if not char in this.CommandChars:
			char = this.SpecialChar("ESC")
		if char == "ESC":
			pass
		elif char == "i":
			this.InNormalMode = False
			this.UpdateCursor()
		elif char == "R":
			this.InNormalMode = False
			this.InReplace = True
		elif char == "a":
			if not len(this.string) < this.cursor + 1:
				this.cursor += 1
			this.InNormalMode = False
			this.UpdateCursor()
		elif char in ["l", "RIGHT"]:
			if not len(this.string) < this.cursor + 1:
				this.cursor += 1
		elif char in ["h", "LEFT"]:
			if this.cursor:
				this.cursor -= 1
		elif char in ["j", "DOWN"]:
			if this.line < this.ContSize - 1:
				this.line += 1
			this.string = this.cont[this.line]
			if this.cursor >= len(this.string):
				this.cursor = len(this.string) - 1
			if this.cursor < 0:
				this.cursor = 0
		elif char in ["k", "UP"]:
			if this.line:
				this.line -= 1
			this.string = this.cont[this.line]
			if this.cursor >= len(this.string):
				this.cursor = len(this.string) - 1
			if this.cursor < 0:
				this.cursor = 0
		elif char in ["x", "DEL"]:
			if len(this.string):
				this.string = ReplaceStringByIndex(this.string, this.cursor, "")
		elif char == "BACKSPACE":
			if len(this.string):
				# this.string = ReplaceStringByIndex(this.string, this.cursor-1, '')
				if this.cursor >= 1:
					this.cursor -= 1
		elif char == "TIO":
			if len(this.string) > this.cursor:
				ch = this.string[this.cursor]
				if ch.isupper():
					ch = ch.lower()
				else:
					ch = ch.upper()
				this.string = ReplaceStringByIndex(this.string, this.cursor, ch)
		elif char == "r":
			CursorMode("underline")
			ch = GetCh()
			if ch != "\x1b":
				this.string = ReplaceStringByIndex(this.string, this.cursor, ch)
			CursorMode("block")

	def insert(this, char):
		if char in this.AvaliableChars and len(this.string) + 1 < this.win.MaxX:
			this.cursor += this.StringInsert(char)
			# this.cursor+=1
		else:
			if not char in this.SpecialInserChars:
				char = this.SpecialChar("PASS")
		if char == "PASS":
			return
		elif char == "ESC":
			if this.cursor:
				this.cursor -= 1
			this.InNormalMode = True
			this.InReplace = False
			this.UpdateCursor()
		elif char == "BACKSPACE":
			if len(this.string):
				if this.cursor >= 1:
					this.string = ReplaceStringByIndex(this.string, this.cursor - 1, "")
					this.cursor -= 1
		elif char == "RIGHT":
			if not len(this.string) < this.cursor + 1:
				this.cursor += 1
		elif char == "LEFT":
			if this.cursor:
				this.cursor -= 1

	@staticmethod  # decorator for custom status bar
	def ShowMode(this):
		if this.InNormalMode:
			t = SetColorMode(COLOR.green, "7") + " normal "
		else:
			if this.InReplace:
				t = SetColorMode(COLOR.red, "7") + " replace "
			else:
				t = SetColorMode(COLOR.cyan, "7") + " insert "
		t += COLOR.nc
		char = this.SpecialChar(this.CharList[-1])	# "get" char
		t += f"{COLOR.BkDarkGrey} {char}"
		t += this.tadd(this)
		printl(pos(this.win.YMode, 0) + t + COLOR.nc)

	def loop(this):
		ch = " "
		while True:
			this.string = this.cont[this.line]
			this.CharList.append(ch)
			if ch == "\r":
				this.InNormalMode = True
				this.UpdateCursor()
				if len(this.cont) == 1:
					return this.string
				else:
					return this.cont
			if this.InNormalMode:
				this.normal(ch)
			else:
				this.insert(ch)
			ToPrint = ""
			for lnn in r(this.cont):
				ln = this.cont[lnn]
				if lnn == this.line:
					ln = this.string
				this.win.ClearLine(lnn + this.win.MinY, relative=False)
				if this.win.DrawLeft:
					ColorSpot(lnn + this.win.MinY, 0, COLOR.BkDarkGrey)
				if this.win.DrawRight:
					ColorSpot(lnn + this.win.MinY, this.win.MaxX, COLOR.BkDarkGrey)
				if ln:
					ToPrint += pos(lnn + this.win.MinY, 1) + ln
				# this.win.print(lnn+this.win.MinY, 1, ln, False)
			else:
				ToPrint += pos(0, this.win.XDif - 2) + " "
				# this.win.print(0, this.win.XDif-2, ' ', False)
			stdout.write(ToPrint)
			if this.DrawRect:
				this.win.DrawOutline()
			this.ShowMode(this)
			this.update(this)
			this.win.move(
				this.line + this.win.MinY, this.cursor + this.win.MinX, relative=False
			)
			ch = GetCh()
			this.cont[this.line] = this.string

	def UpdateCursor(this):
		if this.InNormalMode:
			CursorMode("block")
		else:
			if this.InReplace:
				CursorMode("underline")
			else:
				CursorMode("I-beam")

	def __call__(this):
		return this.loop()

	def StringInsert(this, char) -> int:
		ret = 0
		string = list(this.string)
		if this.InReplace:
			if this.cursor >= len(string):
				string.append(char)
			else:
				string[this.cursor] = char
		else:
			string.insert(this.cursor, char)
		this.string = "".join(string)
		ret = 1
		return ret


def AdvTextBox(
	tl,
	br,
	content="",
	DrawSides=(True, True, True, True),
	update=lambda *x: x,
	UpperMode=False,
	CustomStatusBar=False,
):
	# drawsides = (bottom, top, left, right)
	return _AdvTextBox(tl, br, content, DrawSides, update, UpperMode, CustomStatusBar)()


def ArgvAssing(
	args: list[str],
) -> dict[None | str, list[str]]:  # omfg it's so much better
	# if args is [-d 4 u -4 f -d j /-3 -f]
	# ret will be {
	# items that start with '-' will be a key, the rest wil be values
	# items that start with "/-" will be values, but the starting '/' will be removed
	ret: dict[None | str, list[str]] = {None: []}
	now = None
	for arg in args:
		if arg[0] == "-":
			ret[(now := arg)] = ret.get(arg, [])
		else:
			if arg[0:2] == "/-":
				arg = arg[1:]
			if arg[0:3] == "\/-":
				arg = arg[1:]
			ret[now].append(arg)
	return ret


def eprint(*msg, end="\n", sep=", "):
	msg = sep.join([str(m) for m in msg])
	stderr.write(f"{msg}{end}")
	stderr.flush()


def distance(y: int, x: int) -> int:
	# (x>y) 2x-y-x = x-y
	return 2 * max(y, x) - y - x


def DoAll(lst, func):
	if type(func) != FuncType:
		lst, func = func, lst
	return list(map(func, lst))


class Filer:  # plain text, for UseFile file check BDP (in this lib)
	def __init__(this, name, contents=[], ReadIfExistis=True):
		name = abspath(name)  # absolute path
		if ReadIfExistis and exists(name):
			with open(name, "r") as file:
				lines = file.readlines()
				if lines:
					contents.append(*DoAll(lines, lambda x: x.replace("\n", "")))
		this.name = name
		this.contents = contents
		this.ext = name.split(".")[-1]	# thing after last .

	def __repr__(this):
		return f"{this.name}\n{len(this.contents)} lines\n{len(''.join(this.contents))} chars"

	def write(this):
		with open(this.name, "w") as file:
			for line in this.contents:
				file.write(line + "\n")

	def get(this, linen):
		return this.contents[linen]

	def append(this, cont):
		this.contents.append(cont)

	def __add__(this, cont):
		this.contents.append(cont)
		return this

	def __call__(this, line):
		this.content.append(line)

	def insert(this, line, place):
		this.content.insert()


def IsLeapYear(year=None):
	if year == None:
		year = int(time.year)
	if not year % 4:
		if not year % 100:
			if not year % 400:
				return True
			else:
				return False
		else:
			return True
	else:
		return False


def debugp(name, text, OuterColor=COLOR.nc, InnerColor=COLOR.nc):  # debug print
	stdout.write(
		f"{OuterColor}[{InnerColor}{name.upper()}{OuterColor}]{COLOR.nc} {text}\n"
	)


__sprintf_types: dict[str, Callable[[Any], Any]] = {
	"i": int,
	"f": float,
	"s": str,
	"b": bool,
	"t": bool,
	"x": hex,
	"r": repr,
}

__: dict[str, Callable[[Any], Any]] = __sprintf_types.copy()
for _ in __sprintf_types.keys():
	__["l" + _] = lambda x: [__[_](y) for y in x]
	__["t" + _] = lambda x: tuple([__[_](y) for y in x])
	# dict ain't workin :(
	# __['d'+_]=lambda x: dict([__[_](k) : __[_](v) for k, v in x.items()])
__sprintf_types = __

__sprintf_sj = "|".join(__sprintf_types.keys())
__sprintf_regex = comreg(rf"\{{({__sprintf_sj})\}}")


@cache
def sprintf(string, *stuff, HideErrors=True):
	# different to c's sprintf the template doesn't show what the var is
	# it shows what you want the var to be and sprintf will try to convert it
	ToReplace = __sprintf_regex.findall(string)
	assert len(ToReplace) == len(stuff), sprintf(
		"miss matched string template and value replacer len {i} != {i}",
		len(ToReplace),
		len(stuff),
	)
	if len(ToReplace) == len(stuff) or HideErrors:
		for i in r(ToReplace):
			if len(stuff) > i:
				replace = ToReplace[i]
				try:
					place = f"{(__sprintf_types[replace](stuff[i]))}"
				except ValueError:
					raise ValueError(
						sprintf(
							'\
can\'t convert "{s}" to {s}\
',
							str(stuff[i]),
							str(__sprintf_types[replace]),
						)
					)
				string = string.replace("{" + replace + "}", place, 1)
		return string
	else:
		raise TypeError(
			sprintf(
				"\
not as many replace arguments as string template arguments {i} to {i}",
				len(ToReplace),
				len(stuff),
			)
		)


def printf(string, *stuff, flush=True):
	string = sprintf(string, *stuff)
	stdout.write(string)
	if flush:
		stdout.flush()


def fprintf(FileHandler, string, *stuff):
	FileHandler.write(sprintf(string, *stuff))


def fprint(FileHandler, string):
	FileHandler.write(string)


def words(string: str) -> list[str]:
	return string.split()


def unwords(lst: list[str]) -> str:
	return " ".join(lst)


def IsBitSet(num, index):
	return num & 1 << index != 0


def BinarySearch(lst: list[int], item: int) -> int:
	"""
	Returns the position of item in the list if found, -1 otherwise.
	List must be sorted.
	"""  # is returing -1 a good idea?, it doesn't seem like one
	left = 0
	right = len(lst) - 1
	while left <= right:
		mid = (left + right) // 2
		if lst[mid] == item:
			return mid
		if lst[mid] > item:
			right = mid - 1
		if lst[mid] < item:
			left = mid + 1
	return -1


def FastSingleList(Listing: list[Any]) -> Any:
	ret = []
	for item in Listing:
		if type(item) == list:
			ret += FastSingleList(item)
		else:
			ret.append(item)
	return ret

@cache
def frpos(value, move): # 'fast' relative pos
	# move is defined by user
	return "\x1b[%i%c" % (value, move)

@cache
def rpos(y, x):  # relative pos func
	# y > 0 down
	if y < 0:
		ver = "A"
	else:
		ver = "B"
		y *= -1

	if x < 0:
		hor = "D"
	else:
		hor = "C"
		x *= -1
	ret = ""
	if x:
		ret += "\x1B[%i%c" % (abs(x), hor)
	if y:
		ret += "\x1B[%i%c" % (abs(y), ver)
	return ret
	# \x1b[<Value> prefix
	# up Y:		A
	# down Y:	B
	# forward X: C
	# backward X:D


# XMP stuff
_XMP_XMPVER: float = 0.3


def _XMP_Decode(filename: str, XmpCheck=True) -> dict[str, Any]:
	with open(filename, "r") as file:
		lcont: tuple[str, ...] = tuple(file.readlines())
	ncont: str = ""
	for i in r(lcont):
		# comments with '#'
		if TrimChar(TrimChar(lcont[i]), "\t", "")[0] == "#":
			continue
		if lcont[i][:-1]:
			ncont += TrimChar(TrimChar(lcont[i][:-1]), "\t", "")
	cont: str = ncont
	del ncont
	i = 0
	structure: dict[str, Any] = {}
	contnow: dict[str, Any] = {}
	condepth = []  # keep track of active conteiner tree
	contname = ""
	aliases: dict[str, Any] = {
		"null": None,
		"none": None,
		"true": True,
		"false": False,
	}

	while i < len(cont):
		char = cont[i]
		if char == "<":
			if contname:
				condepth.append((contname, contnow))
			ncontname = cont[i + 1 : i + str(cont[i:]).find(">")]
			if (
				contname
				and ncontname
				and ncontname[0] == "/"
				and ncontname[1:] != contname
			):
				raise WrongClosingName(
					"\n"
					f"can't close <{contname}> with <{ncontname}>\n"
					"container closer must be the same to container opener"
				)
			contname = ncontname
			if contname[0] == "/":	# contname end
				condepth.pop(-1)
				if condepth:
					_n, _c = contname[1:], contnow
					contname, contnow = condepth.pop(-1)
					contnow[_n] = _c
				else:
					structure[contname[1:]] = contnow
					## TODO
					## condepth can't be true right?
					# if condepth:
					#	contname, contnow = condepth.pop(-1)
					# else:
					#	contname = ""
					contname = ""
			else:  # real contname
				contnow = {}
		else:
			if char == "[":
				varname: str = cont[i + 1 : i + cont[i:].find(" ")]
				varval: str = cont[
					i
					+ 2
					+ len(varname) : i
					+ len(varname)
					+ str(cont[i + len(varname) :]).find("]")
				]  # help
				i += len(varname) + cont[i + len(varname) :].find("]")
				if contname:
					if varval[0] == "{" and varval[-1] == "}":
						if len(varval) == 2:
							contnow[varname] = []
						else:
							contnow[varname] = list(
								eval(varval[1:-1].replace("{", "[").replace("}", "]"))
							)
					else:
						contnow[varname] = eval(varval)
				else:
					if varval[0] == "{" and varval[-1] == "}":
						if len(varval) == 2:
							structure[varname] = []
						else:
							structure[varname] = list(
								eval(varval[1:-1].replace("{", "[").replace("}", "]"))
							)
					else:
						structure[varname] = aliases.get(varval, eval(varval))
		i += 1
	if structure["meta"]["xmpver"] != _XMP_XMPVER and XmpCheck:
		fprintf(
			stderr,
			"unmatched xmpver, file:{f} decoder:{f}\n",
			structure["meta"]["xmpver"],
			_XMP_XMPVER,
		)
	return structure


def _XMP_SEncode(structure: dict[str, Any], rl: int = 0) -> str:
	ret = ""
	rs = "\t" * rl
	for k in structure.keys():
		if isinstance(structure[k], dict):
			ret += f"{rs}<{k}>\n"
			ret += _XMP_SEncode(structure[k], rl + 1)
			ret += f"{rs}</{k}>\n"
		else:
			assert not isinstance(structure[k], set), "xmp can't store/load a set yet"
			if isinstance(structure[k], list):
				ret += f"{rs}[{k} {str(structure[k]).replace('[', '{').replace(']', '}')}]\n"
			if isinstance(structure[k], str):
				ret += f"{rs}[{k} \"{structure[k]}\"]\n"
			else:
				ret += f"{rs}[{k} {repr(structure[k])}]\n"
		if rl == 0:
			ret += "\n"
	return ret


def _XMP_Encode(filename: str, structure: dict[str, Any]):
	if "meta" not in structure.keys():
		structure["meta"] = {}
		structure["meta"]["xmpver"] = _XMP_XMPVER
	with open(filename, "w") as file:
		file.write(_XMP_SEncode(structure)[:-1])
		file.flush()


def UseXmp(filename: str, structure: Optional[dict[str, Any]] = None):
	if structure is not None:
		_XMP_Encode(filename, structure)
	else:
		return _XMP_Decode(filename)


# end of XMP stuff


class Window:
	def __init__(this, TopLeft: tuple[int, int], BottomRight: tuple[int, int]):
		# border points excluded from text out
		this.tl = TopLeft
		this.br = BottomRight
		this.t = TopLeft[0]
		this.l = TopLeft[1]
		this.b = BottomRight[0]
		this.r = BottomRight[1]
		this.y = this.t  # + t && < b
		this.x = this.l  # + l && > r
		#
		this.wprint = this.puts
		this.write = this.iputs
		this.print = this.iputs

	def printf(this, y, x, string, *args):
		this.wprint(y, x, sprintf(string, *args))

	def iprintf(this, string, *args):
		printf(string, *args)

	# edges
	def DrawEdges(this, char=RGB(0xFF, 0xFF, 0xA0) + "@" + COLOR.nc):
		# delete this later?
		DrawSpot(this.t, this.r, char)
		DrawSpot(this.t, this.l, char)
		DrawSpot(this.b, this.r, char)
		DrawSpot(this.b, this.l, char)
		this.mb()

	def DrawOuterEdges(this, char=RGB(0xFF, 0xFF, 0xA0) + "@" + COLOR.nc):
		# delete this later?
		DrawSpot(this.t - 1, this.l - 1, char)
		DrawSpot(this.t - 1, this.r + 1, char)
		DrawSpot(this.b + 1, this.l - 1, char)
		DrawSpot(this.b + 1, this.r + 1, char)
		this.mb()

	# borders
	def DrawBorders(this):
		DrawRectangle(this.tl, (this.br), COLOR.BkDarkGrey)
		this.mb()

	def DrawOuterBorders(this):
		DrawRectangle(
			(this.t - 1, this.l - 1), (this.b + 1, this.r + 1), COLOR.BkDarkGrey
		)
		this.mb()

	# moves
	def CheckMove(this, y, x):
		rs = ""
		# y
		if y > this.b:
			rs += f"\ny is bigger then window's bottom border {y} > {this.b}:\nWindow.[rs]move( {COLOR.red}>{y}<{COLOR.nc}, {x} )\n"
		elif y < this.t:
			rs += f"\ny is smaller then window's top border {y} > {this.t}:\nWindow.[rs]move( {COLOR.red}>{y}<{COLOR.nc}, {x} )\n"
		# x
		if x > this.r:
			rs += f"\nx is bigger then window's right border {y} > {this.r}:\nWindow.[rs]move( {y}, {COLOR.red}>{x}<{COLOR.nc} )\n"
		elif x < this.l:
			rs += f"\nx is smaller then window's left border {y} > {this.l}:\nWindow.[rs]move( {y}, {COLOR.red}>{x}<{COLOR.nc} )\n"
		if rs:
			raise ValueError("\n\nWindow class [rs]move call value error!\n" + rs)

	def mb(this):
		stdout.write(pos(this.y, this.x))

	def move(this, y, x):
		# non relative start at win border
		y += this.t
		x += this.l
		this.CheckMove(y, x)
		this.y = y
		this.x = x
		stdout.write(pos(y, x))

	# set move
	def smove(this, y, x):
		# non relative start at win border
		y += this.t
		x += this.l
		this.CheckMove(y, x)
		this.y = y
		this.x = x

	# relative
	def rmove(this, y, x):
		this.CheckMove(this.y + y, this.x + x)
		this.y += y
		this.x += x
		stdout.write(pos(y, x))

	# relative, set
	def rsmove(this, y, x):
		this.CheckMove(this.y + y, this.x + x)
		this.y += y
		this.x += x

	def putc(this, ch):
		stdout.write("%s%c" % (pos(this.y, this.x), ch))

	def puts(this, string):
		stdout.write("%s%s" % (pos(this.y, this.x), string))

	def iputc(this, ch):
		stdout.write(ch)

	def iputs(this, string):
		stdout.write(string)


def MeterToFoot(meter: float) -> float:
	return meter * 3.28084


def FootToMeter(foot: float) -> float:
	return foot * 0.3048


class Temperature:
	def CelsiusToFahrenheit(Celsius: float) -> float:
		return Celsius * 1.8 + 32

	CTF = CelsiusToFahrenheit

	def FahrenheitToCelsius(Fahrenheit: float) -> float:
		return (Fahrenheit - 32) / 1.8

	FTC = FahrenheitToCelsius

	def CelsiusToKelvin(Celsius: float) -> float:
		return Celsius - 273.15

	CTK = CelsiusToKelvin

	def KelvinToCelsius(Kelvin: float) -> float:
		return Kelvin + 273.15

	KTC = KelvinToCelsius

	def FahrenheitToKelvin(Fahrenheit: float) -> float:
		return CelsiusToKelvin(FahrenheitToCelsius(Fahrenheit))

	FTK = FahrenheitToKelvin

	def KelvinToFahrenheit(Kelvin: float) -> float:
		return CelsiusToFahrenheit(KelvinToFahrenheit(Kelvin))

	KTF = KelvinToFahrenheit

def OnDict(xmp:dict[Any, Any], path:Iterable[Any], AlwaysReturnFoud=False) -> tuple[int, Any]:
	# (dict tree, []PathToTake, ARF=False) -> (error index (0 = OK) , value)
	rn = xmp
	path = path.copy() # de-ref []Path
	r = 0
	if len(path) > 0:
		next = path.pop(0)
		if next in rn.keys():
			rn = xmp[next]
		else:
			if AlwaysReturnFoud:
				return r, rn
			return r, None
	while len(path):
		r += 1
		next = path.pop(0)
		if next in rn.keys():
			rn = rn[next]
		else:
			if AlwaysReturnFoud:
				return r, rn
			return r, None
		if len(path) == 0:
			return 0, rn
	else:
		return 0, rn


# )STUFF
# (CONSTS
class WrongClosingName(Exception):
	pass


def nop(*a, **b):
	pass


class noc:
	pass


class _c:
	def _m(this):
		pass


true = True
false = False
USER = _getlogin()
FuncType = type(nop)
NoneType = type(None)
Iterables = [list, set, frozenset]
Infinity = float("inf")
MethodType = type(_c._m)
ARGV = ArgvAssing(argv[1:])
Endl = "\n"
# )CONSTS

if __name__ == "__main__":
	for i in get("-r", "-c").list:
		exec(i)
	for i in get("-e", "").list:
		print(eval(i))
	# adapt cmd.py (lib) for this
	if get("--cli").exists:
		# python3.10, interactive mode, util lib imported
		ss("python3.10 -i -m util")
#!END

# funcs/classes
"""
include time
include json
include pickle
include os
include re
include functools
include time
include os.path
include typing
include random
include os
include sys
def cls log @ 104
def fct r @ 164
def cls timer @ 175
def fct MakeDict @ 206
def fct sleep @ 212
def fct pc @ 221
def fct even @ 224
def fct odd @ 227
def fct lst1 @ 230
def fct RngNoRepetition @ 238
def fct UseFile @ 248
def fct json @ 255
def fct GetInt @ 262
def fct GetFloat @ 277
def fct IsPrime @ 292
def fct fib @ 305
def cls rng @ 313
def fct print @ 357
def fct printl @ 371
def fct prints @ 381
def fct sprint @ 388
def fct input @ 391
def fct GCH @ 399
def cls COLOR @ 405
def fct SetColorMode @ 448
def fct PascalCase @ 458
def fct attrs @ 465
def fct SplitBracket @ 468
def fct StrToMs @ 479
def fct bhask @ 496
def fct near @ 504
def fct rsymb @ 517
def fct rchar @ 530
def fct GetWLen @ 534
def fct count @ 552
def fct timeit @ 565
def fct mmc @ 572
def fct factorial @ 590
def fct exit @ 596
def fct between @ 601
def fct ls @ 604
def fct rstr @ 607
def fct clear @ 621
def fct ANDGroups @ 624
def fct ORGroups @ 634
def fct XORGroups @ 640
def fct NOTGroups @ 652
def cls code @ 663
def cls BDP @ 691
def fct NumberToExponent @ 758
def fct rbool @ 763
def fct rcase @ 766
def fct EncryptS @ 781
def fct DecryptS @ 788
def fct AdvEncryptS @ 795
def fct AdvDecryptS @ 803
def fct numbers @ 813
def fct ShowTextGif @ 816
def fct JustDecimal @ 833
def fct NoDecimal @ 836
def fct number @ 839
def fct TimesInNumber @ 843
def fct NumSum @ 847
def fct FindAll @ 855
def fct DeepSum @ 866
def fct average @ 901
def fct mid @ 908
def fct IsIterable @ 925
def fct SingleList @ 928
def fct BiggestLen @ 940
def fct compare @ 943
def fct graphics @ 964
def fct pos @ 999
def fct ppos @ 1002
def fct ClearLine @ 1006
def fct ClearCollum @ 1014
def fct DrawHLine @ 1023
def fct DrawVLine @ 1030
def fct DrawSpot @ 1035
def fct ColorSpot @ 1038
def fct HideCursor @ 1041
def fct ShowCursor @ 1045
def fct DrawRectangle @ 1049
def fct ReplaceStringByIndex @ 1067
def cls TextBox @ 1070
def fct GetPrimeFactors @ 1174
def cls OStream @ 1186
def cls get @ 1192
def fct RmDir @ 1269
def fct TrimSpaces @ 1278
def fct Hamiltons @ 1283
def fct ReplaceAll @ 1286
def fct MakeString @ 1295
def fct IsListSorted @ 1314
def cls window @ 1317
def fct TestAll @ 1411
def fct TestAny @ 1418
def fct GetQuadrant @ 1425
def fct CursorMode @ 1435
def fct AdvTextBox @ 1687
def fct RGB @ 1695
def fct ArgvAssing @ 1698
def fct eprint @ 1716
def fct distance @ 1721
def fct DoAll @ 1725
def cls Filer @ 1728
def fct IsLeapYear @ 1764
def fct debugp @ 1777
def fct sprintf @ 1799
def fct printf @ 1822
def fct fprintf @ 1828
def fct fprint @ 1831
def fct words @ 1834
def fct unwords @ 1837
def fct IsBitSet @ 1840
def fct BinarySearch @ 1849
def fct nop @ 1872
def cls noc @ 1879
"""
