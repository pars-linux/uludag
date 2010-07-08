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

    #create main frame
    body = urwid.Filler(urwid.Divider(),'top')
    header = urwid.AttrWrap(urwid.Padding(urwid.Text("Pardus Kurtarma Modu"),'center'),'window')
    footer = urwid.AttrWrap(urwid.Padding(urwid.Text("<Yön Tuşları> menüde dolaşmak | <F1> çıkış | <F2> Geri dön"),'right'),'window')
    self.mainFrame=urwid.Frame(body,header,footer)

    
    #call first screen function
    self.rescueOptionsScreen()
    
  def rescueOptionsScreen(self,forward=True):  
    
    #create firt window
    frame = guiTools.listDialog(None,['window','focus'],"Yapmak istediğiniz işlemi seçiniz") 
    
    frame.addMenuItem("Shell'e git",self.goShell)
    frame.addMenuItem("Windows boot loader'ı yükle",self.windowsListScreen)
    frame.addMenuItem("Pardus'u kurtar",self.selectDiskScreen)
   
    
    self.createWindow(frame,80,15)  
  
  def goShell(self):
    """This function closes the rescue mode and turn the shell"""
    raise urwid.ExitMainLoop()

#######################################
######## WINDOWS PROCESS ##############
#######################################

  def windowsListScreen(self,forward=True):
    """This function shows the installed windows in a list on the screen"""
    if forward:
      self.screenContainer.append(self.rescueOptionsScreen)
    
    def installWinBootLoader(windows):
      self.pop_up("Windows ön yükleyicisi kurtarıyor...")
      bootloaderTools.installWindowsBootLoader(windows)
      time.sleep(1)
      self.finalScreen("Windows ön yükleyiciniz kurtarıldı.")
      
   #   self.pop_up("./install-mbr -p %d %s"%(win[1],win[0]))
    
    def windowsInfo(windows):
      """This function shows the selected windows info in listDialog footer"""
      return "Seçilen Windows diski :"+windows.args[3]+" dosya sistemi:"+windows.args[2]
    
    #show info to user by pop up
    self.pop_up("Windows kurulu diskler aranıyor")
    windowsPartitions = diskTools.getWindowsPartitions()
    
    if windowsPartitions:
      frame = guiTools.listDialog(windowsInfo,['window','focus'],"Bootloader'ını geri yüklemek istediğiniz Windows'u seçiniz")
      for windows in diskTools.getWindowsPartitions():
	frame.addMenuItem("Windows%s"%windows[1],installWinBootLoader,windows)
      self.createWindow(frame,80,15)
    else:
      self.finalScreen("Sistemde kurulu Windows bulunamadı.")
    #close pop up and show windowsListScreen
    self.loop.widget = self.mainFrame
    
  def selectDiskScreen(self,forward=True):
    """ INFOOO """
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
    
    frame.addMenuItem("Pisi geçmişi",self.pisiHistoryListScreen)
    frame.addMenuItem("Parola Değiştir",self.userlistScreen)
    frame.addMenuItem("GRUB'ı tekrar yükle",self.grubOperationScreen)
    
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
    frame.addMenuItem("Pardus'un kurulu olduğu disk bölümü",self.installGrub,1)
    frame.addMenuItem("Açılış diski (önerilen)",screen,0)
    
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
    self.pop_up("Grub kurtarılıyor")
    time.sleep(1)
    self.finalScreen("Grub kurtarıldı.")
        
    
#######################################
######## PASSWORD PROCESS #############
#######################################  
  
  def userlistScreen(self,forward=True):
    if forward:
      self.screenContainer.append(self.selectOperationScreen)
    
    self.pop_up("DBUS'a bağlanılıyor")
    self.dbus = dbusTools.pardusDbus(self.selectedDisk[2])
    self.pop_up("Kullanıcı listesi alınıyor")
    users = self.dbus.getUserlist()
    frame = guiTools.listDialog(self.selectedDisk[2],
    ['window','focus'],"Lütfen kullanıcı seçiniz")
    
    
    for user in users:
      frame.addMenuItem(str(user[1]),self.changeUserPassword,user)
    
    self.createWindow(frame,80,30)
    self.loop.widget = self.mainFrame
    
  
  def changeUserPassword(self,user):
    
    self.screenContainer.append(self.userlistScreen)
    
    def error_message(message):
      frame.clearBoxes()
      self.pop_up(message)
      time.sleep(2)
      self.loop.widget = self.mainFrame
    
    def func(passwd,re_passwd):
      if passwd == re_passwd:
	if passwd != "" :  
	  if len(passwd) >3:
	    if passwd != user[1]:
	      self.pop_up("Şifre değiştiriliyor")
	      time.sleep(1)
	      if self.dbus.setUserPass(int(user[0]), passwd):
		  self.pop_up("Kullanıcının şifresi değiştirilemedi.")
	      else:
		  self.finalScreen("Kullanıcının şifresi değiştirildi.")
	      return True
	    else:
	      error_message("Kullanıcı adınız parolanız olamaz")
	  else:
	    error_message("Parolanız çok kısa")
	    return False
      else:
	error_message("Yanlış giriş yaptınız lütfen tekrar deneyin pass: "+passwd+" pass2: "+re_passwd )
      return False
    
    editCaptions = ["Yeni Şifre        :","Yeni Şifre Tekrar :"]
    frame = guiTools.PasswordDialog(func,['window','focus'],editCaptions,"Lütfen yeni şifrenizi giriniz.","Şifresi değiştirilecek kullanıcı: "+str(user[1]))
   
    
    self.otherUnhandled_input = frame.unhandled_input
    #while(True):
    self.createWindow(frame,80,15)
    
    
