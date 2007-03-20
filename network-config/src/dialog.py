# -*- coding: utf-8 -*-

import os

def escape(s):
    import re
    return re.sub("([\"\\\\])", r"\\\1", s)

class dialogListEntry:
    def __init__(self, label, value, data=""):
        self.label = label
        self.value = value
        self.data = data

    def __str__(self):
        if self.data:
            return "%s (%s)" % (escape(self.label), escape(self.data))
        return "%s" % escape(self.label)

class dialog:
    def __init__(self, title):
        self.title = title
    
    def showMessage(self, text):
        dialog_data = '--msgbox "%s" 0 0' % escape(text)
        ret = self.__execute__(dialog_data)
        if ret != None:
            return ret
        return None
    
    def showInputBox(self, text, default=""):
        dialog_data = '--inputbox "%s" 0 0 "%s"' % (escape(text), escape(default))
        ret = self.__execute__(dialog_data)
        if ret != None:
            return ret
        return None
    
    def showList(self, text, entries, default=""):
        menu = []
        entry_map = []
        
        for index, entry in enumerate(entries):
            menu.append('%s "%s"' % (index + 1, entry))
            entry_map.append(entry)
        
        if default:
            dialog_data = '--default-item "%s" --menu "%s" 0 0 0 %s' % (escape(default), escape(text), " ".join(menu))
        else:
            dialog_data = '--menu "%s" 0 0 0 %s' % (escape(text), " ".join(menu))
        
        ret = self.__execute__(dialog_data)
        if ret != None:
            return entry_map[int(ret) - 1]
        return None
    
    def __execute__(self, dialog_data):
        temp_file = os.tempnam()
        ret = os.system('/usr/bin/dialog --title "%s" %s 2> %s' % (self.title, dialog_data, temp_file))
        if not ret:
            ret = file(temp_file).read().strip()
        else:
            ret = None
        os.unlink(temp_file)
        return ret

