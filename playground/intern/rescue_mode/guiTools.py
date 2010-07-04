# -*- coding: utf-8 -*-
import urwid

class MenuItem(urwid.Text):
    """A custom widget for the --menu option"""
    def __init__(self, label,fn, args=None):
        urwid.Text.__init__(self, label)
        self.state = False
        self.fn = fn
        self.args = args
    def selectable(self):
        return True
    def keypress(self,size,key):
        if key == "enter":
       #     self.state = True
            if self.fn != None:
	      if self.args != None:
		self.fn(self.args)
	      else:
		self.fn()
	    
        return key

class listDialog(urwid.Frame):
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
    item= urwid.AttrWrap(MenuItem(label,function,args),self.palette[0],self.palette[1])
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
    
    
class PasswordDialog(urwid.Frame):
  
  def __init__(self,function,palette,editCaptions,header="",footer=""):
    self.palette = palette
    self.function = function
    self.passwd = urwid.Edit(editCaptions[0])
    self.re_passwd = urwid.Edit(editCaptions[1])
    
    self.simpleList = urwid.SimpleListWalker([urwid.LineBox( urwid.AttrWrap(self.passwd,self.palette[0],self.palette[1])),
    urwid.LineBox( urwid.AttrWrap(self.re_passwd,self.palette[0],self.palette[1]))])
    
    liste = urwid.ListBox(self.simpleList)

    urwid.Frame.__init__(self,liste)
    self.header = urwid.LineBox(urwid.Text(header))
    self.footer = urwid.LineBox(urwid.Text(footer))
   
  
  def clearBoxes(self):
      self.passwd.set_edit_text("")
      self.re_passwd.set_edit_text("")
      self.simpleList.set_focus(0)

  def unhandled_input(self, input):
    if input == 'enter':
	self.function(self.passwd.get_edit_text(),self.re_passwd.get_edit_text())
  



  
  
