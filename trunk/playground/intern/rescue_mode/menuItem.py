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
 #   def mouse_event(self,size,event,button,col,row,focus):
  #      if event=='mouse release':
   #         self.state = True
    #        raise DialogExit, 0
     #   return False
   # def get_state(self):
    #    return self.state
    #def get_label(self):
      #  text, attr = self.get_text()
     #   return text