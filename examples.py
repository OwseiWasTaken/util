from util import *


#example of nBDP

#def ReadStr(this):
#	print("reading str")
#	x = ""
#	size = this.Next()
#	assert size < 256
#	for i in r(size):
#		x+=chr(this.Next())
#	# readers must always go to the next byte
#	this.Next()
#	return x
#
#def WriteStr(string) -> tuple[int, int, int]:
#	print("writing str")
#	assert len(string) < 256
#	return 2,len(string),*[ord(i) for i in string]
#
#nBDPwI[str] = WriteStr
##2 = str 'index'
#nBDPrI[2] = ReadStr
#
#x=nBDP("test", nBDPrI, nBDPwI)
#
#out = x.SealArray([65541])
#print(out)
#print(x.OpenArray(out))

# end of example
