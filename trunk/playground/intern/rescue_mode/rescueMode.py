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
    header = urwid.AttrWrap(urwid.Padding(urwid.Text("PKM - Pardus Kurtarma Modu"),'center'),'window')
    footer = urwid.AttrWrap(urwid.Padding(urwid.Text("<Yön Tuşları> menüde dolaşmak | <F1> PKM hakkında | <F2> Geri dön | <F10> Kabuğa git"),'right'),'window')
    self.mainFrame=urwid.Frame(body,header,footer)

    
    #call first screen function
    self.rescueOptionsScreen()
    
  def rescueOptionsScreen(self,forward=True):  
    
    #create firt window
    frame = guiTools.listDialog(None,['window','focus'],"Yapmak istediğiniz işlemi seçiniz") 
    
    
    frame.addMenuItem("Pardus'u kurtar",self.selectDiskScreen)
    frame.addMenuItem("Windows önyükleyicisini kurtar",self.windowsListScreen)
    #frame.addMenuItem("Shell'e git",self.goShell)
    
    self.createWindow(frame,80,15)  
  
  def goShell(self):
    """This function closes the rescue mode and turn the shell"""
    self.popUp("Diskler ayrılıyor")
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
      self.popUp("Windows önyükleyicisi kurtarıyor...")
      bootloaderTools.installWindowsBootLoader(windows)
      time.sleep(1)
      self.finalScreen("Windows önyükleyiciniz kurtarıldı.")
      
   #   self.popUp("./install-mbr -p %d %s"%(win[1],win[0]))
    
    def windowsInfo(windows):
      """This function shows the selected windows info in listDialog footer"""
      return "Seçilen Windows diski :"+windows.args[3]+" dosya sistemi:"+windows.args[2]
    
    #show info to user by pop up
    self.popUp("Windows kurulu diskler aranıyor")
    windowsPartitions = diskTools.getWindowsPartitions()
    
    if windowsPartitions:
      frame = guiTools.listDialog(windowsInfo,['window','focus'],"Önyükleyicisini kurtarmak istediğiniz Windows'u seçiniz")
      for windows in diskTools.getWindowsPartitions():
	frame.addMenuItem("Windows%s"%windows[1],installWinBootLoader,windows)
      self.createWindow(frame,80,15)
    else:
      self.finalScreen("Sistemde kurulu Windows bulunamadı.")
    #close pop up and show windowsListScreen
    self.closePopUp()
    
  def selectDiskScreen(self,forward=True):
    """ INFOOO """
    
    self.disconnectDBus()
      
    if forward:
      self.screenContainer.append(self.rescueOptionsScreen)

    def diskInfo(disk):
      return "Seçilen disk : "+disk.args[0]+" label:"+disk.args[1]
    
    def selectDisk(disk):
      self.selectedDisk = disk
      self.pardusDevice = diskutils.parseLinuxDevice(disk[0])
      self.otherDevices = diskutils.getDeviceMap()
      self.selectOperationScreen()
    
    pardusPartitions = diskTools.getPardusPartInfo()
    
    if pardusPartitions:
    
      frame = guiTools.listDialog(diskInfo,['window','focus'],"Lütfen listeden disk bölümünü seçin") 
	  
      for pardus in diskTools.getPardusPartInfo():
	frame.addMenuItem(pardus[0],selectDisk,[pardus[1],pardus[2],pardus[3]])
	  
      self.createWindow(frame,80,15)
    else:
      self.finalScreen("Sistemde kurulu Pardus bulunamadı.")
  
  def selectOperationScreen(self,forward=True):
    if forward:
      self.screenContainer.append(self.selectDiskScreen)

    frame = guiTools.listDialog("Seçilen disk : "+self.selectedDisk[0]+" label:"+self.selectedDisk[1],
    ['window','focus'],"Lütfen yapamak istediğiniz işlemi seçin")
    
    frame.addMenuItem("GRUB'ı tekrar yükle",self.grubOperationScreen)
    frame.addMenuItem("Parola Değiştir",self.userlistScreen)
    frame.addMenuItem("Pisi geçmişi",self.pisiHistoryListScreen)
    
    self.createWindow(frame,80,15)
  
