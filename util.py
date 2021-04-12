#! /usr/bin/python3.8

# util.py imports
from pickle import dump as _PickleDump, load as _PickleLoad
from json import dump as _JsonDump, load as _JsonLoad

# general imports
from random import randint as rint, choice as ritem
from time import time as tm, sleep as slp , strftime as __ftime__
from sys import argv,exit as exi, getsizeof as sizeof, stdout as sout
from os import getcwd as pwd, system as ss, chdir as cd, listdir as _ls,getenv
from os.path import isfile,exists


USER = getenv("USER")
FuncType = type(lambda a:a )
NoneType = type(None)
iterables = [type(list),type(set),type(frozenset)]
class NumberTooBigError(BaseException):pass

class log:
	def __init__(self,sep=', ',tm=True,file="log"):
		self.tm = tm
		self.sep = sep
		self.LOG = []
		self.add('the log was created')
		self.file = file
	def add(self,*ask) -> None:
		tm = self.tm
		ask=self.sep.join([str(ak) for ak in ask])

		tme = ''
		if tm:tme = f'at {__ftime__("%D %H:%M:%S")} : '
		self.LOG.append(f'{tme}{ask}')

	def remove(self,index_or_content:int or str) -> None:
		if type(index_or_content) == int:
			return self.LOG.pop(index_or_content)
		else:
			self.LOG.index(index_or_content)
			return self.LOG.pop(index_or_content)
		raise ValueError
	def __repr__(self) -> str:
		return f'{self.LOG}'

	def get(self,num:int) -> str:
		return self.LOG[num]

	def __getitem__(self,num:int) -> str:
		return self.LOG[num]

	def __call__(self) -> list:
		return self.LOG

	def __iter__(self) -> None:
		for i in self():
			yield i

	def show(self) -> None:
		for i in self:
			print(i)

	def save(self) -> None:
		with open(self.file,'w') as save_file_log:
			for i in self.LOG:
				save_file_log.write(f'{i}\n')


# _log = log()

# formating:
# _log.add(f'[func or class] ([name]) = [{,} args] => [return]')

# e.g.:
# _log.add(f'func (r) = {end , start, jmp} => range')

def r(end:object,start:int=0,jmp:int=1):
	# _log.add(f'func (r) = {end , start, jmp} => yield')
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

def AssureType(value:object,types:type,err:bool=True,ErrorMsg=None) -> TypeError or bool:
	# _log.add(f'func (AssureType) = {values , types, err} => TypeError or bool')
	if type(types) != type and type(value) == type:
		value,types = types,value

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
	def __init__(self,auto:bool=True):
		# _log.add(f'class (timer.__init__) = {auto} ')
		self.markers = []
		if auto:self.st = tm()

	def start(self):
		# _log.add(f'class (timer.start) = None => None')
		self.st = tm()

	def mark(self):
		# _log.add(f'class (timer.mark) = None => None')
		self.markers.append(self.get())

	def marks(self) -> list:
		# _log.add(f'class (timer.marks) = None => list')
		return self.markers

	def get(self) -> float:
		# _log.add(f'class (timer.get) = None => float')
		return tm() - self.st

	def __call__(self) -> float:
		# _log.add(f'class (timer()) => float')
		if not self.st:
			self.st = tm()
		else:
			return self.get()

	def __iter__(self) -> iter:
		# _log.add(f'class (for i in timer) => yield marks[i]')
		for i in self.markers:
			yield i

	def __repr__(self) -> str(float):
		# _log.add(f'class (timer) -> __repr__ ')
		return f'{self.get}'

def MakeDict(ls1:list or set,ls2:list or set) -> dict:
	# _log.add(f'func (make_dict) with {ls1,ls2}')
	'''
	return a dictionary with ls1 as key and ls2 as result
	will return None if lenght ls1 != lenght of ls2
	'''
	ls1=list(ls1)
	ls2=list(ls2)
	if len(ls1) != len(ls2):
		return None
	ret_dict = dict('')
	for i in r(ls1):
		ret_dict[ls1[i]] = ls2[i]
	return ret_dict

def sleep(seg:float=0,sec:float=0,ms:float=0,min:float=0,hour:float=0,day:float=0) -> None:
	# _log.add(f'func (sleep) with {seg , min , hour , day}')
	slp(ms/1000+seg+sec+min*60+hour*3600+day*86400)

