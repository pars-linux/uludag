# -*- coding: utf-8 -*-
import urwid
import time
import disk
import listeKutu

class MenuItem(urwid.Text):
    """A custom widget for the --menu option"""
    def __init__(self, label,fn, arg=None):
        urwid.Text.__init__(self, label)
        self.state = False
        self.fn = fn
        self.arg = arg
        self.label = label
    def selectable(self):
        return True
    def keypress(self,size,key):
	
        self.state = True
	#if self.fn != None:
	 #   self.fn(self.arg)
        return key  
 #   def get_state(self):
        return self.state
  #  def get_label(self):
    #    text, attr = self.get_text()
     #   return text

class Program:
  palette = [('pardus','white','dark magenta'),
	     ('focus','black','dark cyan')]
	     
  def __init__(self):
    #Main Frame'i oluştur
    body = urwid.Filler(urwid.Divider(),'top')
    header = urwid.AttrWrap(urwid.Text("Pardus 2011 Kurtarma Moduna Hoşgeldiniz"),'pardus')
    footer = urwid.AttrWrap(urwid.Padding(urwid.Text("<Yön Tuşları> menüde dolaşmak | <F1> çıkış"),'right'),'pardus')
    self.mainFrame=urwid.Frame(body,header,footer)
    
    
    #İç Pencereyi oluştur
    body = urwid.Filler(urwid.Text("Açılış yazısı"),'top')
    header = urwid.Pile([urwid.Divider(),urwid.Text("Merhaba")])
    
    button = urwid.Button("Kurtarma Moduna Geç",self.diskSec)
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
  
  
  
  
  def diskSec(self,button):
    def diskBilgisi(item):
      urwid.Text("Seçilen disk : "+item.args[0]+" label:"+item.args[1])
    
    header = urwid.Pile([urwid.Divider(),urwid.Text(" Lütfen listeden disk bölümünü seçin")])
    

    body = listeKutu.listeFooter(diskBilgisi,['pardus','focus'])        
    for i in disk.getPardusVLP():
      body.addMenuItem(i[0],diskBilgisi,[i[2],i[1]])
      
    window = urwid.Frame(body,header)
    
    self.mainFrame.body=window
   
    
  def pencereOlustur(self,frame,width,height):
    window=urwid.LineBox(urwid.AttrWrap(frame,'pardus'))
 #   window = urwid.Padding(window, 'center', width )
  #  window = urwid.Filler(window, 'middle', height )
    self.pencereOlustur=window
    
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
  def kapat(self,button):
      raise urwid.ExitMainLoop()
  
    
def main():
  calistir = Program()
  calistir.main()
    
if __name__=="__main__":
    main()
   
    
