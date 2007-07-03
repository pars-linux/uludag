#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

from qt import *
from kdecore import *
from kdeui import *

from utility import *
from profileHandler import *

class browser(QVBox):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setMargin(6)
        self.setSpacing(6)
        
        bar = QToolBar("lala", None, self)
        but = QToolButton(loadIconSet("add.png"), i18n("Add"), "lala", self.slotAdd, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        self.new_but = but
        but = QToolButton(bar)
        but.setEnabled(False)
        bar.setStretchableWidget(but)
        but = QToolButton(loadIconSet("help.png"), i18n("Help"), "lala", self.slotHelp, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        parseConfig()
        createModules()
        self.prflview = ProfileView(self)
        # FIXME: Connections
##        self.connect(self.btn_update, SIGNAL('clicked()'), self.slotUpdate)
##        self.connect(self.btn_help, SIGNAL('clicked()'), self.slotHelp)
##        self.connect(self.btn_autoFind, SIGNAL('clicked()'), self.slotAutoFind)
##        self.connect(self.btn_defaultOpts, SIGNAL('clicked()'),self.getDefaultOptions)
##        self.connect(self.check_allPart, SIGNAL('clicked()'), self.toggleAllPartitions)
##        self.connect(self.line_opts, SIGNAL('lostFocus()'), self.saveSession)
##        self.connect(self.line_mountpoint, SIGNAL('lostFocus()'), self.saveSession)
##        self.connect(self.combo_fs,SIGNAL('activated(const QString&)'),self.saveSession)
        
    def slotAdd(self):
        profileHandler(self)
    
    def slotEdit(self):
        pass
    def slotDelete(self):
        pass
    def slotHelp(self):
        pass

class ProfileView(QScrollView):
    def __init__(self, parent):
        QScrollView.__init__(self, parent)
        self.profileItems = []
        self.viewport().setPaletteBackgroundColor(KGlobalSettings.baseColor())
        self.setHScrollBarMode(self.AlwaysOff)
        self.columns = 3
        for prflname in config.sections():
            # FIXME: True parametresini duzelt. Bunun icin en son kullanilan network profiline fln bakacan.
            ProfileItem(self, prflname)
        self.myResize(self.contentsWidth(),self.contentsHeight())

    def maxHint(self):
        maxw = 0
        maxh = 0
        print "basla"
        for item in self.profileItems:
            hint = item.sizeHint()
            w = hint.width()
            h = hint.height()
            print w
            if w > maxw:
                maxw = w
            if h > maxh:
                maxh = h
        print maxw
        return maxw, maxh
    
    def columnHint(self, width):
        if len(self.profileItems) == 1:
            return 2
        maxw, maxh = self.maxHint()
        c = width / maxw
        print width
        if c < 1:
            c = 1
        if c > 3:
            c = 3
        return c

    def myResize(self, aw, ah):
        childs = self.profileItems
        self.columns = self.columnHint(self.width())
        if not childs or len(childs) == 0:
            return
        
        i = 0
        j = 0
        maxw = aw / self.columns
        maxh = self.maxHint()[1]
        childs.sort(key=lambda x: x.name)
        for item in childs:
            item.is_odd = (i + j) % 2
            item.setGeometry(i * maxw, j * maxh, maxw, maxh)
            item.update()
            i += 1
            if i >= self.columns:
                i = 0
                j += 1
        self.resizeContents(aw, j * maxh)
    
    def resizeEvent(self, event):
        size = event.size()
        self.myResize(size.width(), size.height())
        QWidget.resizeEvent(self, event)
  
    def paintEvent(self, event):
        cg = self.colorGroup()
        QScrollView.paintEvent(self, event)
        paint = QPainter(self)
        paint.save()
        paint.restore()
    
    def add(self, name):
        ProfileItem(self, name)
        self.myResize(self.contentsWidth(),self.contentsHeight())


class ProfileItem(QWidget):
    def __init__(self, view, name):
        self.is_odd = 0
        QWidget.__init__(self, view.viewport())
        self.isActive = config.getboolean(name, "isActive")
        self.tipper = ProfileTipper(self)
        self.tipper.parent = self
        view.profileItems.append(self)
        
        self.view = view
        self.name = name
        
        self.mypix = loadIconSet("proxy").pixmap(QIconSet.Large, QIconSet.Normal)
        self.check = QCheckBox(self)
        self.check.setChecked(self.isActive)
        QToolTip.add(self.check, i18n("Activate/Deactivate this proxy profile"))
        self.check.setGeometry(6, 3, 16, 16)
        self.connect(self.check, SIGNAL("toggled(bool)"), self.slotToggle)
        self.check.setAutoMask(True)
        
        w = self.check.width()
        self.pix_start = 6 + w + 3
        w = self.mypix.width()
        self.text_start = self.pix_start + w + 6
        
        self.edit_but = IconButton("configure", self)
        QToolTip.add(self.edit_but, i18n("Configure this profile"))
##        self.connect(self.edit_but, SIGNAL("clicked()"), self.slotEdit)
        self.del_but = IconButton("cancel", self)
        QToolTip.add(self.del_but, i18n("Delete this profile"))
##        self.connect(self.del_but, SIGNAL("clicked()"), self.slotDelete)
        
        self.show()
        
        self.ignore_signal = False
    
    def slotToggle(self, on):
        if self.ignore_signal:
            return
    
    def slotDelete(self):
        pass
##        conn = self.conn
##        m = i18n("Should I delete the\n'%s'\nconnection?")
##        if KMessageBox.Yes == KMessageBox.questionYesNo(self, unicode(m) % conn.name, i18n("Delete connection?")):
##            comlink.com.Net.Link[conn.script].deleteConnection(name=conn.name)
    
    def slotEdit(self):
        profileHandler(self.parent().parent(), self.name)

    def mouseDoubleClickEvent(self, event):
        self.slotEdit()
    
    def addressText(self):
##        if self.options.get    ext
        text = "defsbsd"
        return text
    
    def paintEvent(self, event):
        paint = QPainter(self)
        col = KGlobalSettings.baseColor()
        if self.is_odd:
            col = KGlobalSettings.alternateBackgroundColor()
        self.edit_but.setPaletteBackgroundColor(col)
        self.del_but.setPaletteBackgroundColor(col)
        paint.fillRect(event.rect(), QBrush(col))
        dip = (self.height() - self.mypix.height()) / 2
        paint.drawPixmap(self.pix_start, dip, self.mypix)
        paint.save()
        font = paint.font()
        font.setPointSize(font.pointSize() + 2)
        font.setBold(True)
        fm = QFontMetrics(font)
        paint.drawText(self.text_start, fm.ascent() + 5, unicode(self.name))
        fark = fm.height()
        paint.restore()
        fm = self.fontMetrics()
        paint.drawText(self.text_start, 5 + fark + 3 + fm.ascent(), self.addressText())
    
    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        dip = (h - self.check.height()) / 2
        self.check.move(6, dip)
        dip = (h - self.del_but.myHeight) / 2
        self.del_but.setGeometry(w - self.del_but.myWidth - 6 - 6, dip, self.del_but.myWidth, self.del_but.myHeight)
        self.edit_but.setGeometry(w - self.del_but.myWidth - 6 - 6 - self.edit_but.myWidth - 3, dip, self.edit_but.myWidth, self.edit_but.myHeight)
        return QWidget.resizeEvent(self, event)
    
    def sizeHint(self):
        f = QFont(self.font())
        f.setPointSize(f.pointSize() + 2)
        f.setBold(True)
        fm = QFontMetrics(f)
        fm2 = self.fontMetrics()
        rect = fm.boundingRect(unicode(self.name))
        rect2 = fm2.boundingRect(self.addressText())
        w = self.text_start + min(rect.width(), 240) + 6 + self.edit_but.myWidth + 3 + self.del_but.myWidth + 6
        w2 = self.text_start + min(rect2.width(), 240) + 6 + self.edit_but.myWidth + 3 + self.del_but.myWidth + 6
        w = max(w, w2)
        h = max(fm.height() + 3 + fm2.height(), 32) + 10
        return QSize(w, h)

class IconButton(QPushButton):
    def __init__(self, name, parent):
        QPushButton.__init__(self, parent)
        self.setFlat(True)
        self.myset = loadIconSet(name, KIcon.Small)
        self.setIconSet(self.myset)
        size = self.myset.iconSize(QIconSet.Small)
        self.myWidth = size.width() + 4
        self.myHeight = size.height() + 4
        self.resize(self.myWidth, self.myHeight)

class ProfileTipper(QToolTip):
    def maybeTip(self, point):
        prfl_item = self.parent
        
        rect = prfl_item.rect()
        rect.setWidth(rect.width() - prfl_item.del_but.myWidth - prfl_item.edit_but.myWidth - 6 - 6 - 4)
        rect.setX(rect.x() + prfl_item.pix_start)
        if not rect.contains(point):
            return
        
        tip = "<nobr>"
        tip += i18n("Name:")
        tip += " <b>%s</b>" % unicode(prfl_item.name)
        tip += "</nobr>"
        self.tip(rect, tip)