def pc(x:int,y:int) -> float:
	# _log.add(f'func (pc) with {x , y}')
	return int(x/100*y)

def even(var:int) -> bool:
	# _log.add(f'func (even) with ({var})')
	return not var%2

def RngNoRepetition(v_min:int,v_max:int,how_many:int=1) -> list:
	'''
	if how_many is bigger or equal to v_max
	this function will return None
	'''
	# _log.add(f'func (rng_n_rep) with {v_min , v_max , how_many}')
	if how_many>=v_max:
		return None
	ret_list,tmp=[],[x+1 for x in range(v_min,v_max)]
	for _ in r(how_many):
		ret_list.append(tmp.pop(rint(v_min,len(tmp))))
	return ret_list

def UseFile(file:str,mode:str,obj=None) -> object or None:
	"""pickled file btw"""
	# _log.add(f'func ( use_file ) with {file , mode , obj}')
	if mode[-1] != 'b':
		mode+='b'

	if obj == None:
		return _PickleLoad(open(file,mode))
	else:
		_PickleDump(obj,open(file,mode))

def json(file:str,obj:object=None) -> dict or None:
	# _log.add(f'func (js) with {file , obj}')
	if obj == None:	return _JsonLoad(open(file))
	else:_JsonDump(obj, file)

def GetInt(msg:str,end='\n') -> int:
	'''
	will return an integer by inputing a string with {msg , end}
	and converting it to int
	if the user enters an invalid input the function will restart
	'''
	# _log.add(f'func (get_int) with {msg , end}')
	x=input(f'{msg}{end}')
	try:
		y=int(x)
		return y
	except ValueError:
		GetInt(msg,end)

def GetFloat(msg:str,end='\n') -> float:
	'''
	will return an float by inputing a string with {msg , end}
	and converting it to int
	if the user enters an invalid input the function will restart
	'''
	# _log.add(f'func (get_float) with {msg , end}')
	x=input(f'{msg}{end}')
	try:
		y=float(x)
		return y
	except ValueError:
		GetFloat(msg,end)

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

def case(var:int or float,index:int) -> str:
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
	def new(self):
		# _log.add(f'class (rng) -> new prop')
		self.var = []
		for _ in range(self.size):
			self.var.append(rint(self.mn,self.mx))
		return self.var

	def get(self):
		# _log.add(f'class (rng) -> get prop')
		self.var = []
		for _ in range(self.size):
			self.var.append(rint(self.mn,self.mx))
		return self.var

	def __init__(self,mn,mx,size=1):
		# _log.add(f'class (rng) -> __init__ with {self,mn,mx,size}')
		self.size=size
		self.mn=mn
		self.mx=mx
		self.new

	def __repr__(self):
		# _log.add(f'class (rng) -> __repr__')
		if len((var:=self.var))==1:
			var=self.var[0]
		self.new
		return f'{var}'

	def NewSize(self,size):
		# _log.add(f'class (rng) -> new_size with ({size})')
		self.size=size
		self.new

	def NewMin(self,mn):
		# _log.add(f'class (rng) -> new_min with {self,mn}')
		self.mn=mn
	def NewMax(self,mx):
		# _log.add(f'class (rng) -> new_max with {self,mx}')
		self.mx=mx

	def __call__(self):
		return self.get()

def print(*msg,end='\n'):
	# if type(msg)
	# try:
		# b=any([i.__print__(end,rep=False) for i in msg if type(i) == var])
		# if b:return
	# except NameError:pass

	try:
		if len(msg) == 1:
			msg = msg[0]
		if len(msg) == 0:
			msg = ''
	except TypeError:pass

	sout.write(f'{msg}{end}')

	# return f'{msg}{end}'

# start of chaos

def encpt(string:str,fm:str,tm:str):
	# _log.add(f'func (encpt) with {string , fm , tm}')
	string = list(string)
	dif = ord(fm) - ord(tm)
	for s in r(string):
		string[s]=chr( ord( string[s] ) + dif )
	return ''.join(string)

def decpt(string:str,fm:str,tm:str):
	# _log.add(f'func (decpt) with {string , fm , tm}')
	return encpt(string,tm,fm)

# end of chaos (pt 1)

def index(ls:list,var,many=False) -> list:
	# _log.add(f'func (index) with {ls , var , many}')
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

