# -*- coding: utf-8 -*-
import urwid
import time
import disk
import listeKutu
import menuItem
from pardus import diskutils
from pardus import procutils
import os , parted

class Program:
  palette = [('pardus','white','dark magenta'),
	     ('focus','black','dark cyan')]
	     
  def __init__(self):
    #Main Frame'i oluştur
    body = urwid.Filler(urwid.Divider(),'top')
    header = urwid.AttrWrap(urwid.Text("Pardus 2011 Kurtarma Moduna Hoşgeldiniz"),'pardus')
    footer = urwid.AttrWrap(urwid.Padding(urwid.Text("<Yön Tuşları> menüde dolaşmak | <F1> çıkış"),'right'),'pardus')
    self.mainFrame=urwid.Frame(body,header,footer)
    self.in_co = []
 
    #İç Pencereyi oluştur
    body = urwid.Filler(urwid.Text("Açılış yazısı"),'top')
    header = urwid.Pile([urwid.Divider(),urwid.Text("Merhaba")])
    
    button = urwid.Button("Kurtarma Moduna Geç",self.diskSecmeEkrani)
    button = urwid.AttrWrap(button,'pardus','focus')
    
    button2 = urwid.Button("Shell'e git",self.kapat)
    button2 = urwid.AttrWrap(button2,'pardus','focus')
    
    l = [button,button2]
    
    #footer = urwid.AttrWrap(urwid.Padding(urwid.Text("<Yön Tuşları> menüde dolaşmak | <F1> çıkış"),'right'),'pardus')
    #header = urwid.AttrWrap(urwid.Text("Pardus 2011 Kurtarma Moduna Hoşgeldiniz"),'pardus')
    #footer = urwid.AttrWrap(urwid.Padding(urwid.Text("<Yön Tuşları> menüde dolaşmak | <F1> çıkış"),'right'),'pardus')
    #urwid.connect_signal(button,'click',self.diskSec)
    bt = urwid.GridFlow(l, 30, 3, 1, 'center')
    self.window=urwid.Frame(body,header,urwid.Pile([urwid.Divider(),bt],focus_item=1))
    
    self.window.set_focus('footer')
    self.window=urwid.LineBox(urwid.AttrWrap(self.window,'pardus'))
    self.window = urwid.Padding(self.window, 'center', 80 )
    self.window = urwid.Filler(self.window, 'middle', 15 )
    #self.window = self.window
    
    
    #Pencereyi MainFrame'e yerleştir
    self.mainFrame.body = self.window
  
  
  
  
  def diskSecmeEkrani(self,button):
    
    def diskBilgisi(item):
      return "Seçilen disk : "+item.args[0]+" label:"+item.args[1]
    
    def diskSec(device):
      self.in_co.append(device)
      self.pardusDevice = diskutils.parseLinuxDevice(device[0])
      self.otherDevices = diskutils.getDeviceMap()
      #self.otherDevices.remove((self.pardusDevice[2],self.pardusDevice[0]))
      self.islemSecmeEkrani()
    
    listFrame = listeKutu.listInfo(diskBilgisi,['pardus','focus'],"Lütfen listeden disk bölümünü seçin") 
        
    for i in disk.getPardusVLP():
       listFrame.addMenuItem(i[0],diskSec,[i[2],i[1]])
        
    self.pencereOlustur(listFrame,80,15)
  
  
  def islemSecmeEkrani(self):

    listFrame = listeKutu.listInfo("Seçilen disk : "+self.in_co[0][0]+" label:"+self.in_co[0][1],
    ['pardus','focus'],"Lütfen yapamak istediğiniz işlemi seçin")
    
    listFrame.addMenuItem("Pisi geçmişi",None)
    listFrame.addMenuItem("Parola Değiştir",self.getUserList)
    listFrame.addMenuItem("GRUB'ı tekrar yükle",self.grubIslemEkrani)
    
    self.pencereOlustur(listFrame,80,15)
  
#######################################
######## GRUB PROCESS #################
#######################################
  def grubIslemEkrani(self):
       
    listFrame = listeKutu.listInfo("Seçilen disk : "+self.in_co[0][0]+" label:"+self.in_co[0][1],
    ['pardus','focus'],"Lütfen yapamak istediğiniz işlemi seçin")
    
    
    mbr_boot_screen = self.grubIslemSec
    if self.otherDevices:
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
    
    listFrame = listeKutu.listInfo(diskBilgisi,['pardus','focus'],"Birden fazla açılış diski var. Lütfen listeden açılış diskinizi seçiniz.") 
        
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

        shell = """#!/bin/bash
grub --no-floppy --batch < /tmp/_grub"""
        #
        
	fd =  file('/tmp/_grub','w')
	fd.write(batch_template)
	fd.close()
        
	fd =  file('/tmp/grub.sh','w')
	fd.write(shell)
        
	fd.close()
	os.chmod('/tmp/grub.sh',0100)
      
        
#       f = file("/dev/null", "w")
#	procutils.run_quiet("/tmp/grub.sh")    
    
    
      
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
  
  def getUserList(self):
    path = disk.get_partitions_path(self.in_co[0][0])
    listFrame = listeKutu.listInfo(path,
    ['pardus','focus'],"Lütfen kullanıcı seçiniz")
    
    
    
    listFrame.addMenuItem("root",None)
    listFrame.addMenuItem("burak",self.getPassword)
    listFrame.addMenuItem("doruk",self.grubIslemEkrani)
    
    self.pencereOlustur(listFrame,80,30)
    
  
  def getPassword(self):
    def func():
      pass
       
    inputFrame = listeKutu.InputDialog("Tamam",func,['pardus','focus'],"Lütfen yeni şifrenizi giriniz.")
    
    
    inputFrame.addInputItem("Tekrar :")
    inputFrame.addInputItem("Şifre :")
    
    self.nob = inputFrame.unhandled_input

    self.pencereOlustur(inputFrame,80,25)
    
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
   
    
