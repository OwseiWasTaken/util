#! /usr/bin/python3.9

# util.py imports
from pickle import dump as _PickleDump, load as _PickleLoad, dumps as PickleString, loads as UnpickleString
from json import dump as _JsonDump, load as _JsonLoad
from tty import setraw
from termios import tcgetattr , tcsetattr , TCSADRAIN , TIOCGWINSZ
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

# general imports
from random import randint as rint, choice as ritem
from time import time as tm, sleep as slp , strftime as __ftime__
from sys import argv,exit as exi, getsizeof as sizeof, stdout as sout, stdin as sin
from os import getcwd as pwd, system as ss, chdir as cd, listdir as _ls,getenv
from os.path import isfile,exists
from fcntl import ioctl
from struct import pack, unpack

USER:str = getenv("USER")
FuncType:type = type(lambda a:a )
NoneType:type = type(None)
iterables:list = [type(list()),type(set()),type(frozenset())]
class NumberTooBigError(BaseException):pass
infinity:float = float("inf")

class log:
    def __init__(this,sep=', ',tm=True,file="log"):
        this.tm = tm
        this.sep = sep
        this.LOG = []
        this.add('the log was created')
        this.file = file
    def add(this,*ask) -> None:
        tm = this.tm
        ask=this.sep.join([str(ak) for ak in ask])

        tme = ''
        if tm:tme = f'at {__ftime__("%D %H:%M:%S")} : '
        this.LOG.append(f'{tme}{ask}')

    def remove(this,index_or_content:int or str) -> None:

        if type(index_or_content) == int:
            return this.LOG.pop(index_or_content)
        else:
            this.LOG.index(index_or_content)
            return this.LOG.pop(index_or_content)
        print("no such value sa index or content")
        exit(1)
        # raise ValueError
    def __repr__(this) -> str:
        return f'{this.LOG}'

    def get(this,num:int) -> str:
        return this.LOG[num]

    def __getitem__(this,num:int) -> str:
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
        with open(this.file,'w') as save_file_log:
            for i in this.LOG:
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
    def __init__(this,auto:bool=True):
        # _log.add(f'class (timer.__init__) = {auto} ')
        this.markers = []
        if auto:this.st = tm()

    def start(this):
        # _log.add(f'class (timer.start) = None => None')
        this.st = tm()

    def mark(this):
        # _log.add(f'class (timer.mark) = None => None')
        this.markers.append(this.get())

    def marks(this) -> list:
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

    def __repr__(this) -> str(float):
        # _log.add(f'class (timer) -> __repr__ ')
        return f'{this.get}'

def MakeDict(ls1:[list, set, tuple],ls2:[list, set, tuple]) -> dict:
    # _log.add(f'func (make_dict) with {ls1,ls2}')
    '''
    return a dictionary with ls1 as key and ls2 as result
    will return None if lenght ls1 != lenght of ls2
    '''
    ls1=list(ls1)
    ls2=list(ls2)

    ret = {x:y for x,y in zip(list(ls1),list(ls2))}
    return ret


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
    def new(this):
        # _log.add(f'class (rng) -> new prop')
        this.var = []
        for _ in range(this.size):
            this.var.append(rint(this.mn,this.mx))
        return this.var

    def get(this):
        # _log.add(f'class (rng) -> get prop')
        this.var = []
        for _ in range(this.size):
            this.var.append(rint(this.mn,this.mx))
        return this.var

    def __init__(this,mn,mx,size=1):
        # _log.add(f'class (rng) -> __init__ with {this,mn,mx,size}')
        this.size=size
        this.mn=mn
        this.mx=mx
        this.new

    def __repr__(this):
        # _log.add(f'class (rng) -> __repr__')
        if len((var:=this.var))==1:
            var=this.var[0]
        this.new
        return f'{var}'

    def NewSize(this,size):
        # _log.add(f'class (rng) -> new_size with ({size})')
        this.size=size
        this.new

    def NewMin(this,mn):
        # _log.add(f'class (rng) -> new_min with {this,mn}')
        this.mn=mn
    def NewMax(this,mx):
        # _log.add(f'class (rng) -> new_max with {this,mx}')
        this.mx=mx

    def __call__(this):
        return this.get()

def print(*msg,end='\n'):
    try:
        if len(msg) == 1:
            msg = msg[0]
        if len(msg) == 0:
            msg = ''
    except TypeError:pass

    sout.write(f'{msg}{end}')