#bash colors
#\/ \/ \/ \/
#
color={
	'nc':'\033[0m'
	,'white':'\033[0m'
	,'black' : '\033[0;30m'
	,'red' : '\033[0;31m'
	,'green' : '\033[0;32m'
	,'yellow' : '\033[0;33m'
	,'blue' : '\033[0;34m'
	,'magenta' : '\033[0;35m'
	,'cyan' : '\033[0;36m'
	,'light gray' : '\033[0;37m'
	,'light grey' : '\033[0;37m'
	,'dark gray' : '\033[0;90m'
	,'dark grey' : '\033[0;90m'
	,'light red' : '\033[0;91m'
	,'light green' : '\033[0;92m'
	,'light yellow' : '\033[0;93m'
	,'light blue' : '\033[0;94m'
	,'light magenta' : '\033[0;95m'
	,'light cyan' : '\033[0;96m'
	,'br gray' : '\033[0;37m'
	,'br grey' : '\033[0;37m'
	,'br red' : '\033[0;91m'
	,'br green' : '\033[0;92m'
	,'br yellow' : '\033[0;93m'
	,'br blue' : '\033[0;94m'
	,'br magenta' : '\033[0;95m'
	,'br cyan' : '\033[0;96m'
}

#fish basic color list
#\/ \/ \/ \/
#black
#red
#green
#yellow
#blue
#magenta
#cyan
#white
#brblack
#brred
#brgreen
#bryellow
#brblue
#brmagenta
#brcyan
#brwhite
#normal


def SplitBracket(string:str,bracket:str,closing_bracket=''):
	# _log.add(f'func (split_bracket) with {string , bracket , closing_bracket}')

	if closing_bracket == '':
		r = {
		'(':')'
		,'[':']'
		,'{':'}'
		}
		closing_bracket = r[bracket]
	# "[](){}" bracket = '(' => ["[]","){}"] => "[])){}" => ["[]","{}"]
	# don't touch it! (i don't know HOW it works, but it works)
	return closing_bracket.join(str(string).split( bracket )).split(closing_bracket)

def StrToMs(ipt):
	# _log.add(f'func (str_to_ms) with ({ipt})')
	ipt=ipt.split()
	n,ipt = float(ipt[0]),ipt[1]
	TypesToStr = {
	tuple(["years","year","yrs","yr","ys",'y']):220903200000,
	tuple(["weeks","week","w"]):604800000,
	tuple(["days","day",'d']):86400000,
	tuple(['hours','hour','hrs','hr','h']):3600000,
	tuple(['minutes','minute','mins','min','m']):60000,
	tuple(['seconds','second','secs','sec','s']):1000,
	tuple(['milliseconds','millisecond','msecs','msec','ms']):1
	}
	for i in TypesToStr.keys():
		if ipt in i:
			return n*TypesToStr[i]
	return None

def FindAll(string:str,char:str) -> str:
	# _log.add(f'func (remove_all) with {string,char}')
	ret = []
	for i in r(string):
		if char == string[i]:
			ret.append(i)
	return ret

# chaos (pt 2)

# def adv_encpt_file(encpt_key:str,file:str,bin:bool=False) -> open:
# 	# _log.add(f'func ( adv_encpt ) with {encpt_key , file}')
# 	if not bin:
# 		with open(file,'r') as fl:
# 			a = list(fl.readlines())
# 	else:
# 		a = list(UseFile(file,'rb'))

# 	for j in r(a):
# 			for i in encpt_key:
# 				a[j] = encpt(a[j],i,'a')
# 	return a

# def adv_decpt_file(encpt_key:str,file:str,bin:bool=False) -> open:
# 	# _log.add(f'func ( adv_encpt ) with {encpt_key , file}')
# 	if not bin:
# 		with open(file,'r') as fl:
# 			a = list(fl.readlines())
# 	else:
# 		a = list(UseFile(file,'rb'))
# 	for j in r(a):
# 		for i in encpt_key:
# 			a[j] = decpt(a[j],i,'a')
# 	return a

# def adv_encpt_str(key:str,string):
# 	# _log.add(f'func ( adv_encpt_str ) with {key , string}')
# 	for i in key:
# 		string = encpt(string,'a',i)
# 	return string

