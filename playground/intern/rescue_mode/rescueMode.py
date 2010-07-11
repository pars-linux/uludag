# -*- coding: utf-8 -*-
import urwid
import time
import diskTools
import guiTools
import dbusTools
import bootloaderTools
from pardus import diskutils
import gc

class rescueMode:
  palette = [('window','black','light gray'),
	     ('focus','white','dark red'),
	     ('border','black','dark blue'),
	     ('p_border','black','light gray'),
	     ('shadow','white','black'),
	     ('body','black','dark blue')]
	     
  def __init__(self):
    self.screenContainer = []
    self.otherUnhandled_input = None
    self.dbus = None

    #create main frame
    body = urwid.Filler(urwid.Divider(),'top')
    header = urwid.AttrWrap(urwid.Padding(urwid.Text("PKM - Pardus Rescue Mode"),'center'),'window')
    footer = urwid.AttrWrap(urwid.Padding(urwid.Text("< UP -DOWN > Move on menu | <F1> About PKM | <F2> Undo | <F10>  Quit"),'right'),'window')
    self.mainFrame=urwid.Frame(body,header,footer)

    
    #call first screen function
    self.rescueOptionsScreen()
    
  def rescueOptionsScreen(self,forward=True):  
    
    #create firt window
    frame = guiTools.listDialog(None,['window','focus'],"Please select an option from list") 
    
    
    frame.addMenuItem("Rescue Pardus",self.selectDiskScreen)
    frame.addMenuItem("Rescue Windows bootloader",self.windowsListScreen)
    #frame.addMenuItem("Shell'e git",self.goShell)
    
    self.createWindow(frame,80,15)  
  
  def goShell(self):
    """This function closes the rescue mode and turn the shell"""
    self.popUp("Unmounting partitions")
    self.closeProcess()
    
    self.loop.screen.stop()
    raise urwid.ExitMainLoop()

#######################################
######## WINDOWS PROCESS ##############
#######################################

  def windowsListScreen(self,forward=True):
    """This function shows the installed windows in a list on the screen"""
    if forward:
      self.screenContainer.append(self.rescueOptionsScreen)
    
    def installWinBootLoader(windows):
      self.popUp("Rescuing Windows bootloader")
      bootloaderTools.installWindowsBootLoader(windows)
      time.sleep(1)
      self.finalScreen("Windows bootloader was rescued")
      
   #   self.popUp("./install-mbr -p %d %s"%(win[1],win[0]))
    
    def windowsInfo(windows):
      """This function shows the selected windows info in listDialog footer"""
      return "Selected Windows disk :"+windows.args[3]+" file system:"+windows.args[2]
    
    #show info to user by pop up
    self.popUp("Searching Windows installed disks")
    windowsPartitions = diskTools.getWindowsPartitions()
    
    if windowsPartitions:
      frame = guiTools.listDialog(windowsInfo,['window','focus'],"Please select a Windows installed disk which you want to rescue")
      for windows in diskTools.getWindowsPartitions():
	frame.addMenuItem("Windows%s"%windows[1],installWinBootLoader,windows)
      self.createWindow(frame,80,15)
    else:
      self.finalScreen("There is no Windows installed disk")
    #close pop up and show windowsListScreen
    self.closePopUp()
    
  def selectDiskScreen(self,forward=True):
    """ INFOOO """
    
    self.disconnectDBus()
      
    if forward:
      self.screenContainer.append(self.rescueOptionsScreen)

    def diskInfo(disk):
      return "Selected Pardus disk : "+disk.args[0]+" label:"+disk.args[1]
    
    def selectDisk(disk):
      self.selectedDisk = disk
      self.pardusDevice = diskutils.parseLinuxDevice(disk[0])
      self.otherDevices = diskutils.getDeviceMap()
      self.selectedDiskInfo = "Selected Pardus disk :"+self.selectedDisk[0]+" label:"+self.selectedDisk[1]
      self.selectOperationScreen()
    
    pardusPartitions = diskTools.getPardusPartInfo()
    
    if pardusPartitions:
    
      frame = guiTools.listDialog(diskInfo,['window','focus'],"Please select a partition from list") 
	  
      for pardus in diskTools.getPardusPartInfo():
	frame.addMenuItem(pardus[0],selectDisk,[pardus[1],pardus[2],pardus[3]])
	  
      self.createWindow(frame,80,15)
    else:
      self.finalScreen("There is no Pardus installed disk")
  
  def selectOperationScreen(self,forward=True):
    if forward:
      self.screenContainer.append(self.selectDiskScreen)

    frame = guiTools.listDialog(self.selectedDiskInfo,
    ['window','focus'],"Please select an operation")
    
    frame.addMenuItem("Reinstall GRUB ( boot problems )",self.grubOperationScreen)
    frame.addMenuItem("Change password (lost password)",self.userlistScreen)
    frame.addMenuItem("Pisi history (undo package operations)",self.pisiHistoryListScreen)
    
    self.createWindow(frame,80,15)
  
