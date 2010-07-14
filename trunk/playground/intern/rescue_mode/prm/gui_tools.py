# -*- coding: utf-8 -*-
import urwid


class MenuItem(urwid.Text):

    """A custom widget for the --menu option"""
    def __init__(self, label, function, args=None):
        urwid.Text.__init__(self, label)
        self.state = False
        self.function = function
        self.args = args
    def selectable(self):
        return True
    def keypress(self, size, key):
        if key == "enter":
            if self.function != None:
                if self.args != None:
                    self.function(self.args)
                else:
                    self.function()
        return key

class PasswordEdit(urwid.Edit):

    def __init__(self, label):
        urwid.Edit.__init__(self, label)
        self.password = ""

    def keypress(self, size, key):
        if self.valid_char(key):
            self.password += key
            self.insert_text("*")
        elif key in ["backspace", "delete"]:
            self.edit_text = self.edit_text[:-1]
        return key

class ListDialog(urwid.Frame):

    def __init__(self, fn_o_info, palette, header=""):
        self.palette = palette
        self.simple_list = urwid.SimpleListWalker([])
        fn_flag = False
        if fn_o_info != None:
            if "function" in str(type(fn_o_info)):
                self.function = fn_o_info
                urwid.connect_signal(self.simple_list, "modified",
                    self.list_modified)
            else:
                fn_flag = True


        liste = urwid.ListBox(self.simple_list)
        liste = urwid.AttrWrap(liste, palette[0])

        urwid.Frame.__init__(self, liste)
        self.header = urwid.Pile([urwid.Text(header),
          urwid.Divider('_'), urwid.Divider()])

        if fn_flag:
            self.create_footer(fn_o_info)

    def add_item(self, label, function, args=None):
        item = urwid.AttrWrap(MenuItem(" - " + label, function, args),
          self.palette[0], self.palette[1])
        self.simple_list.append(item)

    def list_modified(self):
        item = self.simple_list.get_focus()[0].get_w()
        self.create_footer(self.function(item))

    def create_footer(self, text):
        self.footer = urwid.Pile([urwid.Divider('_'),
          urwid.Divider(), urwid.Text(text)])

class PasswordDialog(urwid.Frame):

    def __init__(self, function, palette, edit_captions, header=""):
        self.palette = palette
        self.function = function
        self.passwd = PasswordEdit(edit_captions[0])
        self.re_passwd = PasswordEdit(edit_captions[1])

        self.simple_list = urwid.SimpleListWalker([
          urwid.LineBox( urwid.AttrWrap(self.passwd,
            self.palette[0], self.palette[1])),
              urwid.LineBox( urwid.AttrWrap(self.re_passwd,
                self.palette[0], self.palette[1]))])

        liste = urwid.ListBox(self.simple_list)

        urwid.Frame.__init__(self, liste)
        self.header =  urwid.Pile([urwid.Text(header),
          urwid.Divider('_'), urwid.Divider()])

    def clear_boxes(self):
        self.passwd.password = ""
        self.re_passwd.password = ""
        self.passwd.set_edit_text("")
        self.re_passwd.set_edit_text("")
        self.simple_list.set_focus(0)

    def unhandled_input(self, pressed):
        if pressed == 'enter':
            self.function(self.passwd.password, self.re_passwd.password)

def create_window(frame, palette):
    window = urwid.LineBox(frame)
    window = urwid.AttrWrap(window, palette[0])
    window = urwid.Columns( [window, ('fixed', 2, urwid.AttrWrap(
            urwid.Filler(urwid.Text((palette[1], '  ')), "top")
            , palette[2]))])
    window = urwid.Frame( window, footer =
         urwid.AttrWrap(urwid.Text((palette[1], '  ')), palette[2]))
    return window

#if __name__ == "__main__":
#    ps = PasswordEdit("burak")
#    ps = urwid.Filler(ps, "top")
#    loop = urwid.MainLoop(ps)
#    loop.run()