# def adv_decpt_str(key:str,string):
# 	# _log.add(f'func ( adv_decpt_str ) with {key , string}')
# 	for i in key:
# 		string = encpt(string,i,'a')
# 	return string

# # end of chaos (pt 2)

def bhask(a,b,c):
	# _log.add(f'func ( bhask ) with {a,b,c}')
	delt = ((b**2) - (4*a*c))**.5
	b*=-1
	a*=2
	x = (b + delt)/a
	y = (b - delt)/a
	return x,y

def near(base:float or int,num:float or int,dif_up:float or int,dif_down:float or int=None) -> bool:
	# _log.add(f'func ( near ) with {base,num,dif_up,dif_down}')
	if dif_down == None:dif_down = dif_up
	return base+dif_up >= num >= base-dif_down

def lst1(lst:object) -> object:
	# _log.add(f'func ( lst1 ) with ({lst})')
	if len(lst) == 1:
		return lst[0]
	return lst

# chaos (pt 3)

# def adv_encpt2(key,string,_jam='p',_k=0):
# 	'''
# 	how to use adv_encpt2 / adv_decpt2

# 	key = rchar(30)
# 	print(''.join(key))
# 	j='542953510102865'
# 	j=adv_encpt2(key,j)
# 	print(f'result: {j}')
# 	j=adv_decpt2(key,j)
# 	ss('clear')
# 	print(f'result: {j}')
# 	'''

# 	# _log.add(f'funct ( adv_encpt2 ) with {key , string , _jam , _k}')
# 	if len(key) == _k:return 1
# 	if _jam == 'p':
# 		j = 'p'
# 		_jam = 'n'
# 	else:
# 		j='n'
# 		_jam = 'p'
# 	k = key[_k]

# 	if j == 'n':
# 		s=''.join([encpt(string,k,'a')])
# 	elif j == 'p':
# 		s=''.join([encpt(string,'a',k)])

# 	x=adv_encpt2(key,s,_jam=_jam,_k=_k+1)
# 	if x == 1:return s
# 	return x

# def adv_decpt2(key,string,_jam='p',_k=0):
# 	# _log.add(f'funct ( adv_decpt2 ) with {key , string , _jam , _k}')
# 	key=key[::-1]
# 	return adv_encpt2(key,string,_jam=_jam,_k=_k)

# # end of chaos (pt 3)

def rsymb(size=1):
	# _log.add(f'funct ( rsymb ) with ({ size })')
	#33-47 58-64 160-191
	c=[]
	for _ in r(size):
		tp = rint(1,3)
		if tp == 1:
			c.append(chr(rint(33,47)))
		elif tp == 2:
			c.append(chr(rint(58,64)))
		else:
			c.append(chr(rint(160,191)))
	return lst1(c)

def rchar(size=1):
	# _log.add(f' funct ( rchar ) with ({ size })')
	#65-90 97-122
	return lst1([(chr(rint(65,90))) if rint(0,1) else (chr(rint(97,122))) for char in r(size)])

printf=print

def GetWLen(msg:str,ln:int,end:str='\n') -> int:
	AssureType(int,ln,ErrorMsg=f"lengh type != int \n {ln} of type {type(ln)} != int")
	'''
	will return an str by inputing a string with {msg , end}
	if the user enters an invalid input the function will restart
	the valid input has the same size as ln
	snippet:
	len(input) == ln
		ret
	else
		restart
	'''
	# _log.add(f'func (get_w_len) with {msg , end}')
	x=input(f'{msg}{end}')
	if len(x) == ln:
		return x
	else:
		GetWLen(msg,ln,end)

def CallWExcept(funct:FuncType,excpts:BaseException,*args:object,call:bool=False,call_f:bool=None) -> object:
	# _log.add(f'func ( call_w_except ) with {funct , excpts , *args , call , call_f }')
	x = funct(*args)
	if x in excpts:
		if call:
			call_f()
		else:
			CallWExcept(funct,excpts,*args)
	else:
		return x

def count(end:object,start:int=0,jmp:int=1):
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

def mmc(a:int,b:int) -> int:
	AssureType(int,a,ErrorMsg=f"a : {a} != int")
	AssureType(int,b,ErrorMsg=f"b : {b} != int")
	# _log.add(f'func ( mmc/lcm ) with {a , b}')
	greater = max(a,b)
	s = tm()
	for i in count(0):
		G = greater+i
		if not G % a and not G % b:break
		if tm()-s>len(f"{greater}")*2:raise Exception('timed out')
	return G

