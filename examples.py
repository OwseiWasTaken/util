from util import *


#example of nBDP

def ReadInt(this):
	# single different line
	print("reading int")
	size = this.Next()
	x = 0
	for i in r(size):
		# +=*9 = =*10
		x+=x*255+this.Next()
	# readers must always go to the next byte
	this.Next()
	return x

#int
def WriteInt(cont) -> tuple[int, int, int]:
	print("writing int")
	# set size
	x = 0
	c = cont
	while c:
		x+=1
		c = c>>1
	if d:=x%8:
		d = 8-d
		x+=d
	# // to easly keep int
	x=x//8
	# set bytes
	# invert
	rs = ('0'*d) + bin(cont)[2:]
	ret = []
	for i in r(x):
		i*=8
		z = rs[i:i+8]
		ret.append(int(z, 2))
	# remember to keeṕ the index (the 1)
	# and the index of the Reader<type> the same
	return 1, x, *ret

#str
def ReadStr(this):
	print("reading str")
	x = ""
	size = this.Next()
	assert size < 256
	for i in r(size):
		x+=chr(this.Next())
	# readers must always go to the next byte
	this.Next()
	return x

def WriteStr(string) -> tuple[int, int, int]:
	print("writing str")
	assert len(string) < 256
	return 2,len(string),*[ord(i) for i in string]

nBDPwI = {int:WriteInt, str:WriteStr}
nBDPrI = [nop, ReadInt, ReadStr]

x=nBDP("cum", nBDPrI, nBDPwI)

out = x.SealArray([65541])
print(out)
print(x.OpenArray(out))

