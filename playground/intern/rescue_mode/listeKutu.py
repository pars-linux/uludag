# -*- coding: utf-8 -*-
import menuItem
import urwid

class listInfo(urwid.Frame):
  def __init__(self,fn_o_info,palette,header=""):
    
    
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
    
    
class InputDialog(urwid.Frame):
  
  def __init__(self,button,button_function,palette,header=""):
    self.palette = palette
   
    
    self.simpleList = urwid.SimpleListWalker([])
    
    liste = urwid.ListBox(self.simpleList)
    #liste = urwid.Filler(liste,'top')
    urwid.Frame.__init__(self,liste)
    self.header = urwid.Pile([urwid.LineBox(urwid.Text(header)),urwid.Divider(),urwid.Divider()])
    self.footer = urwid.Padding(urwid.LineBox(urwid.AttrWrap(urwid.Padding(menuItem.MenuItem(button,button_function),'center'),self.palette[0],self.palette[1])),'center',30)
    
  def addInputItem(self,label):
    item= urwid.LineBox( urwid.AttrWrap(urwid.Edit(label),self.palette[0],self.palette[1]))
    self.simpleList.insert(0,item)
    
  def getContents(self):
    return self.simpleList.contents
  
  def unhandled_input(self, input):
    if input == 'down':
      self.set_focus('footer')
    if input == 'up':
      self.set_focus('body')
  
  