lcm = mmc

def fact(n:int) -> int:
	# _log.add(f'func ( fact ) with {n}')
	Fact = 1
	for i in range(1,n+1):
		Fact*=i
	return Fact

def argv_assing(argvs:iter) -> dict:
	'''
	this function will loop through all argvs, and will define the ones starting with - as indicators
	and the others just normal arguments
	the returning value will be a dictionary like this:
	argv = ['-i','input','input2','-o','output','output2']
	{'-i':['input','input2],'-o':['output','output2']}
	'''
	# _log.add(f'func ( argv_assing ) with {argvs}')
	indcn=[]
	ret={}
	for i in r(argvs):
		if str(argvs[i])[0] == '-':
			indcn.append(i)

	if indcn == [] and argvs != []:
		ret[None] = argvs

	elif indcn == []:
		ret[None] = []

	elif indcn[0] > 0:
		ret[None] = argvs[0:indcn[0]]


	for i in r(indcn):
		try:
			dif = indcn[i+1]-indcn[i]
			add = argvs[indcn[i]:indcn[i]+dif][1:]
			for AddIndex in r(add):
				add[AddIndex] = add[AddIndex].replace("/-",'-')
			ret[argvs[indcn[i]:indcn[i]+dif][0]] = add#argvs[indcn[i]:indcn[i]+dif][1:]
		except IndexError:
			add = argvs[indcn[i]+1:]
			for AddIndex in r(add):
				add[AddIndex] = add[AddIndex].replace("/-",'-')
			ret[argvs[indcn[i]]] = add#argvs[indcn[i]+1:]
	return ret

ArgvAssing = argv_assing

class time:
	@property
	def sec(self):
		# _log.add(f'class ( time ) -> sec')
		return __ftime__(f"%S")

	@property
	def min(self):
		# _log.add(f'class ( time ) -> min')
		return __ftime__(f"%M")

	@property
	def hour(self):
		# _log.add(f'class ( time ) -> hour')
		return __ftime__("%H")

	@property
	def day(self):
		# _log.add(f'class ( time ) -> day')
		return __ftime__("%D").split('/')[1]

	@property
	def month(self):
		# _log.add(f'class ( time ) -> month')
		return __ftime__("%D").split('/')[0]

	@property
	def year(self):
		# _log.add(f'class ( time ) -> year')
		return __ftime__("%D").split("/")[2]

try:
	import gi
	gi.require_version('Notify', '0.7')
	from gi.repository import Notify
	class notify:
		def __init__(self,title:str="",body:str="",instant:bool=False,name:str="GNOME-notify-class util.py"):
			# _log.add(f'class ( notify ) -> {title , body , instant , name}')
			Notify.init(name)
			if title or body:
				self.notf=Notify.Notification.new(str(title),str(body))
				if instant:
					self.notf.show()
			else:
				self.notf=Notify.Notification.new("","")
		def new(self,title,body,instant=False):
			self.notf=Notify.Notification.new(str(title),str(body))
			return self
		def __call__(self):self.notf.show()
		def __repr__(self):return f'{self.notf}'
		def show(self):self()

except ImportError:
	if '--debug' in argv:
		NotifyError = f'{color["red"]}[{color["yellow"]}WARNING{color["red"]}]{color["nc"]} notify won\'t work without python 3.8'

def exit(num:int=1) -> None:
	# _log.add(f'class ( exit ) = ({num}) => act')
	AssureType(int,num,ErrorMsg=f'var {num} of wrong type, should be int')
	if num < 256:
		exi(num)
	else:
		raise NumberTooBigError(f'exit num : {num} > 255')

def between(x:float or int,min:float or int,max:float or int) -> bool:
	return min < x < max

def ls(dir='.') -> list:
	return [i if isfile(f'{dir}/{i}') else f"{i}/" for i in _ls(dir)]

def rstr(ln:int,chars:bool=True,symbs:bool=True,ints:bool=True,intmin:int=0,intmax:int=9) -> str:
	ret = []
	for _ in r(ln):
		fs = []
		if chars:fs.append(rchar)
		if symbs:fs.append(rsymb)
		if ints:fs.append(rint)
		f = ritem(fs)
		if f == rint:
			ret.append(f(intmin,intmax))
		else:
			ret.append(f())
	return ''.join([str(a) for a in ret])

