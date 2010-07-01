# -*- coding: utf-8 -*-
import menuItem
import urwid

class listInfo(urwid.Frame):
  def __init__(self,fn_o_info,palette,header="",):
    
    
    self.palette = palette
    
    self.simpleList = urwid.SimpleListWalker([])
    
    f_bayrak = False
    
    if "function" in str(type(fn_o_info)):
      self.function = fn_o_info
      urwid.connect_signal(self.simpleList, "modified",self.listeModified)
    else:
      f_bayrak=True
      
    
    liste = urwid.LineBox(urwid.ListBox(self.simpleList))
    
    urwid.Frame.__init__(self,liste)
    self.header = urwid.LineBox(urwid.Text(header))
    
    if f_bayrak:
      self.createFooter(fn_o_info)
    
    
    
  def addMenuItem(self,label,function,args=None):
    item= urwid.AttrWrap(menuItem.MenuItem(label,function,args),self.palette[0],self.palette[1])
    self.simpleList.insert(0,item)
    
  def getContents(self):
    return self.simpleList.contents
  
  def listeModified(self):
    item = self.simpleList.get_focus()[0].get_w()
    #self.footer = urwid.LineBox(a)
    self.createFooter(self.function(item))
    
    #self.footer = urwid.LineBox(urwid.Text("Seçilen disk : "+item.args[0]+" label:"+item.args[1]))
  def createFooter(self,text):
    self.footer = urwid.LineBox(urwid.Text(text))
    
  
  
