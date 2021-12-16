#! /usr/bin/python3.10
#TODO xmpver
#imports
from util import *

class WrongClosingName(Exception): pass

XMPVER:int = 0.3

def Decode( filename:str , XmpCheck = True) -> dict[str:Any]:
	with open(filename, 'r') as file:
		cont = tuple(file.readlines())
	ncont = ""
	for i in r(cont):
		if cont[i][:-1]:
			ncont+=( TrimChar( TrimChar( cont[i][:-1]), "\t", ""))
	cont = ncont
	del ncont
	i = 0
	structure = {}
	contnow = {}
	condepth = [] # keep track of active conteiner tree
	contname = ""

	while i < len(cont):
		char = cont[i]
		if char == '<':
			if contname:
				condepth.append((contname, contnow))
			ncontname = cont[i+1:i+cont[i:].find('>')]
			if contname and ncontname and ncontname[0] == '/' and ncontname[1:] != contname:
				raise WrongClosingName(
f"<{contname}> != <{ncontname}> container closer must be the same to container opener")
			contname = ncontname
			if contname[0] == '/': # contname end
				condepth.pop(-1)
				if condepth:
					_n, _c = contname[1:], contnow
					contname, contnow = condepth.pop(-1)
					contnow[_n] = _c
				else:
					structure[contname[1:]] = contnow
					if condepth:
						contname, contnow = condepth.pop(-1)
					else:
						contname = ""
			else: # real contname
				contnow = {}
		else:

			if char == '[':
				varname = cont[
					i+1
					:
					i+cont[i:].find(' ')
				]
				varval = cont[
					i+2+len(varname)
					:
					i+len(varname)+cont[i+len(varname):].find(']')
				] # help
				i += len(varname)+cont[i+len(varname):].find(']')
				if contname:
					if varval[0] == '{' and varval[-1] == '}':
						contnow[varname] = list(eval(
							varval[1:-1].replace('{', '[').replace('}', ']')
						))
					else:
						contnow[varname] = eval(varval)
				else:
					if varval[0] == '{' and varval[-1] == '}':
						structure[varname] = list(eval(
							varval[1:-1].replace('{', '[').replace('}', ']')
						))
					else:
						structure[varname] = eval(varval)
		i+=1
	if structure["meta"]["xmpver"] != XMPVER and XmpCheck:
		fprintf(stderr, "unmatched xmpver, file:{f} decoder:{f}\n",
			structure["meta"]["xmpver"], XMPVER)
	return structure

def _SEncode( structure , rl = 0 ):
	ret = ""
	rs = "\t"*rl
	for k in structure.keys():
		if isinstance(structure[k], dict):
			ret+=f"{rs}<{k}>\n"
			ret+=_SEncode(structure[k], rl+1)
			ret+=f"{rs}</{k}>\n"
		else:
			if isinstance(structure[k], list):
				ret+=f"{rs}[{k} {str(structure[k]).replace('[', '{').replace(']', '}')}]\n"
			else:
				ret+=f"{rs}[{k} {repr(structure[k])}]\n"
		if rl == 0:
			ret+='\n'
	return ret

def Encode( filename:str, structure:dict[str,Any] ):
	if "meta" not in structure.keys():
		structure["meta"] = {}
		structure["meta"]["xmpver"] = XMPVER
	with open(filename, 'w') as file:
		file.write( _SEncode(structure)[:-1] )

def UseFile( filename:str, structure:dict[str, Any] = None ):
	if structure == None:
		return Decode(filename)
	else:
		Encode(filename, structure)

UseFile("file.xmp")
