CSLValue = None
CSLAPI_NAME = "string"
debug = None

moddir = dir()

def getFuncTable():
	vtbl = {}
	cls = API()
	for i in dir(cls):
		if i[:4] == "csl_":
			vtbl[i[4:]] = getattr(cls, i)
	return vtbl
	
class API:
	def	csl_strupper(self, prms):
		if prms.has_key("string"):
			a = prms["string"].toString()
			return CSLValue("string", a.upper())
			
	def csl_strip(self, prms):
		if prms.has_key("string"):
			a = prms["string"].toString()
			return CSLValue("string", a.strip())
		debug(DEBUG_FATAL, "Invalid Strip:", prms)
		
	def csl_strlower(self, prms):
		if prms.has_key("string"):
			a = prms["string"].toString()
			return CSLValue("string", a.lower())
			
	def csl_startswith(self, prms):
				if prms.has_key("prefix") and prms.has_key("string"):
					a = prms["string"].toString()
					return CSLValue("string", a.startswith(prms['prefix'].toString()))
	def csl_split(self, prms):
				if prms.has_key("separator") and prms.has_key("string"):
					a = prms["string"].toString()
					arr = a.split(prms["separator"].toString())
					ret = {}
					x = 0
					for i in arr:
						if i != "":
							ret[x] = CSLValue("string", i)
							x += 1
					#print "SPLIT Return:", ret, a, arr,prms["separator"].toString()
					return CSLValue("array", ret)
				print "Incorrect split:", prms
				
	def csl_strlen(self, prms):
		if prms.has_key("string"):
			return CSLValue("numeric", len(prms['string'].toString()))
	
	def csl_strstr(self, prms):
		if prms.has_key("string") and prms.has_key("pattern"):
			print "STRSTR:", prms
			st = prms['string'].toString()
			if st.find(prms['pattern'].toString()) != -1:
				return CSLValue("numeric", 1)
			else:
				return CSLValue("numeric", 0)
			
	def csl_substr_left(self, prms):
		if prms.has_key("string"):
			st = prms['string'].toString()						
			if prms.has_key("size"):
				maxs = int(prms['size'].toNumeric());
				
			else:
				maxs = len(st)
			if maxs > len(st):
				maxs = len(st)
			
			a = st[:maxs]
			return CSLValue("string", a)
	
	def csl_substr_mid(self, prms):
		if prms.has_key("string"):
			if prms.has_key("first"):
				st = prms['string'].toString()
			if prms.has_key("size"):
				maxs = size;
			else:
				maxs = len(st)
			pos = st.find(prms['first'].toString())
			if pos == -1:
				return CSLValue("string", "")
			a = st[pos+1:]
			a = a[:maxs]
			return CSLValue("string", a)
	
	def csl_getnumleft(self, prms):
		ret = ""
		if prms.has_key("string"):
			s = prms["string"].toString()
			skip = 0
			#print "GETNumLeft: '%s'" % (s)
			for i in s:
				if i in "0123456789.":
					ret += i
					skip = 1
				elif i == " ":
					if skip:
						if len(ret):
							ret = float(ret)
						break							
				else:
					if len(ret):
						ret = float(ret)
					break
		#print "getnumleft return:", ret
		if int(ret) == ret:
			ret = int(ret)
		return CSLValue("numeric", ret)
	
	def csl_getnumright(self, prms):
		ret = ""
	
		if prms.has_key("string"):					
			s = prms["string"].toString()
			#print "GETNumRight: '%s'" % (s)
			skip = 0
			for i in range(len(s) - 1, -1, -1):
				c = s[i]
				if c in "0123456789":
					ret = c + ret
					skip = 1
				elif i == " ":
					if skip:
						if len(ret):
							ret = float(ret)
						break							
				else:
					break
		#print "getnumright return:", ret
		return CSLValue("numeric", ret)
	
	def csl_casestartswith(self, prms):
		if prms.has_key("prefix") and prms.has_key("string"):
			a = prms["string"].toString()
			a = a.lower()
			needle = prms['prefix'].toString()
			needle = needle.lower()
			return CSLValue("string", a.startswith(needle))
			
	def csl_caseendswith(self, prms):
		if prms.has_key("trailer") and prms.has_key("string"):
			a = prms["trailer"].toString()
			a = a.lower()
			needle = prms['trailer'].toString()
			needle = needle.lower()
			return CSLValue("string", a.startswith(needle))
	
	def csl_casefind(self, prms):
		if prms.has_key("pattern") and prms.has_key("string"):
			a = prms["string"].toString()
			a = a.lower()
			needle = prms['pattern'].toString()
			needle = needle.lower()
			ret = CSLValue("string", a.find(needle))
			if ret == -1:
				return CSLValue("numeric", 0)
			else:
				return CSLValue("numeric", ret + 1)
	
	def csl_caserfind(self, prms):
		if prms.has_key("pattern") and prms.has_key("string"):
			a = prms["string"].toString()
			a = a.lower()
			needle = prms['pattern'].toString()
			needle = needle.lower()
			ret = CSLValue("string", a.rfind(needle))
			if ret == -1:
				return CSLValue("numeric", 0)
			else:
				return CSLValue("numeric", ret + 1)
		else:
			return CSLValue("numeric", 0)
	
	def csl_rfind(self, prms):
		if prms.has_key("string") and prms.has_key("pattern"):
			a = prms["string"].toString()
			needle = prms['pattern'].toString()
			ret = CSLValue("string", a.rfind(needle))
			if ret == -1:
				return CSLValue("numeric", 0)
			else:
				return CSLValue("numeric", ret + 1)
		else:
			return CSLValue("numeric", 0)
	
	def csl_insert(self, prms):
		if prms.has_key("string") and prms.has_key("part"):
			pos = 0
			rep = 0
			if prms.has_key("position"):
				pos = prms["position"].toNumeric() - 1
	
			if pos < 0:
				pos = 0
	
			if prms.has_key("replace"):
				rep = prms["replace"].toNumeric()
			st = prms["string"]
			ll = st[:pos]
			rl = st[pos + 1:]
	
			if rep:
				rl = rl[rep:]
			return CSLValue("string", ll + prms['part'] + rl)
			
	def csl_hex2dec(self, prms):
		if prms.has_key("value"):
			x = int(prms["value"].toString(), 16)					
			return CSLValue("numeric", x)
		return CSLValue("NULL", 0)
