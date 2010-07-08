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
            if self.fn != None:
	      if self.args != None:
		self.fn(self.args)
	      else:
		self.fn()
        return key
        
class PasswordEdit(urwid.Edit):
  def __init__(self,label):
    urwid.Edit.__init__(self,label)
    self.password = ""
   
  def keypress(self,size,key):
    if self.valid_char(key):
      self.password+=key
      self.insert_text("*")
    elif key in ["backspace","delete"]:      
      self.edit_text =self.edit_text[:-1]
    #else:
    return key

class listDialog(urwid.Frame):
  def __init__(self,fn_o_info,palette,header=""):
    
    
    self.palette = palette
    
    self.simpleList = urwid.SimpleListWalker([])
    
    fn_flag = False
    
    if fn_o_info != None: 
      if "function" in str(type(fn_o_info)):
	self.function = fn_o_info
	urwid.connect_signal(self.simpleList, "modified",self.listeModified)
      else:
	fn_flag=True	
	
    
    #liste = urwid.LineBox(urwid.ListBox(self.simpleList))
    liste = urwid.ListBox(self.simpleList)
    liste = urwid.AttrWrap(liste,palette[0])

    #liste =urwid.Pile([urwid.Filler(urwid.Divider('_'),'top'),liste])#,urwid.Filler(urwid.Divider('_'),'top')])
    #liste = urwid.AttrWrap(liste,palette[2])
    
    urwid.Frame.__init__(self,liste)
    self.header = urwid.Pile([urwid.Text(header),urwid.Divider('_'),urwid.Divider()])
    
	
    if fn_flag:
      self.createFooter(fn_o_info)
    
    
    
  def addMenuItem(self,label,function,args=None):
    item= urwid.AttrWrap(MenuItem(" - "+label,function,args),self.palette[0],self.palette[1])
   # self.simpleList.insert(0,item)
    self.simpleList.append(item)
    
  def getContents(self):
    return self.simpleList.contents
  
  def listeModified(self):
    item = self.simpleList.get_focus()[0].get_w()
    #self.footer = urwid.LineBox(a)
    self.createFooter(self.function(item))
    
    #self.footer = urwid.LineBox(urwid.Text("Seçilen disk : "+item.args[0]+" label:"+item.args[1]))
  def createFooter(self,text):
    self.footer = urwid.Pile([urwid.Divider('_'),urwid.Divider(),urwid.Text(text)])
    #urwid.LineBox(urwid.Text(text))
    
    
class PasswordDialog(urwid.Frame):
  
  def __init__(self,function,palette,editCaptions,header="",footer=""):
    self.palette = palette
    self.function = function
    self.passwd = PasswordEdit(editCaptions[0])
    self.re_passwd = PasswordEdit(editCaptions[1])
    
    self.simpleList = urwid.SimpleListWalker([urwid.LineBox( urwid.AttrWrap(self.passwd,self.palette[0],self.palette[1])),
    urwid.LineBox( urwid.AttrWrap(self.re_passwd,self.palette[0],self.palette[1]))])
    
    liste = urwid.ListBox(self.simpleList)

    urwid.Frame.__init__(self,liste)
    self.header =  urwid.Pile([urwid.Text(header),urwid.Divider('_'),urwid.Divider()])
    self.footer =  urwid.Pile([urwid.Divider('_'),urwid.Divider(),urwid.Text(footer)])
   
  
  def clearBoxes(self):
      self.passwd.password=""
      self.re_passwd.password=""
      self.passwd.set_edit_text("")
      self.re_passwd.set_edit_text("")
      self.simpleList.set_focus(0)

  def unhandled_input(self, input):
    if input == 'enter':
	self.function(self.passwd.password,self.re_passwd.password)
	
if __name__=="__main__":
  ps = PasswordEdit("burak")
  ps = urwid.Filler(ps,"top")
  loop = urwid.MainLoop(ps)
  loop.run()
  



  
  
