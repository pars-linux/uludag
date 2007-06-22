from struct import *
import string

class Hive:
	"Class for read windows registry hives"
	def __init__(self,filename):
		self.__file__ = open(filename)	# open hive file
		data = self.__file__.read(4096)	# load binary data
		thetuple = unpack("36s2i4052s",data)	# unpack hive structure
		self.__firstkeyindex__ = thetuple[1]
		self.__size__ = thetuple[2]
	
	def firstkey(self):
		"Returns the root key of hive"
		return Key(self.__file__,self.__firstkeyindex__+4096)
	
	def getkey(self,path):
		"Returns the key corresponding to path given"
		key = self.firstkey()
		mylist = path.split('\\')
		for i in range(0,len(mylist)):
			key = key.getsubkey(mylist[i])
		return key
	
	def getvalue(self,path,field):
		"Returns the value corresponding to path and field given"
		key = self.getkey(path)
		return key.getvalue(field)
		
		
class Key:
	"Class for windows registry keys"
	
	def __init__(self,thefile,position):
		self.__file__ = thefile
		self.__position__ = position
		
		self.__file__.seek(position)
		data = self.__file__.read(80)
		thetuple = unpack("19i2h",data)
		
		self.__size__ = thetuple[0]
		self.__parentindex__ = thetuple[4]
		self.numsubkeys = thetuple[6]
		self.__lfindex__ = thetuple[8]
		self.numvalues = thetuple[10]
		self.__valuelistindex__ = thetuple[11]
		self.__namesize__ = thetuple[19]
		
		self.name = self.__file__.read(self.__namesize__)	# name of the key
		
		self.__children__ = []
		self.__file__.seek(4096+self.__lfindex__+8)
		for x in range(0,self.numsubkeys):
			data = unpack("2i",self.__file__.read(8))[0]
			self.__children__.append(data)
		
	def getchild(self,childno):
		"Get subkey by index"
		if ((childno<0) or (childno>=self.numsubkeys)):
			raise IndexError, "list index out of range"
		return Key(self.__file__, self.__children__[childno]+4096)
	
	def getsubkey(self,keyname):
		"Get subkey by name"
		for x in range(0,self.numsubkeys):
			key = self.getchild(x)
			if key.name==keyname:
				return key
		raise KeyError, keyname
	
	def subkeys(self):
		"Return a list of subkey names of the key"
		keys = []
		for x in range(0,self.numsubkeys):
			key = self.getchild(x)
			keys.append(key.name)
		return keys
	
	def valuedict(self):
		"Returns a dictionary of fields and values of the key"
		fields = []
		dictionary = {}
		self.__file__.seek(4100+self.__valuelistindex__)
		
		for x in range(0,self.numvalues):
			data = self.__file__.read(4)
			thetuple = unpack("i",data)
			fields.append(thetuple[0])
		
		for x in range(0,len(fields)):
			self.__file__.seek(4096+fields[x])
			data = self.__file__.read(24)
			thetuple = unpack("i2sh3i2h",data)	# value key
			
			vk = thetuple[1]
			namesize = thetuple[2]
			datasize = thetuple[3]
			dataindex = thetuple[4]
			valtype = thetuple[5]
			flag = thetuple[5]
			
			if (0<valtype<3 and vk=="vk" and flag%2!=0 and 0<namesize<200 and 0<datasize<1000):	# FIXME: cok kasinc oldu
				field = self.__file__.read(namesize)
				self.__file__.seek(4096+dataindex+4)
				data = self.__file__.read(datasize)
				mylist = data.split('\x00')
				value = string.join(mylist,'')
				dictionary[field] = value
		
		return dictionary
	
	def getvalue(self,field):
		"Returns the value of the corresponding field of the key"
		return self.valuedict()[field]
	