#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import *
from kdeui import *

from utility import *


class textWidget(QLineEdit):
    def __init__(self, parent, mode, options):
        QLineEdit.__init__(self, parent)
        self.mode = mode
        self.options = options
        if options.get("no_edit", False) and mode == "edit":
            self.setReadOnly(True)
    
    def importValue(self, value):
        self.setText(unicode(value))
    
    def exportValue(self):
        return str(self.text())


class passwordWidget(QLineEdit):
    def __init__(self, parent, mode, options):
        QLineEdit.__init__(self, parent)
        self.setEchoMode(QLineEdit.Password)
        self.mode = mode
        self.options = options
        self.value = ""
    
    def importValue(self, value):
        if value:
            self.value = value
            self.setText("*" * 10)
            self.clearModified()
    
    def exportValue(self):
        if self.isModified():
            self.value = str(self.text())
        if "hashMethod" in self.options:
            mod, met = self.options["hashMethod"].rsplit(".", 1)
            crypt = getattr(__import__(mod), met)
            return crypt(self.value)
        return self.value


class numberWidget(QSpinBox):
    def __init__(self, parent, mode, options):
        QSpinBox.__init__(self, parent)
        self.setMaxValue(2**30)
        self.setMinValue(0)
        self.mode = mode
        self.options = options
    
    def importValue(self, value):
        if value:
            self.setValue(int(value))
    
    def exportValue(self):
        return self.value()


class comboWidget(QComboBox):
    def __init__(self, parent, mode, options):
        QComboBox.__init__(self, parent)
        self.mode = mode
        self.options = options
        self.values = []
        if options.get("allow_null", False):
            self.values.append("")
            self.insertItem(i18n("Select..."))
        for value, label in options["options"]:
            self.values.append(value)
            self.insertItem(i18n(label))
        if "default" in options:
            self.importValue(options["default"])
    
    def importValue(self, value):
        if value and value in self.values:
            index = self.values.index(value)
            self.setCurrentItem(index)
    
    def exportValue(self):
        if not self.values[self.currentItem()]:
            return []
        return str(self.values[self.currentItem()])


class listWidgetEditor(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setCaption(i18n("Edit List"))
        layout = QVBoxLayout(self)
        layout.setMargin(4)
        layout.setSpacing(4)
        
        self.editor = KEditListBox(self, "editor")
        layout.addWidget(self.editor)
        
        layout_buttons = QHBoxLayout()
        layout.addLayout(layout_buttons)
        
        but = QPushButton(getIconSet("apply", KIcon.Small), i18n("Apply"), self)
        layout_buttons.addWidget(but)
        self.connect(but, SIGNAL("clicked()"), self.accept)
        
        but = QPushButton(getIconSet("cancel", KIcon.Small), i18n("Cancel"), self)
        layout_buttons.addWidget(but)
        self.connect(but, SIGNAL("clicked()"), self.reject)
        
        self.resize(QSize(350, 300).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
    
    def importValue(self, value):
        self.editor.setItems(QStringList.fromStrList(value))
    
    def accept(self):
        QDialog.accept(self)
    
    def reject(self):
        QDialog.reject(self)


class listWidget(QWidget):
    def __init__(self, parent, mode, options):
        QWidget.__init__(self, parent)
        self.mode = mode
        self.options = options
        self.items = []
        
        layout = QHBoxLayout(self, 0)
        layout.setSpacing(4)
        
        self.textItems = QLineEdit(self)
        self.textItems.setReadOnly(True)
        layout.addWidget(self.textItems)
        
        self.buttonEdit = QPushButton(getIconSet("configure", KIcon.Small), "", self)
        layout.addWidget(self.buttonEdit)
        self.connect(self.buttonEdit, SIGNAL("clicked()"), self.slotEdit)
    
    def slotEdit(self):
        dialog = listWidgetEditor(self)
        items = [unicode(x) for x in self.items]
        dialog.importValue(items)
        if dialog.exec_loop():
            items = [str(x) for x in dialog.editor.items()]
            self.importValue(items)
    
    def importValue(self, value):
        self.items = value
        short_value = value[:3]
        if len(short_value) < len(value):
            short_value = "%s..." % ", ".join(short_value)
        else:
            short_value = ", ".join(short_value)
        self.textItems.setText(unicode(short_value))
    
    def exportValue(self):
        return self.items


class timerWidget(QTimeEdit):
    def __init__(self, parent, mode, options):
        QTimeEdit.__init__(self, parent)
        self.setRange(QTime(0, 0, 0), QTime(23, 59, 59))
        self.mode = mode
        self.options = options
    
    def importValue(self, value):
        if value:
            min, secs = divmod(value, 60)
            hour, min = divmod(min, 60)
            self.setTime(QTime(hour, min, secs))
    
    def exportValue(self):
        t = self.time()
        return t.hour() * 60 * 60 + t.minute() * 60 + t.second()


class timeIntervalWidget(QWidget):
    def __init__(self, parent, mode, options):
        QWidget.__init__(self, parent)
        self.mode = mode
        self.options = options
        
        layout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.setSpacing(4)
        
        self.begin = timerWidget(self, mode, options)
        layout.addWidget(self.begin)
        
        sep = QLabel("-", self)
        layout.addWidget(sep)
        
        self.end = timerWidget(self, mode, options)
        layout.addWidget(self.end)
    
    def importValue(self, value):
        if value:
            begin, end = value.split("-")
            self.begin.importValue(begin)
            self.end.importValue(end)
    
    def exportValue(self):
        begin = self.begin.exportValue()
        end = self.end.exportValue()
        if begin == 0 and end == 0:
            return ""
        return "%s-%s" % (begin, end)
