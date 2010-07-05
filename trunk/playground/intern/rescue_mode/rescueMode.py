# -*- coding: utf-8 -*-
import urwid
import time
import diskTools
import guiTools
import dbusTools
from pardus import diskutils
import subprocess
import os , parted

class Program:
  palette = [('pardus','white','dark magenta'),
	     ('focus','black','dark cyan')]
	     
  def __init__(self):
    self.dbus = None
    #Main Frame'i oluştur
    body = urwid.Filler(urwid.Divider(),'top')
    header = urwid.AttrWrap(urwid.Text("Pardus 2011 Kurtarma Moduna Hoşgeldiniz"),'pardus')
    footer = urwid.AttrWrap(urwid.Padding(urwid.Text("<Yön Tuşları> menüde dolaşmak | <F1> çıkış"),'right'),'pardus')
    self.mainFrame=urwid.Frame(body,header,footer)
    self.in_co = []
 
    #İç Pencereyi oluştur
    listFrame = guiTools.listDialog(None,['pardus','focus'],"Yapmak istediğiniz işlemi seçiniz") 
    
    listFrame.addMenuItem("Shell'e git",self.kapat)
    listFrame.addMenuItem("Windows boot loader'ı yükle",self.winListScreen)
    listFrame.addMenuItem("Pardus'u kurtar",self.diskSecmeEkrani)
    
    self.pencereOlustur(listFrame,80,15)
  
  
  
  def winListScreen(self):
    def winInfo(item):
      return "Seçilen Windows diski :"+item.args[3]+" dosya sistemi:"+item.args[2]
    self.pop_up("Windows kurulu diskler aranıyor")
    listFrame = guiTools.listDialog(winInfo,['pardus','focus'],"Bootloader'ını geri yüklemek istediğiniz Windows'u seçiniz")
    for win in diskTools.getWinBootPartitions():
      listFrame.addMenuItem("Windows%s"%win[1],self.installWinBootLoader,win)
    
    self.pencereOlustur(listFrame,80,15)
    self.loop.widget = self.mainFrame
  
  def installWinBootLoader(self,win):
    
    subprocess.call("./install-mbr -p %d %s"%(win[1],win[0]),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    self.pop_up("./install-mbr -p %d %s"%(win[1],win[0]))
  
  def diskSecmeEkrani(self):
    
    def diskBilgisi(item):
      return "Seçilen disk : "+item.args[0]+" label:"+item.args[1]
    
    def diskSec(device):
      self.selectedDisk = device
      self.in_co.append(device)
      self.pardusDevice = diskutils.parseLinuxDevice(device[0])
      self.otherDevices = diskutils.getDeviceMap()
      #self.otherDevices.remove((self.pardusDevice[2],self.pardusDevice[0]))
      self.islemSecmeEkrani()
    
    listFrame = guiTools.listDialog(diskBilgisi,['pardus','focus'],"Lütfen listeden disk bölümünü seçin") 
        
    for i in diskTools.getPardusPartInfo():
       listFrame.addMenuItem(i[0],diskSec,[i[1],i[2],i[3]])
        
    self.pencereOlustur(listFrame,80,15)
  
  
  def islemSecmeEkrani(self):

    listFrame = guiTools.listDialog("Seçilen disk : "+self.selectedDisk[0]+" label:"+self.selectedDisk[1],
    ['pardus','focus'],"Lütfen yapamak istediğiniz işlemi seçin")
    
    listFrame.addMenuItem("Pisi geçmişi",None)
    listFrame.addMenuItem("Parola Değiştir",self.userlistScreen)
    listFrame.addMenuItem("GRUB'ı tekrar yükle",self.grubIslemEkrani)
    
    self.pencereOlustur(listFrame,80,15)
  
#######################################
######## GRUB PROCESS #################
#######################################
  def grubIslemEkrani(self):
       
    listFrame = guiTools.listDialog("Seçilen disk : "+self.in_co[0][0]+" label:"+self.in_co[0][1],
    ['pardus','focus'],"Lütfen yapamak istediğiniz işlemi seçin")
    
    
    mbr_boot_screen = self.grubIslemSec
    if len(self.otherDevices)>1:
      mbr_boot_screen = self.grubDiskSec
    listFrame.addMenuItem("Pardus'un kurulu olduğu disk bölümü",self.grubIslemSec,1)
    listFrame.addMenuItem("Açılış diski (önerilen)",mbr_boot_screen,0)
    
    self.pencereOlustur(listFrame,80,15)
    
    
    
  def grubDiskSec(self,arg):
    def diskBilgisi(item):
      return "Seçilen disk : "+item.args[0][1]
    def grubIslemSec(option):
      self.in_co.append(option[1])
      self.in_co.append(option[0])
      self.grubYukle()   
    
    listFrame = guiTools.listDialog(diskBilgisi,['pardus','focus'],"Birden fazla açılış diski var. Lütfen listeden açılış diskinizi seçiniz.") 
        
    for i in self.otherDevices:
       deviceName = parted.PedDevice.get(i[1]).model
       listFrame.addMenuItem(deviceName,grubIslemSec,[i,2])
        
    self.pencereOlustur(listFrame,90,15)
    
  
  def grubIslemSec(self,option):
      self.in_co.append(option)
      self.grubYukle() 
    
  def grubYukle(self):
    def grub(pardusDevice,option):
	pass
	root_path = "(%s,%s)" % (pardusDevice[0], pardusDevice[1])
	
	if option == 0:
	  setupto = "(%s)" % pardusDevice[0]
	elif option == 1:
	  setupto = "(%s,%s)" % (pardusDevice[0], pardusDevice[1]) 
	elif option == 2:
	  setupto = "(%s)" % pardusDevice[2]
	
	batch_template = """root %s
setup %s
quit
""" % (root_path, setupto)

        
	fd =  file('/tmp/_grub','w')
	fd.write(batch_template)
	fd.close()
        
        
#       f = file("/dev/null", "w")
#	procutils.run_quiet("/tmp/grub.sh")  
#	subprocess.call("grup -no-floppy --batch < /tmp/_grub",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    
      
    if self.in_co[1] !=2:
      grub([self.pardusDevice[2],self.pardusDevice[3]],self.in_co[1])
    else:
      grub([self.pardusDevice[2],self.pardusDevice[3],self.in_co[2][0]],self.in_co[1])
      
      
    self.sonuc(open('/tmp/_grub').read()+"secenek: %d "%self.in_co[1])
    
    
  def sonuc(self,arg):
    self.pop_up("GRUB yükleniyor")

    time.sleep(1)
    body = urwid.Padding(urwid.Text(arg),'center')
    body = body = urwid.Filler(body,'middle')
    self.pencereOlustur(body,80,10)
    self.loop.widget=self.mainFrame
    
#######################################
######## PASSWORD PROCESS #############
#######################################  
  
  def userlistScreen(self):
  #  self.pop_up("Diske bağlanılıyor")
   # path = diskTools.get_partitions_path(self.in_co[0][0])
    self.pop_up("DBUS'a bağlanılıyor")
    self.dbus = dbusTools.pardusDbus(self.selectedDisk[2])
    self.pop_up("Kullanıcı listesi alınıyor")
    users = self.dbus.getUserlist()
    listFrame = guiTools.listDialog(self.selectedDisk[2],
    ['pardus','focus'],"Lütfen kullanıcı seçiniz")
    
    
    for user in users:
      listFrame.addMenuItem(str(user[1]),self.getPassword,user)
    
    self.pencereOlustur(listFrame,80,30)
    self.loop.widget = self.mainFrame
    
  
  def getPassword(self,user):
    def func(passwd,re_passwd):
      if passwd == re_passwd:
	if passwd != "":
	  self.pop_up("Şifre değiştiriliyor")
	  if self.dbus.setUserPass(int(user[0]), passwd):
	      self.pop_up("Değiştirilemedi")
	  else:
	      self.pop_up("Değiştirildi")
	  return True
      else:
	inputFrame.clearBoxes()
	self.pop_up("Yanlış giriş yaptınız lütfen tekrar deneyin")
	time.sleep(2)
	self.loop.widget = self.mainFrame
	return False
    
    editCaptions = ["Yeni Şifre        :","Yeni Şifre Tekrar :"]
    inputFrame = guiTools.PasswordDialog(func,['pardus','focus'],editCaptions,"Lütfen yeni şifrenizi giriniz.","Şifresi değiştirilecek kullanıcı: "+str(user[1]))
   
    
    self.nob = inputFrame.unhandled_input
    #while(True):
    self.pencereOlustur(inputFrame,80,15)
     


    
  def pencereOlustur(self,body,width,height,header=None,footer=None):
    window=urwid.LineBox(urwid.AttrWrap(urwid.Frame(body,header,footer),'pardus'))
    window = urwid.Padding(window, 'center', width )
    window = urwid.Filler(window, 'middle', height )
    self.mainFrame.body=window
    
  def pop_up(self,mesaj):
    widget = urwid.Padding(urwid.Text(mesaj),'center')
    widget = urwid.Filler(widget,'middle')
    widget = urwid.Overlay(urwid.LineBox(urwid.AttrWrap(widget,'focus')), self.mainFrame, 'center', 50, 'middle', 5)    
    self.loop.widget=widget
    self.loop.draw_screen()
    
  
  
  
  def main(self):
    self.loop = urwid.MainLoop(self.mainFrame,self.palette,unhandled_input=self.IO)
    self.loop.run()
    
  def IO(self,input):
    if input in 'f1':
      raise urwid.ExitMainLoop()
    else:
      pass
    self.nob(input)
  
  def nob(self,input):
    pass
   
    
  def kapat(self,button):
      raise urwid.ExitMainLoop()
  
    
def main():
  calistir = Program()
  calistir.main()
    
if __name__=="__main__":
    main()
   
    
