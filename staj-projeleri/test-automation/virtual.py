# -*- coding: utf-8 -*-
####################################
#
# Written By : Şükrü BEZEN
# Written By : Semen Cirit
#
# Email : sukru@sukrubezen.com
# Email : scirit@pardus.org.tr
#
####################################


import os, sys, glob, time

try:
  import pexpect
except:
  print "you need to install pexpect module"
  exit()

class revdepRebuildAndLddResults:

  def __init__(self):
    self.ip = ""
    self.revdepOutput = ""

    self.revdep_outfile = open("revdep_outfile","w")
    self.broken_outfile = open("broken","a")
    self.ldd_outfile    = open("ldd_outfile","a")

    self.machineName = ""
    self.machineNames = []

    if(len(sys.argv) == 6):
      self.userPass = sys.argv[3]
      self.rootPass = sys.argv[4]
      self.get_machineNames()
      self.chooseMachine()
      self.virtualName = str(sys.argv[1]) + "@" + str(sys.argv[2])
    else:
      print "You need  to provide at least 5 arguments to be able to run this script\n Tip: VMUserName VMName VMuserPassword WMrootPassword RealuserName "
      exit()

    self.repos = []
    self.repos.append("http://packages.pardus.org.tr/pardus-2009-test/pisi-index.xml.bz2")
    self.repos.append("http://packages.pardus.org.tr/testci-2009/pisi-index.xml.bz2")
    self.repos.append("http://packages.pardus.org.tr/pardus-2008-test/pisi-index.xml.bz2")
    self.repos.append("http://packages.pardus.org.tr/testci-2008/pisi-index.xml.bz2")

    self.repoNames = []
    self.choice = ""
    self.pisilrResult = ""
    self.keyValue = {}

    i = 0
    for repo in self.repos:
        splitRepos = repo.split("/")
        repoName = splitRepos[3]
        self.repoNames.append(repoName)

  """ This function gets the virtual box machine names in order to list the machines to user."""
  def get_machineNames(self):
    getMachineNamesCommand  = os.popen("VBoxManage list vms")
    outMachine  = getMachineNamesCommand.read()

    while(1):
      rhs    = outMachine.find("{") - 2
      if(rhs == -3):break
      i = rhs

      while(1):
          i -= 1
          if(outMachine[i] == '\n'):
              lhs = i
              break
      self.machineNames.append(outMachine[lhs+2:rhs])
      outMachine = outMachine[rhs+3:]

  """ This function enables user to choose the machine that he/she wants to work."""
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
      else:
          print "Please write a correct number !"

  """ This function starts the virtual machine that the user has chosen."""
  def startVm(self):
    os.popen("VBoxManage startvm " + self.machineName)
    self.checkState("running")

  """ This function shutdowns the virtual machine that the user has chosen."""
  def shutdownVm(self):
    os.popen("VBoxManage controlvm " + self.machineName + " poweroff")
    self.checkState("poweroff")

  """ This function takes the snapshot of the virtual machine the user has chosen."""
  def takeSnapshot(self):
    os.popen("VBoxManage snapshot " + self.machineName + " take TestSnapshot")
    time.sleep(0.5)

  """ This function revert the current snapshot to its previous state."""
  def goBack(self):
    os.popen("VBoxManage snapshot " + self.machineName + " discardcurrent --state")

  """ This function shows if the selected virtual machine network is in Bridged Adapter state."""
  def showBridge(self):
    showBridgeCommand = os.popen("VBoxManage showvminfo "+ self.machineName +" --machinereadable")
    outShowBridge = showBridgeCommand.read()
    lhs   = outShowBridge.find("nic1") + 6
    i     = lhs
    while(1):
      i+=1
      if(outShowBridge[i] == '\n'):
          rhs = i-1
          break

    nic = outShowBridge[lhs:rhs]
    return nic

  """ This function returns several different states of selected virtaul machine."""
  def showState(self):
    showStateCommand = os.popen("VBoxManage showvminfo "+ self.machineName +" --machinereadable")
    outShowState = showStateCommand.read()
    lhs   = outShowState.find("VMState=")+9
    i     = lhs
    while(1):
      i+=1
      if(outShowState[i] == '\n'):
          rhs = i-1
          break
    state = outShowState[lhs:rhs]
    print state
    return state

  """ This function checks if state is changed."""
  def checkState(self,state):
    while(1):
      if(self.showState() == state):
          break
      else:
          time.sleep(0.5)

  """ This function makes a remote connection to selected virtual machine from user machine."""
  def connectTo(self,mode="normal"):
    print "Connection start..."
    if(mode == "normal"):
      self.execute = pexpect.spawn("ssh " + str(sys.argv[1]) + "@" + self.ip , timeout=None)
      print "ssh " + str(sys.argv[1]) + "@" + self.ip

      if(self.checkKnownHosts(self.ip) == False):
          print "false"
          self.execute.expect('(yes/no)?')
          self.execute.sendline('yes')
      self.execute.expect('.*ssword:')
      self.execute.sendline(self.userPass)
    else:
        print "true"
        self.execute2 = pexpect.spawn("scp ldd.py " + str(sys.argv[1]) + "@" + self.ip + ":/home/" + str(sys.argv[1])  , timeout=None)

        if(self.checkKnownHosts(self.ip) == False):
            self.execute2.expect('(yes/no)?')
            self.woo.sendline('yes')
        self.execute2.expect('.*ssword:')
        self.execute2.sendline(self.userPass)

        outConnectTo = self.execute2.readline()

  def sendCommand(self, command, mode="not_root"):

    if(mode == "parse"):
      self.revdepOutput = ""

    self.execute.sendline(command)
    print command

    if(mode == "close"):
      while(1):
          outSendCommand = self.execute.readline()
          if(outSendCommand.find(self.virtualName) != -1):
              break
          self.execute.close()
          return
    if(mode == "exit"):
      self.virtualName = str(sys.argv[1]) + "@" + str(sys.argv[2])
      return

    if(mode == "root"):
        self.execute.expect('.*rola:')
        self.execute.sendline(self.rootPass)
        self.virtualName = str(sys.argv[2])
        return

    self.execute.sendline("uname")

    while(1):
      outSendCommand = self.execute.readline()
      if(outSendCommand.find(self.virtualName) != -1):
          break
    #sys.stdout.write(outSendCommand)

    while(1):
      outSendCommand = self.execute.readline()
      if(outSendCommand.find(self.virtualName) != -1):
          break

      if((outSendCommand.find("uname") == -1) and (outSendCommand.find(self.virtualName) == -1) ):
          if(mode == "parse"):
              self.revdepOutput += outSendCommand
          elif(mode == "ldd"):
              self.ldd_outfile.write(outSendCommand)
              sys.stdout.write(outSendCommand)
              self.execute.readline()  #read the output of uname
          elif(mode == "pisilr"):
              print outSendCommand
              if not "bz2" in outSendCommand and not "contrib" in outSendCommand:
                self.pisilrResult = outSendCommand.split(" ")
                print self.pisilrResult

  def checkKnownHosts(self, what):
    file = open("/home/" + str(sys.argv[5]) + "/.ssh/known_hosts")
    content = file.read()
    itr = content.find(what)
    if(itr == -1): 
        return False
    else: 
        return True

  def repoWorks(self):
    i = 0
    print "Please choose which repository you want to add"
    print "If you want to add something different than those, just write the address of the repository and enter \n"


    for repo in self.repoNames:
      i += 1
      print str(i) + " - " + repo + "\n" + self.repos[i-1]
    self.choice = raw_input()

    if(self.choice == "1" or self.choice == "2" or self.choice == "3" or self.choice == "4"):
      self.sendCommand("pisi ar " + self.repoNames[int(self.choice)-1] + " " + self.repos[int(self.choice)-1] + " -y")
    else:
        splitRepos = self.choice.split("/")
        repoName = splitRepos[3]
        self.sendCommand("pisi ar " + repoName + " " + self.choice + " -y")

  def lddWorks(self,package):
    self.sendCommand("python /home/" + str(sys.argv[1]) + "/ldd.py start " + str(sys.argv[1]) + " " + package)
    self.sendCommand("python /home/" + str(sys.argv[1]) + "/ldd.py end " + str(sys.argv[1]) ,"ldd")

  def reverseChecker(self):
    ack_file = open("ack", "r")

    for line in ack_file.readlines():
      self.startVm()
      self.connectTo()
      self.sendCommand("su -","root")
      self.sendCommand("pisi it " + line.strip() + " -y")
      self.sendCommand("revdep-rebuild","parse")
      self.lddWorks(line)
      self.sendCommand("exit","close")
      self.parseOutput()
      self.shutdownVm()
      time.sleep(1)
      self.goBack()

  def parseOutput(self):

    outParse = self.revdepOutput
    self.revdep_outfile.write(outParse)
    self.revdep_outfile.flush()
    splitted = outParse.split("\n")

    for line in splitted:
        print line
        split_out = line.split(" ")

        if "paket" in line:             # for Turkish
            self.keyValue[split_out[3].strip()] = split_out[0]
            print self.keyValue[split_out[3].strip()]
        elif "Package" in line:          # for English
            print split_out[4].strip()
            self.keyValue[split_out[4].strip()] = split_out[1]
            print self.keyValue[split_out[4].strip()]
    for line in splitted:
        print line
        split_out = line.split(" ")

        if "broken" in line and not "libraries" in line:
            print split_out[3]
            self.broken_outfile.write( "Package " + self.keyValue[split_out[3]] + "  needs " + split_out[3] + " library so following package(s) needed:")
            self.broken_outfile.write("\n")

            for i  in range(5, len(split_out)):
                if not ")" in split_out[i]:
                    print split_out[i]
                    self.findPackage(split_out[i])
                else:
                    print split_out[i].strip().replace(")", "")
                    self.findPackage(split_out[i].strip().replace(")", ""))

  def findPackage(self,library):
    release = self.repoNames[int(self.choice)-1].split("-")
    html = os.popen("curl http://packages.pardus.org.tr/search/pardus-%s/" % release[1]  + library + "/")
    temphtml = html.read()

    while(1):
      itr = temphtml.find("/search/pardus-%s/package/" % release[1]) + len("/search/pardus-%s/package/" % release[1])
      if(itr == (-1 + len("/search/pardus-%s/package/" % release[1]))):
          break
      temphtml = temphtml[itr:]
      itr = temphtml.find(">") + 1
      itl = temphtml.find("<")
      package = temphtml[itr:itl]
      temphtml = temphtml[itr:]
      itr = temphtml.find("<td>")
      temphtml = temphtml[itr:]
      itr = temphtml.find("<td>") + len("<td>")
      itl = temphtml.find("</td>")
      library = temphtml[itr:itl]
      self.broken_outfile.write(package + " " + library)
      self.broken_outfile.write("\n")