def clear() -> None:
	ss("clear")

cls = clear

Clean = clear

def ln(val,lenght,start=0):
	if type(val) in [int,float]:
		val = f"{val}"
	val = val[start:lenght]
	if len(val) > lenght:
		val+=" "*len(val-lenght)
	return val

def inrange(num:int,lis:list) -> bool:
	return num < len(lis)

def ANDGroups(g1:set or list or frozenset,g2:set or list or frozenset):
	G1 = set(g1)
	G2 = set(g2)
	Gall = *g1,*g2
	Gret = set()
	for i in Gall:
		if i in G1 and i in G2:
			Gret.add(i)
	return Gret

def ORGroups(g1:set or list or frozenset,g2:set or list or frozenset):
	Gret = set((*g1,*g2))
	return Gret

def XORGroups(g1:[set , list , frozenset],g2:[set , list , frozenset]):
	G1 = set(g1)
	G2 = set(g2)
	Gall = *g1,*g2
	Gret = set()
	for i in Gall:
		if i in G1 + i in G2 == 1:
			Gret.add(i)
	return Gret

def NOTGroups(g1:[set, list, frozenset],g2:[set, list, frozenset]):
	G1 = set(g1)
	G2 = set(g2)
	Gret = set()
	for i in G1:
		if not i in G2:
			Gret.add(i)
	return Gret

class code:
	def __init__(self,name="test",mode="exec",code=[]):
		self.name,self.mode,self.code = name,mode,code

	def __add__(self,line):
		self.code.append(line)
		return code(self.name,self.mode,self.code)

	def __call__(self):
		if type(self.code) == str:self.code=self.code.split('\n')
		for line in self.code:
			exec(compile(line,self.name,self.mode))

	def __repr__(self):
		msg = ""
		if type(self.code) == str:self.code=self.code.split('\n')
		if len(self.code) > 1:
			for line in self.code:
				msg+=f"{line}\n"
		else:
			msg = f"{self.code[0]}"
		return msg