#######################################
######## PISI HISTORY #################
#######################################    

  def pisiHistoryListScreen(self,forward=True):
    if forward:
      self.screenContainer.append(self.selectOperationScreen)
      
      
    def takeBack2(no):
      self.pop_up("Pisi geçmişi kurtarılıyor %d"%no)
      #time.sleep(1)
      self.dbus.takeBack(no)
      self.finalScreen("Pisi geçmişi kurtarıldı.")
    
    self.pop_up("DBUS'a bağlanılıyor")
    self.dbus = dbusTools.pardusDbus(self.selectedDisk[2])
    self.pop_up("Pisi geçmişi alınıyor")
    historys = self.dbus.getHistory()
    frame = guiTools.listDialog(self.selectedDisk[2],
    ['window','focus'],"Lütfen kurtarmak istediğiniz geçmişi seçiniz")
    
    
    for history in historys:
      frame.addMenuItem("no: %d tarih: %s saat: %s"%(history.no,history.date,history.time),takeBack2,history.no)
    
    self.createWindow(frame,80,30)
    self.loop.widget = self.mainFrame

  def createWindow(self,body,width,height,header=None,footer=None):
    
    window=urwid.LineBox(urwid.AttrWrap(urwid.Frame(body,header,footer),'window'))
    window=urwid.AttrWrap(window,'window')
    window = urwid.Columns( [window,('fixed', 2, urwid.AttrWrap(
            urwid.Filler(urwid.Text(('border','  ')), "top")
            ,'shadow'))])
    window = urwid.Frame( window, footer = 
         urwid.AttrWrap(urwid.Text(('border','  ')),'shadow'))
    
    window = urwid.Padding(window, 'center', width )
    window = urwid.Filler(window, 'middle', height )
    temp =self.mainFrame.body
    self.mainFrame.body=urwid.AttrWrap(window,'body')
    gc.collect()
    
  def pop_up(self,mesaj):
    
    window=urwid.Frame(urwid.AttrWrap(urwid.LineBox(urwid.Filler(urwid.Padding(urwid.Text(mesaj),'center'),'middle')),'focus'))
    window=urwid.AttrWrap(window,'window')
    window = urwid.Columns( [window,('fixed', 2, urwid.AttrWrap(
           urwid.Filler(urwid.Text(('p_border','  ')), "top")
          ,'shadow'))])
    window = urwid.Frame( window, footer = 
        urwid.AttrWrap(urwid.Text(('p_border','  ')),'shadow'))
    
    #window = urwid.Padding(window, 'center')
   # window = urwid.WidgetWrap(window)
    
    
    widget = urwid.Overlay(window, self.mainFrame, 'center', 50, 'middle', 5)    
    self.loop.widget=widget
    self.loop.draw_screen()
    
  def finalScreen(self,message):
    self.screenContainer = [self.rescueOptionsScreen]
    body = urwid.Padding(urwid.Text(message+" Bilgisayarı yeniden başlatma için enter'a basınız"),'center')
    body = body = urwid.Filler(body,'middle')
    self.createWindow(body,80,10)
    self.loop.widget=self.mainFrame
    self.otherUnhandled_input = None
   
  def run(self):
    self.loop = urwid.MainLoop(self.mainFrame,self.palette,unhandled_input=self.IO)
    self.loop.run()
    
  def IO(self,input):
    if 'f1'in input :
      raise urwid.ExitMainLoop()
    if 'f2' in input :
      if self.screenContainer:
	self.screenContainer.pop()(False)
 
    if self.otherUnhandled_input:
      self.otherUnhandled_input(input)
    
if __name__=="__main__":
    rescue = rescueMode()
    rescue.run()
   
    
