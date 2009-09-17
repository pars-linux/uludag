# -*- coding: utf-8 -*-

####################################
#
# Written By : Şükrü BEZEN
#
# Email : sukru@sukrubezen.com
#
####################################

import os, sys, glob

try:
  import pexpect 
except:
  print "you need to install pexpect module"
  exit()
  
  

class virtual:
  
  def __init__(self):
    self.ip = ""
    self.revdepOutput = ""
    
    self.revdep_outfile = open("revdep_outfile","w")
    self.broken_outfile = open("broken","w")
    self.ldd_outfile    = open("ldd_outfile","w")
    
    self.machineName = ""
    self.machineNames = []
    self.userPass = sys.argv[3]
    self.rootPass = sys.argv[4]
    
    if(len(sys.argv) == 5):
      self.get_machineNames()
      self.chooseMachine()
      self.virtualName = str(sys.argv[1]) + "@" + str(sys.argv[2])
    else:
      print "You need  to provide at least 4 arguments to be able to run this script\n Tip: username machineName userPassword rootPassword VirtualMachineName "
      exit()
      
    self.depolar = []
    self.depolar.append("http://packages.pardus.org.tr/pardus-2009-test/pisi-index.xml.bz2")
    self.depolar.append("http://packages.pardus.org.tr/testci-2009/pisi-index.xml.bz2")
    self.depolar.append("http://packages.pardus.org.tr/pardus-2008-test/pisi-index.xml.bz2")
    self.depolar.append("http://packages.pardus.org.tr/testci-2008/pisi-index.xml.bz2")
    
    self.depoNames = []
    self.paths    = []
    self.packages = []
    
    i = 0
    
    for depo in self.depolar:
      lhs = depo.find("tr") + 3
      rhs = lhs
      i += 1
      
      while(1):
	if(depo[rhs].find("/") != -1):
	  break
	else:
	  rhs += 1
      self.depoNames.append(depo[lhs:rhs])
        
    
  def get_machineNames(self):
    komut  = os.popen("VBoxManage list vms")
    cikti  = komut.read()
    
    while(1):
      rhs    = cikti.find("{") - 2
      if(rhs == -3):break
      i = rhs
    
      while(1):
	i -= 1
	if(cikti[i] == '\n'):
	  lhs = i
	  break
      self.machineNames.append(cikti[lhs+2:rhs])
      cikti = cikti[rhs+3:]
      
  def chooseMachine(self):
    count = 1
    for machine in self.machineNames:
      print str(count) + "-" + machine
      count += 1
    
    while(1):  
      itr = raw_input("Please choose the machine you want to work with\n")
      if(int(itr) >= 1):
	self.machineName = self.machineNames[int(itr)-1]
	break
      else: print "Please write a correct number !"


  def startVm(self):
    os.popen("VBoxManage startvm " + self.machineName)
    self.checkState("running")
    
  def shutdownVm(self):
    os.popen("VBoxManage controlvm " + self.machineName + " poweroff")
    self.checkState("poweroff")
  
  
  def takeSnapshot(self):
    os.popen("VBoxManage snapshot " + self.machineName + " take testornek")
    
  def goBack(self):
    os.popen("VBoxManage snapshot " + self.machineName + " discardcurrent --state")

  def showBridge(self):
    komut = os.popen("VBoxManage showvminfo "+ self.machineName +" --machinereadable")
    cikti = komut.read()
    lhs   = cikti .find("nic1") + 6
    i     = lhs
    while(1):
      i+=1
      if(cikti[i] == '\n'):
	rhs = i-1
	break
    
    nic = cikti[lhs:rhs]
    return nic

  def showState(self):
    komut = os.popen("VBoxManage showvminfo "+ self.machineName +" --machinereadable")
    cikti = komut.read()
    lhs   = cikti.find("VMState=")+9
    i     = lhs
    while(1):
      i+=1
      if(cikti[i] == '\n'):
	rhs = i-1
	break
    
    state = cikti[lhs:rhs]
    return state
    
  def checkState(self,state):    
    while(1):
      if(self.showState() == state):break
      else: continue
      
  def connectTo(self,mode="normal"):
    if(mode == "normal"):
      self.foo = pexpect.spawn("ssh " + str(sys.argv[1]) + "@" + self.ip , timeout=None)
    
      if(self.checkKnownHosts(self.ip) == False):
	self.foo.expect('(yes/no)?')
	self.foo.sendline('yes')
    
      self.foo.expect('.*ssword:')
      self.foo.sendline(self.userPass)
    else:
      self.woo = pexpect.spawn("scp /home/sukru/Virtual/ldd.py " + str(sys.argv[1]) + "@" + self.ip + ":/home/sukru" , timeout=None)
      
      if(self.checkKnownHosts(self.ip) == False):
	self.woo.expect('(yes/no)?')
	self.woo.sendline('yes')
   
      self.woo.expect('.*ssword:')
      self.woo.sendline(self.userPass)
      
      cikti = self.woo.readline()           

    
  def sendCommand(self, command,mode="not_root"):
    
    if(mode == "parse"):
      self.revdepOutput = ""
    
    self.foo.sendline(command)
    
    if(mode == "close"):
      while(1):
	cikti = self.foo.readline()           
	if(cikti.find(self.virtualName) != -1):break
      self.foo.close()
      return
    
          
    if(mode == "exit"):
      self.virtualName = str(sys.argv[1]) + "@" + str(sys.argv[2])
      return
      
    if(mode == "root"):
	self.foo.expect('.*rola:')
	self.foo.sendline(self.rootPass)
	self.virtualName = str(sys.argv[2])
	return
    
    self.foo.sendline("uname")   
    
    while(1):
      cikti = self.foo.readline()           
      if(cikti.find(self.virtualName) != -1):break
    
    
    sys.stdout.write(cikti)
        
    while(1):
      cikti = self.foo.readline()
      
      if(cikti.find(self.virtualName) != -1):break
      
      if((cikti.find("uname") == -1) and (cikti.find(self.virtualName) == -1) ):
	if(mode == "parse"):
	  self.revdepOutput += cikti
	elif(mode == "ldd"):
	  self.ldd_outfile.write(cikti)
	
	sys.stdout.write(cikti)
    
    self.foo.readline()  #read the output of uname
      
      
  def checkKnownHosts(self, what):
    file = open("/home/" + str(sys.argv[1]) + "/.ssh/known_hosts")
    content = file.read()
    itr = content.find(what)
    if(itr == -1): return False
    else: return True
    
    
    
  def repoWorks(self):
    
    i = 0
    
    print "Please choose which repository you want to add"
    print "If you want to add something different than those, just write the address of the repository and enter \n"
    
    for depo in self.depoNames:
      i += 1
      print str(i) + " - " + depo + "\n" + self.depolar[i-1]
      
      
    chose = raw_input()
    
    if(chose == "1" or chose == "2" or chose == "3" or chose == "4"):
      
      self.sendCommand("pisi ar " + self.depoNames[int(chose)-1] + " " + self.depolar[int(chose)-1] + " -y")
      
    else:
      #TODO check if chose is valid repository or not
      
      lhs = chose.find("tr") + 3
      rhs = lhs
      
      while(1):
	if(chose[rhs].find("/") != -1):
	  break
	else:
	  rhs += 1
	  
      self.sendCommand("pisi ar " + chose[lhs:rhs] + " " + chose + " -y")
  
  def lddWorks(self,package):
    self.sendCommand("python /home/" + str(sys.argv[1]) + "/ldd.py start " + str(sys.argv[1]) + " " + package)
    self.sendCommand("python /home/" + str(sys.argv[1]) + "/ldd.py end " + str(sys.argv[1]) ,"ldd")
  
  
  def reverseChecker(self):
    
    _file = open("ack")
    content  = _file.read()
    splitted = content.split('\n')
    
    for line in splitted:
      self.goBack()
      self.startVm()
      self.connectTo()
      self.sendCommand("su -","root")
      self.sendCommand("pisi it " + line + " -y")
      self.sendCommand("revdep-rebuild","parse")
      self.lddWorks(line)
      self.sendCommand("exit","close")
      self.parseOutput()
      self.shutdownVm()
      
  def parseOutput(self):
    cikti = self.revdepOutput
    self.revdep_outfile.write(cikti)
    self.revdep_outfile.flush()
    splitted = cikti.split("\n")
    i = -1
    
    for line in splitted:
      i += 1
      if(line.find("4_names") != -1):break
      
    while(1):
      i += 1
      
      if(i == len(splitted)): break
      
      out = splitted[i]
      split_out = out.split(" ")
      
      if(out.find("paket") != -1 ):             # for Turkish
	
	if(split_out[3][0] != '/'):
	  self.paths.append("/" + split_out[3])
	else:
	  self.paths.append(split_out[3])
	  
	self.packages.append(split_out[0])
      
      elif(out.find("Package") != -1):          # for English
	
	if(split_out[4][0] != '/'):
	  self.paths.append("/" + split_out[4])
	else:
	  self.paths.append(split_out[4])
	
	self.packages.append(split_out[1])
      
    #------------------------------------------------------------------  
    
    i = -1
    for line in splitted:
      i += 1
      if(line.find("2_ldpath") != -1): break
    
    i += 2
    
    while(1):
      i += 1
      out = splitted[i]
      if(out.find("done") != -1): break
      
      out = out[out.find("broken"):]
      split_out = out.split(" ")
      secpath = split_out[1]
      
      if(secpath[0] != '/'):
	control = "/" + secpath
      else:
	control = secpath
      
      j = -1
      
      for path in self.paths:
	j += 1
	
	if(path == control):
	  m = 3
	  
	  while(1):
	    lib = split_out[m]
	    
	    if(lib.find(")") != -1):
	      self.broken_outfile.write( self.packages[j] + " paketindeki " + lib[:lib.find(")")] + " dosyasi icin bulunan paketler :") 
	      self.broken_outfile.write("\n")
	      self.findPackage(lib[:lib.find(")")])
	      break
	    else:
	      self.broken_outfile.write( self.packages[j] + " paketindeki " + lib + " dosyasi icin bulunan paketler :")
	      self.broken_outfile.write("\n")
	      self.findPackage(lib)
	      
	    m += 1
      

	    
  def findPackage(self,library):
        
    html = os.popen("curl http://packages.pardus.org.tr/search/pardus-2009/" + library + "/")
    temphtml = html.read()
    
    while(1):
      itr = temphtml.find("/search/pardus-2009/package/") + len("/search/pardus-2009/package/")
           
      if(itr == (-1 + len("/search/pardus-2009/package/")) ):break
      
      temphtml = temphtml[itr:]
      
      itr = temphtml.find(">") + 1
      
      itl = temphtml.find("<")
      
      paket = temphtml[itr:itl]
      
      
      
      temphtml = temphtml[itr:]
      itr = temphtml.find("<td>")
      
      temphtml = temphtml[itr:]
     
      itr = temphtml.find("<td>") + len("<td>")
      
      itl = temphtml.find("</td>")
      
      yol = temphtml[itr:itl]
      
      self.broken_outfile.write(paket + " " + yol)
      self.broken_outfile.write("\n")
      



obje = virtual()


if(not (obje.showBridge() == "bridged")):
  print "It seems you still did not configure your Network property into \"bridged\" \n program will exit now"
  exit()

obje.startVm()
print "After you open your OS check your opendns server,and write your ip address (/sbin/ifconfig) and enter to continue"
obje.ip = raw_input()
obje.connectTo()
obje.connectTo("extreme")
obje.sendCommand("su -","root")
obje.sendCommand("pisi up --ignore-safety -y")
obje.sendCommand("pisi rr pardus-2009 -y")
obje.sendCommand("pisi rr contrib -y")
obje.repoWorks()
obje.sendCommand("pisi up --ignore-safety -y")
obje.takeSnapshot()
obje.sendCommand("exit","close")
obje.shutdownVm()



obje.reverseChecker()