class var(object):
	'''
	this class should NOT be used for items in iterables!

	this class "contains" the other classes in it,
	so you can stop worring about doing this foo=DoShit(foo,args),
	and start doing this foo.DoShit(args)
	'''
	def __init__(self,Value:object,Type:type=None,PrintMutipleLines=True):
		if type(Value) == type and type(Type) != type:
			Value,Type = Type,Value

		if Type == None:Type=type(Value)

		self.Type = Type
		self.Value = Value
		self.PrintMutipleLines=bool(PrintMutipleLines)
		
		Types = {
			(float,int):"IsNumber",
			(list,set,str):"IsIterable",
			(str,):"IsString",
			(frozenset,):"IsFrozenset",
			(dict,):"IsDict"
		}

		for i in types.keys():
			if self.Type in i:
				exec(f"self.{types[i]} = True")
			else:
				exec(f"self.{types[i]} = False")

		# self.IsNumber = self.Type in [float,int]
		# self.IsIterable = self.Type in [list,set,str]
		# self.IsString = self.Type in [str]
		# self.IsFrozenSet = self.Type in [frozenset]
		# self.IsDict = self.Type in [dict]

	# math shit start



	def __add__(self,add):
		try:
			return self.Value.__add__(add)
		except Exception:pass
		# var + var
		ReturnVar = None
		if type(add) == var:add=add.Value

		# frozen set is frozen set!
		if self.IsFrozenSet:
			raise TypeError

		# var != dict
		if not self.IsDict:
			if self.IsIterable:
				ReturnVar = self.Type(ORGroups(self.Value,add))
			else:
				ReturnVar = self.Value+add

		# var = dict
		elif self.IsDict:
			ret = self.Value
			for i in add.keys():
				ret[i] = add[i]
			ReturnVAr =  var(self.Type,ret)
		return var(ReturnVar,PrintMutipleLines=self.PrintMutipleLines)

	def __sub__(self,add):
		# var - var
		ReturnVar,ReturnType = None,self.Type
		if type(add) == var:add=add.Value

		# var != dict
		if not self.IsDict:
			if self.IsIterable:
				ReturnVar = self.Type(NOTGroups(self.Value,add))
			else:
				ReturnVar = self.Value-add

		# var == dict
		else:
			ret = self.Value
			retK = ret.keys()
			if type(add) == dict:
				for i in add.keys():
					del ret[i]
			else:
				for i in add:
					del ret[i]
			ReturnVar = ret

		# return var obj of same type and (probably) different value
		return var(ReturnVar,PrintMutipleLines=self.PrintMutipleLines)

	def __mul__(self,add):
		if type(add) == var:add=add.Value

		if self.IsNumber:
			return var(self.Value * add,PrintMutipleLines=self.PrintMutipleLines)
		else:
			raise WrongType(f"var class can't multiply {self.Value} with {add}")

	def __truediv__(self,add):
		if type(add) == var:add=add.Value

		if self.IsNumber:
			return var(self.Value / add,PrintMutipleLines=self.PrintMutipleLines)
		else:
			raise WrongType(f"var class can't divide {self.Value} with {add}")

	def __floordiv__(self,add):
		if type(add) == var:add=add.Value

		if self.IsNumber:
			return var(self.Value // add,PrintMutipleLines=self.PrintMutipleLines)
		else:
			raise WrongType(f"var class can't (floor) divide {self.Value} with {add}")

	# math shit done
	# list/dict stuff start

	def __iter__(self):
		for i in self.Value:
			yield i

	# calling method
	def __getitem__(self,index_or_content):
		if type(index_or_content) == var:index_or_content = index_or_content.Value
		ret = self.Value[index_or_content]
		if type(ret)!=var:
			ret = var(ret,PrintMutipleLines=self.PrintMutipleLines)
		return ret

	# list/dict stuff done
	# (other) magic methods start

	def dict(self,lst:list):
		return var(MakeDict(self.Value,lst),PrintMutipleLines=self.PrintMutipleLines)

	def __dict__(self,lst:list):
		return var(MakeDict(self.Value,lst),PrintMutipleLines=self.PrintMutipleLines)

	def __len__(self):
		if self.IsDict:
			return len(self.Value.Keys())
		return len(self.Value)

	def __r__(self,start: int=0  ,jmp: int=1):
		return range(start,len(self.Value),jmp)

	def __setitem__(self, index, obj):
		if self.IsFrozenSet:
			raise TypeError(f"can't set value of FrozenSet\nvalue:{self.Value}")
		if self.IsString:
			ret = list(self.Value)
			ret[index] = obj
		else:
			ret = [self.Value]
			ret[index] = obj
		
		self.Value = ret


	def __repr__(self):
		msg = ''
		if self.IsIterable and not self.IsString:
			for thingIndex in r(self.Value):
				thing = self.Value[thingIndex].__repr__()
				# if type(thing).find("__main__.") != -1:
					# TypeMsg = f"{type(thing)}".split("__main__.")[1]
				# else:
				TypeMsg = f'{type(thing)}'.split('\'')[1]
				if self.PrintMutipleLines:
					msg += f"{thingIndex} : {TypeMsg} : {thing}\n"
				else:
					msg += f"{TypeMsg}: {thing}, "
			msg = msg[:-1]
		else:
			# if f"{type(self.Value)}".find("__main__.") != -1:
				# TypeMsg = f"{type(self.Value)}".split("__main__.")[1][:-2]
			# else:
			TypeMsg = f'{self.Type}'.split('\'')[1]
			if self.IsString:
				msg+=f"{TypeMsg} : {''.join(self.Value)}"
			else:
				msg += f"{TypeMsg} : {self.Value}"

		return msg

	# magic methods done
	# complex methods start

	def split(self,string:str=None):
		if type(string) == var:string = string.Value
		if string == None:
			ret = self.Value.split()
		else:
			ret = self.Value.split(string)

		if type(ret)!=var:
			ret = var(ret,PrintMutipleLines=self.PrintMutipleLines)
		return ret

	def join(self,string:str or var):
		if type(string) == var:string = string.Value
		ret = ""
		if self.IsIterable:
			for thing in self.Value:
				if type(thing) == var:
					ret+=f"{string}{thing.Value}"
				else:
					ret+=f"{string}{thing}"

			ret = ret[1:]
			if type(ret)!=var:
				ret = var(ret,PrintMutipleLines=self.PrintMutipleLines)
			return ret
		else:
			raise TypeError(f"\n{var} is not iterable")

	def SplitBracket(self,bracket,ClosingBracket="default"):
		if type(bracket) == var:bracket = bracket.Value
		if type(ClosingBracket) == var:ClosingBracket = ClosingBracket.Value

		# AssureType(self.Value,str)

		if ClosingBracket == "default":
			ret = SplitBracket(self.Value,bracket)
		else:
			ret = SplitBracket(self.Value,bracket,ClosingBracket)
		if type(ret)!=var:
			ret = var(ret,PrintMutipleLines=self.PrintMutipleLines)
		return ret


	def keys(self):
		return list(self.Value.keys())

	def index(self,IndexOrContent:object):
		ret = None
		if self.IsIterable:
			ret = self.Value.index(IndexOrContent)
		elif self.IsDict:
			mkdict = {}
			for i in self.keys():
				mkdict[self[i]] = i
			ret = mkdict[IndexOrContent]

		else:
			raise TypeError(f"{self} is not iterable or dictionary")
		if type(ret)!=var:
			ret = var(ret,PrintMutipleLines=self.PrintMutipleLines)
		return ret

	def copy(self):
		return var(self.Value,PrintMutipleLines=self.PrintMutipleLines)

	def pop(self,index):
		return var(self.Value.pop(index),PrintMutipleLines=self.PrintMutipleLines)

	# complex methods done


class BDP:
	def __init__(this,name):
		# for unix like system

		if not exists(f"/home/{USER}/BDP"):
			ss("mkdir /BDP/")

		if not name.startswith("~/BDP/"):
			name = f"~/BDP/{name}"
		if not name.endswith(".bdp"):
			name = f"{name}.bdp"

		name = name.replace("//",'/')
		name = name.replace('~',f"/home/{USER}")

		this.name = name
		this.data = None


	def save(this,data=None):
		if data == None:
			data = this.data

		if not exists(f"{this.name}"):
			ss(f"touch {this.name}")

		UseFile(this.name,'w',data)

	def load(this,file=None):
		if file == None:
			file = this.name
		this.data = UseFile(file,'r')
		return this.data

	def __repr__(this):
		if len(f"{this.data}") < 40:
			return f"name: {this.name}\ndata: {this.data}"
		else:
			return f"name: {this.name}\n{color['yellow']}data: data too big{color['nc']}"

def MessageMid(msg,WindoLen,OffsetChar=' '):
	off = OffsetChar*(WindoLen//2)
	return f"{off}{msg}{off}"


def NumberToExponent(number):
	smol = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','.':'.'}

	ret = ''.join([smol[i] for i in str(number)])
	return ret

# funcs/classes
'''
	type = FuncType
	type = NoneType
	list = iterables
	class NumberTooBigError
	class log
	func( AssureType)
	func( r)
	class timer
	func( make_dict)
	func( sleep)
	func( pc)
	func( even)
	func( odd)
	func( rng_n_rep)
	func( use_file)
	func( js)
	func( is_prime)
	func( case)
	func( fib)
	class rng
	func( print)
	func( muid)
	func( encpt)
	func( decpt)
	func( index)
	class color
	func( split_bracket)
	func( any_str_in_list)
	func( remove_all)
	func( adv_encpt_file)
	func( adv_decpt_file)
	func( adv_encpt_str)
	func( adv_decpt_str)
	func( bhask)
	func( near)
	func( lst1)
	class const
	func( adv_encpt2)
	func( adv_decpt2)
	func( rsymb)
	func( rchar)
	func( ritem)
	func( get_w_len)
	func( call_w_except)
	func( mmc)
	func( lcm)
	func( fact)
	func( argv_assing)
	class time
	class notify
	func( exit)
	func( between)
	func( ls)
	func( rstr)
	func( clear)
	func( ln)
	func( inrange)
	func( ANDGroups)
	func( ORGroups)
	func( XORGroups)
	class code
	class var
	class BDP
	func( mid)
	func( MessageMid)
'''

if __name__ == "__main__":
# 	for i in r(argv,1):
# 		if i == "pass" or i == "":continue
# 		print(f'q{i}: {argv[i]}')
# 		try:
# 			print(f'a{i}: {eval(argv[i])}')
# 		except Exception as f:print(f'{color["red"]}ERR: {f}{color["nc"]}')
# 		print('\n')
	exit(0)
