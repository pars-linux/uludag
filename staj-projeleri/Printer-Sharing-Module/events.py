import cups,os

class Events:
	connection = cups.Connection()
	def __init__(self):
		self.smb = samba()
		self.sambastatus = "shared"
	
	def shareCups(self,buttonname,printername,parent):
		if buttonname == "Share":
			self.connection.setPrinterShared(printername,True)
			if parent.allowbox.isChecked():
				allowedip = str(parent.customedit.text())
				allowedip = allowedip.replace("*","")
				allowedip = allowedip.replace(" ","")
				if allowedip == "...":
					allowedip = ""
				self.shareSamba(buttonname,allowedip)
		else:
			self.connection.setPrinterShared(printername,False)
			if self.sambastatus == "shared":
				self.shareSamba(buttonname,"")
				
	def getShared(self):
		return self.connection.adminGetServerSettings()['_share_printers']
			
	def serversettings(self):
		settings = self.connection.adminGetServerSettings()
		rmtad = settings['_remote_admin']
		rmtan = settings['_remote_any']
		dbg = settings['_debug_logging']
		shr = settings['_share_printers']
		cnc = settings['_user_cancel_any']
		return [int(rmtad),int(rmtan),int(dbg),int(shr),int(cnc)]
	
	def applyServerSettings(self,rmtad,rmtan,dbg,shr,cnc):
		settings = self.connection.adminGetServerSettings()
		settings["_remote_admin"] = rmtad
		settings["_remote_any"] = rmtan
		settings["_debug_logging"] = dbg
		settings["_share_printers"] = shr
		settings["_user_cancel_any"] = cnc
		
		self.connection.adminSetServerSettings(settings)
		
	def shareSamba(self,buttonname,allowed):
		if buttonname == "Share":
			self.smb.edit("global","netbios name",os.getenv("HOSTNAME"))
			self.smb.edit("global","printcap name","cups")
			self.smb.edit("global","printing", "cups")
			self.smb.edit("global","security","share")
			self.smb.edit("global","guest account","pnp")
			
			self.smb.edit("printers","hosts allow", str(allowed))
			self.smb.edit("printers","path","/var/spool/samba")
			self.smb.edit("printers","printable","yes")
			self.smb.edit("printers","writable","no")
			self.smb.edit("printers","browseable","no")
			self.smb.edit("printers","guest ok","yes")
			self.smb.edit("printers", "create mode", "")
			
			self.smb.edit("share","comment","Samba - Linux Share")
			self.smb.edit("share","path","/home/shared-folder")
			self.smb.edit("share","read only","no")
			self.smb.edit("share","guest ok","yes")
			
			self.smb.edit("print$","comment", "Printer Drivers")
			self.smb.edit("print$","path" ,"/usr/share/cups/drivers")
			self.smb.edit("print$","guest ok", "yes")
			self.smb.edit("print$","write list","root")
			self.smb.edit("print$","browsable", "yes")
			self.sambastatus = "shared"
			
			
			self.smb.writeSections()
		else:
			self.smb.edit("global","hosts allow", "")
			self.smb.edit("global","printcap name","")
			self.smb.edit("global","printing", "")
			self.smb.edit("global","security","user")
			self.smb.edit("global","guest account","")
			
			self.smb.edit("printers","path","/var/spool/samba")
			self.smb.edit("printers","printable","yes")
			self.smb.edit("printers","writable","no")
			self.smb.edit("printers","browseable","no")
			self.smb.edit("printers","guest ok","no")
			self.smb.edit("printers", "create mode", "0700")
			self.sambastatus = "notshared"
			
			
			self.smb.writeSections()
			
#Samba settings
import os, socket, fcntl, struct

class samba:
	def __init__(self): 
		self.sections = []
		self.getSections()
	
	#Section parsing from smb.conf for easy modifications
	def getSections(self):
		file = open("/etc/samba/smb.conf","r")
		lines = file.readlines()
		file.close()
		self.sections.append([])
		index = 0 
		
		for line in lines:
			if line.replace(" ","")[0] == "[":
				self.sections.append([])
				index = index + 1
			self.sections[index].append(line)
			
	def edit(self,section, key, value):
		for index in range(1, len(self.sections)):
			#if there is a section with our name :
			if self.sections[index][0][self.sections[index][0].index("[")+1:self.sections[index][0].index("]")] == section:
				#Finds an appropriate location to write new conf statement
				#If our key occurs we modify its value
				for i in range(len(self.sections[index])):
					pattern = self.sections[index][i].split("=")[0]
					first = self.findfirst(pattern)
					last = self.findlast(pattern)
					if(first!=-1 and pattern[first:last]==key):
						if len(value)>0:
							self.sections[index][i] = "%s = %s\n" %(key,value)
						else:
							self.sections[index][i] = ""
						return 1
				#If our key does not occurs:
				#If there are comments after statements we add our statement before comments
				else:
					if len(value)>0:	
						insertindex = 0
						for line in self.sections[index][1:]:
							insertindex = insertindex + 1
							lineindex = self.findfirst(line)
							if lineindex != -1 and not line[lineindex].isalpha():
								self.sections[index].insert(insertindex,"%s = %s\n"%(key,value))
								return 1
						#If there are no comment we append the list
						else:
							self.sections[index].append("%s = %s\n"%(key,value))
							return 1
						
		#If there is no section with given name we create it:
		else:
			if len(value)>0:
				self.addSection(section,key,value)
				return 1
	def findfirst(self,str):
		for i in range(len(str)):
			if str[i] != " ":
				return i
		else:
			return -1
		
	
	def findlast(self,str):
		str = str.split("=")[0]
		l = len(str)
		for i in range(l):
			if str[l-i-1].isalpha():
				return l-i
	
	#This method adds a new section a smb.conf
	def addSection(self,section,key,value):
		self.sections.append([] )
		length = len(self.sections) -1 
		self.sections[length].append("[%s]\n"%(section))
		self.sections[length].append("%s = %s\n" % (key,value))
	
	#This method saves back the new configurations
	def writeSections(self):			
		file = open("/etc/samba/smb.conf","w")
		for sec in self.sections:
			for line in sec:
				#print line
				file.write(line)
		file.close()
		os.system("service samba restart")
		
#code from  http://code.activestate.com/recipes/439094/
def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])
	
	
if __name__ == "__main__":
	Events()