#######################################
######## GRUB PROCESS #################
#######################################

  def grubOperationScreen(self,forward=True):
    
    if forward:
      self.screenContainer.append(self.selectOperationScreen)
       
    frame = guiTools.listDialog(self.selectedDiskInfo,
    ['window','focus'],"Please select target to install bootloader")
      
    screen = self.installGrub
    if len(self.otherDevices)>1:
      screen = self.selectGrubDisk
    frame.addMenuItem("Firt bootable disk (recommended)",screen,0)
    frame.addMenuItem("Pardus installed partition",self.installGrub,1)
    
    self.createWindow(frame,80,15)
    
    
    
  def selectGrubDisk(self,arg):
    
    self.screenContainer.append(self.grubOperationScreen)
    
    def diskInfo(disk):
      return "Selected disk : "+disk.args[0][1]
    def installGrub(args):
      self.bootDevice = args[0][0]
      self.installGrub(args[1])
    
    frame = guiTools.listDialog(diskInfo,['window','focus'],"There are more then one bootable disk. Please select a disk from list to install bootloader") 
        
    for i in diskTools.getDeviceModel(self.otherDevices):
       frame.addMenuItem(i[0],installGrub,[i[1],2])
        
    self.createWindow(frame,90,15)
    
  
  def installGrub(self,option):
    if option ==2:
      bootloaderTools.installGrub([self.pardusDevice[2],self.pardusDevice[3],self.bootDevice],option)
    else:
      bootloaderTools.installGrub([self.pardusDevice[2],self.pardusDevice[3]],option)
    self.popUp("Installing bootloader ")
    time.sleep(1)
    self.finalScreen("Bootloader was installed")
        
    
#######################################
######## PASSWORD PROCESS #############
#######################################  
  
  def userlistScreen(self,forward=True):
    if forward:
      self.screenContainer.append(self.selectOperationScreen)
    
    
    self.connectDBus()
    self.popUp("Getting user list")
    users = self.dbus.getUserlist()
    frame = guiTools.listDialog(self.selectedDiskInfo,
    ['window','focus'],"Please select an user")
    
    
    for user in users:
      frame.addMenuItem(str(user[1]),self.changeUserPassword,user)
    
    self.createWindow(frame,80,30)
    self.closePopUp()
    
  
  def changeUserPassword(self,user):
    
    self.screenContainer.append(self.userlistScreen)
    
    def error_message(message):
      frame.clearBoxes()
      self.popUp(message)
      time.sleep(2)
      self.closePopUp()
      
    def func(passwd,re_passwd):
      if passwd == re_passwd:
	if passwd != "" :  
	      self.popUp("Password was updating")
	      time.sleep(1)	      
	      returnValue = self.dbus.setUserPass(int(user[0]), passwd)
	      if returnValue[0] == 'message':
		self.finalScreen(returnValue[1])
	      else:
		error_message(returnValue[1])
      else:
	error_message("Passwords do not match")
      return False
    
    editCaptions = ["New password         :",
		    "New password (again) :"]
    frame = guiTools.PasswordDialog(func,['window','focus'],editCaptions,"The user whose password will be update: "+str(user[1]))
   
    
    self.otherUnhandled_input = frame.unhandled_input
    #while(True):
    self.createWindow(frame,80,15)
    
    
