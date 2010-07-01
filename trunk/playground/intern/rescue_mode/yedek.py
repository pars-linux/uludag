# -*- coding: utf-8 -*-
  def islemSec(self,secilenDisk):
    
    self.pop_up("Disk sisteme bağlanıyor")

 #   time.sleep(2)
    header = urwid.Pile([urwid.Divider(),urwid.Text(" Lütfen yapamak istediğiniz işlemi seçin")])
    #footer = urwid.AttrWrap(,'pardus')s
    footer = urwid.LineBox(urwid.Text(" Seçilen disk : "+secilenDisk))
    menu1 = urwid.AttrWrap(MenuItem("GRUB'ı tekrar yükle",self.grubYukle),'pardus','focus')
    menu2 = urwid.AttrWrap(MenuItem("Pisi geçmişi",None),'pardus','focus')
    menu3 = urwid.AttrWrap(MenuItem("Parola Değiştir",None),'pardus','focus')
    
    content = urwid.SimpleListWalker([menu1,menu2,menu3])
    liste = urwid.LineBox( urwid.ListBox(content))
    
    
    
    
    self.pencereOlustur(liste,80,15,header,footer)
    self.loop.widget = self.mainFrame
    
    #self.loop.widget=self.mainFrame
 
    
  
  def grubYukle(self,arg):
    header = urwid.Pile([urwid.Divider(),urwid.Text(" Lütfen sistem yükleyicisinin kurulacağurwid.ExitMainLoopı hedefi seçin")])
    #footer = urwid.AttrWrap(,'pardus')s
    #footer = urwid.LineBox(urwid.Text(" Footer"))
    menu1 = urwid.AttrWrap(MenuItem("Açılış diski (önerilen)",self.sonuc,"GRUB"),'pardus','focus')
    menu2 = urwid.AttrWrap(MenuItem("Pardus'un kurulu olduğu disk bölümü",self.sonuc,"GRUB 2"),'pardus','focus')
    menu3 = urwid.AttrWrap(MenuItem("Listeden seçimlik disk",self.grubDiskSec),'pardus','focus')
    
    content = urwid.SimpleListWalker([menu1,menu2,menu3])
    liste = urwid.LineBox( urwid.ListBox(content))    
    self.pencereOlustur(liste,80,15,header)
    
  def grubDiskSec(self,arg):
    header = urwid.Pile([urwid.Divider(),urwid.Text(" Lütfen listeden disk bölümünü seçin")])
 
    menu1 = urwid.AttrWrap(MenuItem("HARDISK 1",self.sonuc,"GRUB LİSTELİ"),'pardus','focus')
    menu2 = urwid.AttrWrap(MenuItem("HARDISK 2",None),'pardus','focus')
    
    content = urwid.SimpleListWalker([menu1,menu2])
    liste = urwid.LineBox( urwid.ListBox(content))
    self.pencereOlustur(liste,80,15,header)
    
  def sonuc(self,arg):
    self.pop_up("GRUB yükleniyor")

    time.sleep(2)
    body = urwid.Padding(urwid.Text(arg+" işleminiz başarıyla gerçekleştirilmiştir."),'center')
    body = body = urwid.Filler(body,'middle')
    self.pencereOlustur(body,80,10)
    self.loop.widget=self.mainFrame
     