resultObject = revdepRebuildAndLddResults()
if(not (resultObject.showBridge() == "bridged")):
    print "It seems you still did not configure your Network property into \"bridged\" \n program will exit now"
    exit()

resultObject.startVm()
print "After the VirtualBox has opened, please restart openssh of Real Machine and Virtualbox and write the virtualbox ip address and enter to continue:"
resultObject.ip = raw_input()
resultObject.connectTo()
resultObject.connectTo("extreme")
resultObject.sendCommand("su -","root")
resultObject.sendCommand("pisi up --ignore-safety -y")
resultObject.sendCommand("exit","close")
resultObject.shutdownVm()
time.sleep(1)
resultObject.takeSnapshot()

resultObject.startVm()
print "After the VirtualBox has opened, please restart openssh of Real Machine and Virtualbox and write the virtualbox ip address and enter to continue:"
resultObject.ip = raw_input()
resultObject.connectTo()
resultObject.connectTo("extreme")
resultObject.sendCommand("su -", "root")
resultObject.sendCommand("pisi lr", "pisilr")
resultObject.sendCommand("pisi rr %s  -y" % resultObject.pisilrResult[0].replace("\x1b[32m", ""))
resultObject.sendCommand("pisi rr contrib -y")
resultObject.repoWorks()
resultObject.reverseChecker()