#######################################
######## PISI HISTORY #################
#######################################    

  def pisiHistoryListScreen(self,forward=True):
    if forward:
      self.screenContainer.append(self.selectOperationScreen)
      
      
    def takeBack(no):
      self.popUp("Taking back Pisi history")
      #time.sleep(1)
      self.dbus.takeBack(no)
      self.finalScreen("Pisi history had been taken back") 
  
    self.connectDBus()
    
    self.popUp("Getting Pisi history information")
    historys = self.dbus.getHistory()
    frame = guiTools.listDialog(self.selectedDisk[2],
    ['window','focus'],"Please select an operation to undo")
    
    
    for history in historys:
      frame.addMenuItem("operation: %d %s (%s)"%(history.no,history.date,history.type),takeBack,history.no)
    
    self.createWindow(frame,80,30)
    self.closePopUp()

  def finalScreen(self,message):
    self.screenContainer = [self.rescueOptionsScreen]
    body = urwid.Padding(urwid.Text(message+" Please press return to restart computer"),'center')
    body = body = urwid.Filler(body,'middle')
    self.createWindow(body,80,10)
    self.closePopUp()
    self.otherUnhandled_input = None  
    
  def aboutRescuMode(self):
    self.popUp("Pardus Resceu Mode\nVersion:1.0 (beta)\nLicence:GPL_v2\n\nAuthor:Mehmet Burak Aktürk\nE-mail: mb.akturk@gmail.com",height=10)
  
  def createWindow(self,body,width,height):
    window=guiTools.Window(body,["window","border","shadow"])
    window = urwid.Padding(window, 'center', width )
    window = urwid.Filler(window, 'middle', height )
    self.mainFrame.body=urwid.AttrWrap(window,'body')
    gc.collect()
    
  def closeScreen(self):
    self.closePopUp()
    frame = guiTools.listDialog(None,['focus','window'],"Please select what you want to do")
    frame.addMenuItem("Go to shell",self.goShell)
    frame.addMenuItem("Restart Computer",None)
    frame.addMenuItem("Shut down",None)
    
    window = guiTools.Window(frame,["focus","p_border","shadow"])
    
    widget = urwid.Overlay(window, self.mainFrame, 'center',50,'middle', 10)    
    self.loop.widget=widget
    self.loop.draw_screen()
    
        
    
    
    
  def popUp(self,message,width=50,height=5):
    window = guiTools.Window(urwid.Filler(urwid.Padding(urwid.Text(message),'center'),'top'),["focus","p_border","shadow"])
    widget = urwid.Overlay(window, self.mainFrame, 'center',width, 'middle', height)    
    self.loop.widget=widget
    self.loop.draw_screen()
  
  def closePopUp(self): 
     self.loop.widget = self.mainFrame
     
  def connectDBus(self):
    if self.dbus == None or self.dbus.path != self.selectedDisk[2]:
	self.popUp("Trying to connect DBus")
	self.dbus = dbusTools.pardusDbus(self.selectedDisk[2])
	
  def disconnectDBus(self):
    if self.dbus != None:
      self.popUp("Trying to disconnect DBus")
      self.dbus.finalizeChroot()
      self.dbus = None
      self.closePopUp()
  
  def closeProcess(self):
    self.disconnectDBus()
    diskTools.umountPardusPartitions()
    
      
  def run(self):
    self.loop = urwid.MainLoop(self.mainFrame,self.palette,unhandled_input=self.IO)
    self.loop.screen.tty_signal_keys('undefined','undefined','undefined','undefined','undefined')
    self.loop.screen.start()
    self.loop.run()
    
  def IO(self,input):
    if 'f1'in input :
      self.aboutRescuMode()
    if 'esc' in input:
      self.closePopUp()
    if 'f2' in input :
      if self.screenContainer:
	self.screenContainer.pop()(False)
    if 'f10' in input:
	self.closeScreen()
 
    if self.otherUnhandled_input:
      self.otherUnhandled_input(input)
    
if __name__=="__main__":
    rescue = rescueMode()
    rescue.run()