def printl(*msg):
    try:
        if len(msg) == 1:
            msg = msg[0]
        if len(msg) == 0:
            msg = ''
    except TypeError:pass

    sout.write(f'{msg}')


# def input(*msg,joiner=", "):
# 	print(joiner.join(msg),end="")
# 	for line in sin:
# 		return line[0:-1]
# issue prints AFTER reading input (WTF)
# e.i
# input(':') & user enters'd'
# result:
# d
# :⏎
# return d


# start of chaos

# def encpt(string:str,fm:str,tm:str):
# 	# _log.add(f'func (encpt) with {string , fm , tm}')
# 	string = list(string)
# 	dif = ord(fm) - ord(tm)
# 	for s in r(string):
# 		string[s]=chr( ord( string[s] ) + dif )
# 	return ''.join(string)

# def decpt(string:str,fm:str,tm:str):
# 	# _log.add(f'func (decpt) with {string , fm , tm}')
# 	return encpt(string,tm,fm)

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

color={
# formating: '$(name)' : '\003[$(mode);$(ColorCode)m'
# modes: 0:normal 1:bold? 2:dark 3:italics 4:underline 5:blinking 6:blinking2? 7:bkground
    'nc':'\033[0m',
    'white':'\033[0m',
    'black' : '\033[0;30m',
    'red' : '\033[0;31m',
    'green' : '\033[0;32m',
    'yellow' : '\033[0;33m',
    'blue' : '\033[0;34m',
    'magenta' : '\033[0;35m',
    'cyan' : '\033[0;36m',
    
    'dark gray' : '\033[0;90m',
    'dark grey' : '\033[0;90m',
    
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
    'bk white':'\033[7;0m',
    'bk black' : '\033[7;30m',
    'bk red' : '\033[7;31m',
    'bk green' : '\033[7;32m',
    'bk yellow' : '\033[7;33m',
    'bk blue' : '\033[7;34m',
    'bk magenta' : '\033[7;35m',
    'bk cyan' : '\033[7;36m',
    'bk light gray' : '\033[7;37m',
    'bk light grey' : '\033[7;37m',
    'bk dark gray' : '\033[7;90m',
    'bk dark grey' : '\033[7;90m',
    'bk light red' : '\033[7;91m',
    'bk light green' : '\033[7;92m',
    'bk light yellow' : '\033[7;93m',
    'bk light blue' : '\033[7;94m',
    'bk light magenta' : '\033[7;95m',
    'bk light cyan' : '\033[7;96m',
    
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
        '(' : ')',
        '[' : ']',
        '{' : '}',
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
    if a-1<b or b<a+1:
        return a*b
    AssureType(int,a,ErrorMsg=f"a : {a} != int")
    AssureType(int,b,ErrorMsg=f"b : {b} != int")
    # _log.add(f'func ( mmc/lcm ) with {a , b}')
    greater = max(a,b)
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

def fact(n:int) -> int:
    # _log.add(f'func ( fact ) with {n}')
    Fact = 1
    for i in range(1,n+1):
        Fact*=i
    return Fact

def ArgvAssing(argvs:iter) -> dict:
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

    if indcn == []:
        if argv == []:
            ret[None] = []
        else:
            ret[None] = argvs

    elif indcn[0] > 0:
        ret[None] = argvs[0:indcn[0]]

    for index in r(argvs):
        argvs[index] = argvs[index].replace("/-",'-')

    for i in r(indcn):
        try:
            dif = indcn[i+1]-indcn[i]
            add = argvs[indcn[i]:indcn[i]+dif][1:]
            # for AddIndex in r(add):
                # add[AddIndex] = add[AddIndex].replace("/-",'-')
            ret[argvs[indcn[i]:indcn[i]+dif][0]] = add#argvs[indcn[i]:indcn[i]+dif][1:]
        except IndexError:
            add = argvs[indcn[i]+1:]
            # for AddIndex in r(add):
                # add[AddIndex] = add[AddIndex].replace("/-",'-')
            ret[argvs[indcn[i]]] = add#argvs[indcn[i]+1:]
    return ret


argv_assing = ArgvAssing

class time:
    @property
    def sec(this):
        # _log.add(f'class ( time ) -> sec')
        return __ftime__(f"%S")

    @property
    def min(this):
        # _log.add(f'class ( time ) -> min')
        return __ftime__(f"%M")

    @property
    def hour(this):
        # _log.add(f'class ( time ) -> hour')
        return __ftime__("%H")

    @property
    def day(this):
        # _log.add(f'class ( time ) -> day')
        return __ftime__("%D").split('/')[1]

    @property
    def month(this):
        # _log.add(f'class ( time ) -> month')
        return __ftime__("%D").split('/')[0]

    @property
    def year(this):
        # _log.add(f'class ( time ) -> year')
        return __ftime__("%D").split("/")[2]

def notify(title="",body=""):
    Notify.init("util.py/func/notify/init")
    Notify.Notification.new(str(title),str(body)).show()

def exit(num:int=1) -> None:
    # _log.add(f'class ( exit ) = ({num}) => act')
    AssureType(int,num,ErrorMsg=f'var {num} of wrong type, should be int')
    if num < 256:
        exi(num)
    else:
        raise NumberTooBigError("exit num : %d > 255" % num)

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
    def __init__(this,name="test",mode="exec",code=[]):
        this.name,this.mode,this.code = name,mode,code

    def __add__(this,line):
        this.code.append(line)
        return code(this.name,this.mode,this.code)

    def __call__(this):
        if type(this.code) == str:this.code=this.code.split('\n')
        for line in this.code:
            exec(compile(line,this.name,this.mode))

    def __repr__(this):
        msg = ""
        if type(this.code) == str:this.code=this.code.split('\n')
        if len(this.code) > 1:
            for line in this.code:
                msg+=f"{line}\n"
        else:
            msg = f"{this.code[0]}"
        return msg


class var(object):
    '''
    this class should NOT be used for items in iterables! (like lists)

    this class "contains" the other classes in it,
    so you can stop worring about doing this foo=DoShit(foo,args)
    and start doing this foo.DoShit(args)
    and facilitating your life when using dicts

    for i in {'a':1,'b':2,'c':3} = 	ERROR
    for i in var({'a':1,'b':2,'c':3}) = dict.keys()

    "hello world"[3] = '!' = ERROR
    var("hello world")[3] = '!' = "hel!o world"

    [1,2,3]+[2,3,4] = ERROR
    var([1,2,3])+[2,3,4] = [1,2,3,2,3,4]
    var([1,2,3])+var([2,3,4]) = [1,2,3,2,3,4]
    '''
    def __init__(this,Value:object,Type:type=None,PrintMutipleLines=True):
        if type(Value) == type and type(Type) != type:
            Value,Type = Type,Value

        if Type == None:Type=type(Value)

        this.Type = Type
        this.Value = Value
        this.PrintMutipleLines=bool(PrintMutipleLines)

        Types = {
            (float,int):"IsNumber",
            (list,set,str):"IsIterable",
            (str,):"IsString",
            (frozenset,):"IsFrozenset",
            (dict,):"IsDict"
        }

        for i in Types.keys():
            exec(f"this.{Types[i]} = {this.Type in i}")

    # math shit start



    def __add__(this,add):
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
                ReturnVar = this.Type(ORGroups(this.Value,add))
            else:
                ReturnVar = this.Value+add

        # var = dict
        elif this.IsDict:
            ret = this.Value
            for i in add.keys():
                ret[i] = add[i]
        return ReturnVar

    def __sub__(this,add):
        # var - var
        ReturnVar,ReturnType = None,this.Type
        if type(add) == var:add=add.Value

        # var != dict
        if not this.IsDict:
            if this.IsIterable:
                ReturnVar = this.Type(NOTGroups(this.Value,add))
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

    def __mul__(this,add):
        if type(add) == var:add=add.Value

        if this.IsNumber:
            return this.Value * add
        else:
            raise WrongType(f"var class can't multiply {this.Value} with {add}")

    def __truediv__(this,add):
        if type(add) == var:add=add.Value

        if this.IsNumber:
            return this.Value / add
        else:
            raise WrongType(f"var class can't divide {this.Value} with {add}")

    def __floordiv__(this,add):
        if type(add) == var:add=add.Value

        if this.IsNumber:
            return this.Value // add
        else:
            raise WrongType(f"var class can't (floor) divide {this.Value} with {add}")

    # math shit done
    # list/dict stuff start

    def __iter__(this):
        for i in this.Value:
            yield i

    # calling method
    def __getitem__(this,index_or_content):
        if type(index_or_content) == var:index_or_content = index_or_content.Value
        ret = this.Value[index_or_content]

        return ret

    # list/dict stuff done
    # (other) magic methods start

    def dict(this,lst:list):
        return MakeDict(this.Value,lst)

    def __dict__(this,lst:list):
        return MakeDict(this.Value,lst)

    def __len__(this):
        if this.IsDict:
            return len(this.Value.Keys())
        return len(this.Value)

    def __setitem__(this, index, obj):
        if this.IsFrozenSet:
            raise TypeError(f"can't set value of FrozenSet\nvalue:{this.Value}")
        if this.IsString:
            ret = list(this.Value)
            ret[index] = obj
        else:
            ret = [this.Value]
            ret[index] = obj

        this.Value = ret


    def __repr__(this):
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

    def split(this,string:str=None):
        if type(string) == var:string = string.Value
        if string == None:
            ret = this.Value.split()
        else:
            ret = this.Value.split(string)
        return ret

    def join(this,string:str or var):
        if type(string) == var:string = string.Value
        ret = ""
        if this.IsIterable:
            for thing in this.Value:
                if type(thing) == var:
                    ret+=f"{string}{thing.Value}"
                else:
                    ret+=f"{string}{thing}"

            return ret[1:]
        else:
            raise TypeError(f"\n{var} is not iterable")

    def SplitBracket(this,bracket,ClosingBracket="default"):
        if type(bracket) == var:bracket = bracket.Value
        if type(ClosingBracket) == var:ClosingBracket = ClosingBracket.Value

        if ClosingBracket == "default":
            ret = SplitBracket(this.Value,bracket)
        else:
            ret = SplitBracket(this.Value,bracket,ClosingBracket)
        if type(ret)!=var:
            ret = ret
        return ret


    def keys(this):
        return list(this.Value.keys())

    def index(this,content:object):
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

    def pop(this,index):
        if this.IsString:
            char = this.Value[index]
            if index == -1:
                this.Value = this.Value[:-1]
            else:
                this.Value = this.Value[index+1:]+this.Value[:index]
            return char
        else:
            return this.Value.pop(index)

    def remove(this,content):
        this.Value.remove(this)

    def copy(this):
        return var(this.Value,PrintMutipleLines=this.PrintMutipleLines)
    
    def find(this,string:str)-> int:
        return this.Value.find(string)


    # complex methods done


class BDP:
    def __init__(this,name,IgnoreDataSize=False):
        # for unix like system
        # c:/users/{USER}/bdp
        this.IgnoreDataSize = IgnoreDataSize

        if not exists(f"/home/{USER}/BDP"):
            ss("mkdir /BDP/")

        if not name.startswith("~/BDP/"):
            name = f"~/BDP/{name}"
        if not name.endswith(".pog"):
            name = f"{name}.pog"

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

    def load(this):
        this.data = UseFile(this.name,'r')
        return this.data

    def __repr__(this):
        if len(f"{this.data}") < 100 or this.IgnoreDataSize:
            return f"name: {this.name}\ndata: {this.data}"
        else:
            return f"name: {this.name}\n{color['yellow']}data too big to display\nBDP(IgnoreDataSize=True) to ignore size{color['nc']}"

    def __call__(this,data=None):

        if data == None and this.data == None:
            return this.load()

        elif this.data == None:
            this.data = data

        this.save()
        return "saved"

def MessageMid(msg,WindoLen,OffsetChar=' '):
    off = OffsetChar*(WindoLen//2)
    return f"{off}{msg}{off}"

def NumberToExponent(number):
    smol = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','.':'.'}

    ret = ''.join([smol[i] for i in str(number)])
    return ret

def rbool(OneIn=2):
    return not rint(0,OneIn-1)

def rcase(word:str):
    wd = ''
    for case in word:
        if rbool():
            case = case.upper()
        else:
            case = case.lower()
        wd+=case
    return wd

def invert(var):
    return var[::-1]

def EncryptS(var,key:int or float):
    return [ord(char)+key for char in var]
    # ret = []
    # for char in str(var):
        # ret.append(ord(char)+key)
    # return ret

def DecryptS(var:str,key:int or float):
    return "".join([f"{chr(char-key)}" for char in var])
    # ret = []
    # for char in var:
        # ret.append(f"{chr(char-key)}")
    # return "".join(ret)

def AdvEncryptS(var,key,deep):
    if deep <= 0:
        deep=1
    elif deep == 1 or deep == 0:
        return EncryptS(var, key)
    else:
        return AdvEncryptS(var, key*deep, deep-1)

def AdvDecryptS(var,key,deep):
    if deep <= 0:
        deep=1
    elif deep == 1 or deep == 0:
        return DecryptS(var, key)
    else:
        return AdvDecryptS(var, key*deep, deep-1)

def PosOrNeg(num):
    try:
        return 1//num*2+1
    except ZeroDivisionError:
        return 0

def odd(var:int) -> bool:
    return var%2

def numbers(times,nums=0):
    return eval(f'[{nums}'+f",{nums}"*(times-1)+']')

def ShowTextGif(sprites,SleepTime=0.35,times=-1):#if times is negative the loop won't stop || if times = 0, it will be len(sprites)*2
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

def GetCh():
    fd = sin.fileno()
    old_settings = tcgetattr(fd)
    try:
        setraw(sin.fileno())
        ch = sin.read(1)
    finally:
        tcsetattr(fd, TCSADRAIN, old_settings)
    return ch

def GetTerminalSize():
    h, w, *_ = unpack('HHHH',ioctl(0, TIOCGWINSZ,pack('HHHH', 0, 0, 0, 0)))
    return w, h

def JustDecimal(number):
    return number-int(number)

def NoDecimal(number):
    return int(number)

def number(num:str)->int or float:
    return eval(num)

def TimesInNumber(TimesIn,NumberTo) -> bool:
    return bool(sum([rbool(TimesIn) for x in r(NumberTo)]))

def NumSum(numbers:int or float) -> int:
    numbers = str(numbers).replace('.', "")
    numbers = sum([int(num) for num in numbers])
    if len(str(numbers)) != 1:
        return NumSum(numbers)
    else:
        return numbers

def FindAll(StringToSearchIn:str,StringToFind:str) -> list[str]:
    StringToFindL = len(StringToFind)
    NotStringToFind = '0'*StringToFindL
    if NotStringToFind == StringToFind:
        NotStringToFind = '1'*StringToFindL
    # StringToFind can't be 000... and 111... at the same time!

    # how many times {StringToFind} appears in {StringToSearchIn}
    times:int = int((len(StringToSearchIn) - len(StringToSearchIn.replace(StringToFind,"")))/StringToFindL)
    # how? | gets len of StringASText - len of StringASText without {StringToFind} devides the result to the len os {StringToFind}

    ret = []
    for i in r(times):
        ret.append(StringToSearchIn.find(StringToFind))
        StringToSearchIn = StringToSearchIn.replace(StringToFind, NotStringToFind,1)
    return ret

def timeit(func):
    def wrapper(*args,**kwargs):
        timer = tm()
        ret=func(*args,**kwargs)
        return ret,round(tm()-timer,6)
    return wrapper


def DeepSum(args,ParseStringWith=eval,ParseString=False,ReturnDeeph=False):
    """
    this function will add everything in the iterable in {args}, even strings
    may return deeph of the iterable in {ReturnDeeph} is True (will calculate deeph any way tho)
    this ReturnDeeph thing adds one for every item but iterables (but will count the deeph in side those iterables)
    """
    ret = 0
    deeph = 0
    for thing in args:
        deeph+=1
        if type(thing) in (float,int):
            # add number
            ret+=thing
        elif type(thing) == str:
            if ParseString:
                # parse and add string
                ret+=ParseStringWith(thing)
            else:
                # breaks because found string
                raise TypeError("\n%sERROR IN \"DeepSum\" function%s\n\
value %s is of type string (and ParseString = False)" %  (color['br red'],color["nc"],repr(thing)))
        else:
            # recourciveness (it that a word?)
            deeph-=1
            RetA,DeephA=DeepSum(thing,ParseString=ParseString,ParseStringWith=ParseStringWith,ReturnDeeph=True)
            # adds the nums and deeph of recourcive run
            ret += RetA
            deeph += DeephA

    if ReturnDeeph:
        return ret,deeph
    else:
        return ret
    # DUDE DOING THIS MADE ME WANT TO KILL SOMEONE


def average(args,SumString=False,SumFunc=DeepSum):
    sum,deeph = SumFunc(args,ParseString=SumString,ReturnDeeph=True)
    return sum/deeph


# funcs/classes [OUT DATED ?]
'''
    # VARS
    USER
    FuncType
    NoneType
    iterables
    class NumberTooBigError
    infinity
    # CLASSES / FUNCS
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
    func( notify)
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
    func( NumberToExponent)
    func( rbool)
    func( rcase)
    func( invert)
    func( EncryptS)
    func( DecryptS)
    func( AdvEncryptS)
    func( AdvDecryptS)
    func( PosOrNeg)
    func( odd)
    func( numbers)
    func( ShowTextGif)
    func( GetCh)
    func( GetTerminalSize)
    func( JustDecimal)
    func( number)
'''