#######################################
######## GRUB PROCESS #################
#######################################

  def grubOperationScreen(self,forward=True):
    
    if forward:
      self.screenContainer.append(self.selectOperationScreen)
       
    frame = guiTools.listDialog("Seçilen disk : "+self.selectedDisk[0]+" label:"+self.selectedDisk[1],
    ['window','focus'],"Lütfen yapamak istediğiniz işlemi seçin")
      
    screen = self.installGrub
    if len(self.otherDevices)>1:
      screen = self.selectGrubDisk
    frame.addMenuItem("Açılış diski (önerilen)",screen,0)
    frame.addMenuItem("Pardus'un kurulu olduğu disk bölümü",self.installGrub,1)
    
    self.createWindow(frame,80,15)
    
    
    
  def selectGrubDisk(self,arg):
    
    self.screenContainer.append(self.grubOperationScreen)
    
    def diskInfo(disk):
      return "Seçilen disk : "+disk.args[0][1]
    def installGrub(args):
      self.bootDevice = args[0][0]
      self.installGrub(args[1])
    
    frame = guiTools.listDialog(diskInfo,['window','focus'],"Birden fazla açılış diski var. Lütfen listeden açılış diskinizi seçiniz.") 
        
    for i in diskTools.getDeviceModel(self.otherDevices):
       frame.addMenuItem(i[0],installGrub,[i[1],2])
        
    self.createWindow(frame,90,15)
    
  
  def installGrub(self,option):
    if option ==2:
      bootloaderTools.installGrub([self.pardusDevice[2],self.pardusDevice[3],self.bootDevice],option)
    else:
      bootloaderTools.installGrub([self.pardusDevice[2],self.pardusDevice[3]],option)
    self.popUp("Grub kurtarılıyor")
    time.sleep(1)
    self.finalScreen("Grub kurtarıldı.")
        
    
#######################################
######## PASSWORD PROCESS #############
#######################################  
  
  def userlistScreen(self,forward=True):
    if forward:
      self.screenContainer.append(self.selectOperationScreen)
    
    
    self.connectDBus()
    self.popUp("Kullanıcı listesi alınıyor")
    users = self.dbus.getUserlist()
    frame = guiTools.listDialog("Seçilen disk : "+self.selectedDisk[0]+" label:"+self.selectedDisk[1],
    ['window','focus'],"Lütfen kullanıcı seçiniz")
    
    
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
	      self.popUp("Şifre değiştiriliyor")
	      time.sleep(1)	      
	      returnValue = self.dbus.setUserPass(int(user[0]), passwd)
	      if returnValue[0] == 'message':
		self.finalScreen(returnValue[1])
	      else:
		error_message(returnValue[1])
      else:
	error_message("Yanlış giriş yaptınız lütfen tekrar deneyin")
      return False
    
    editCaptions = ["Yeni Şifre        :","Yeni Şifre Tekrar :"]
    frame = guiTools.PasswordDialog(func,['window','focus'],editCaptions,"Şifresi değiştirilecek kullanıcı: "+str(user[1]))
   
    
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
      self.popUp("Pisi geçmişi kurtarılıyor")
      #time.sleep(1)
      self.dbus.takeBack(no)
      self.finalScreen("Pisi geçmişi kurtarıldı.") 
  
    self.connectDBus()
    
    self.popUp("Pisi geçmişi alınıyor")
    historys = self.dbus.getHistory()
    frame = guiTools.listDialog(self.selectedDisk[2],
    ['window','focus'],"Lütfen kurtarmak istediğiniz geçmişi seçiniz")
    
    
    for history in historys:
      frame.addMenuItem("no: %d tarih: %s saat: %s (%s)"%(history.no,history.date,history.time,history.type),takeBack,history.no)
    
    self.createWindow(frame,80,30)
    self.closePopUp()

  def finalScreen(self,message):
    self.screenContainer = [self.rescueOptionsScreen]
    body = urwid.Padding(urwid.Text(message+" Bilgisayarı yeniden başlatma için enter'a basınız"),'center')
    body = body = urwid.Filler(body,'middle')
    self.createWindow(body,80,10)
    self.closePopUp()
    self.otherUnhandled_input = None  
    
  def aboutRescuMode(self):
    self.popUp("Pardus Kurtarma Modu\nSürüm:1.0 (beta)\nLisans:GPL_v2\n\nYazar:Mehmet Burak Aktürk\nE-posta: mb.akturk@gmail.com",height=10)
  
  def createWindow(self,body,width,height):
    window=guiTools.Window(body,["window","border","shadow"])
    window = urwid.Padding(window, 'center', width )
    window = urwid.Filler(window, 'middle', height )
    self.mainFrame.body=urwid.AttrWrap(window,'body')
    gc.collect()
    
  def closeScreen(self):
    self.closePopUp()
    frame = guiTools.listDialog(None,['focus','window'],"Lütfen kurtarmak istediğiniz geçmişi seçiniz")
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
	self.popUp("DBUS'a bağlanılıyor")
	self.dbus = dbusTools.pardusDbus(self.selectedDisk[2])
	
  def disconnectDBus(self):
    if self.dbus != None:
      self.popUp("DBUS kapatılıyor")
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