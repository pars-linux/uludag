# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import os
import shutil
import stat
from multiprocessing import Process, Queue
from Queue import Empty

import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QPixmap, QObject, QTimer, QMutex, QWaitCondition

import pisi.ui

import yali.util
import yali.pisiiface
import yali.postinstall
import yali.context as ctx
from yali.gui import ScreenWidget
from yali.gui.Ui.installwidget import Ui_InstallWidget

from yali.gui.Ui.installprogress import Ui_InstallProgress
from pds.gui import PAbstractBox, BOTCENTER

EventCopy, EventSetProgress, EventError, EventCopyFinished , EventAllFinished , EventRetry = range(1001, 1007)

class InstallProgressWidget(PAbstractBox):

    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)

        self.ui = Ui_InstallProgress()
        self.ui.setupUi(self)

        self._animation = 2
        self._duration = 500

    def showInstallProgress(self):
        QTimer.singleShot(1, lambda: self.animate(start = BOTCENTER, stop = BOTCENTER))

    """
    def hideHelp(self):
            self.animate(start = CURRENT,
                         stop  = TOPCENTER,
                         direction = OUT)
    def toggleHelp(self):
        if self.isVisible():
            self.hideHelp()
        else:
            self.showHelp()

    def setHelp(self, help):
        self.ui.helpContent.hide()
        self.ui.helpContent2.setText(help)
        # self.resize(QSize(1,1))
        QTimer.singleShot(1, self.adjustSize)
    """



def iter_slideshows():
    slideshows = []

    release_file = os.path.join(ctx.consts.branding_dir, ctx.flags.branding, ctx.consts.release_file)
    slideshows_content = yali.util.parse_branding_slideshows(release_file)

    for content in slideshows_content:
        slideshows.append({"picture":QPixmap(os.path.join(ctx.consts.branding_dir,
                                                    ctx.flags.branding,
                                                    ctx.consts.slideshows_dir,
                                                    content[0])), "description":content[1]})
    while True:
        for slideshow in slideshows:
            yield slideshow

class Widget(QWidget, ScreenWidget):
    name = "liveInstallation"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_InstallWidget()
        self.ui.setupUi(self)

        self.installProgress = InstallProgressWidget(self)

        self.timer = QTimer(self)
        QObject.connect(self.timer, SIGNAL("timeout()"), self.changeSlideshows)

        self.poll_timer = QTimer(self)
        QObject.connect(self.poll_timer, SIGNAL("timeout()"), self.checkQueueEvent)

        if ctx.consts.lang == "tr":
            self.installProgress.ui.progress.setFormat("%%p")

        self.iter_slideshows = iter_slideshows()

        # show first pic
        self.changeSlideshows()

        self.total = 0
        self.cur = 0
        self.has_errors = False

        # mutual exclusion
        self.mutex = None
        self.wait_condition = None
        self.queue = None

        self.retry_answer = False
        self.sys_copier = None

    def shown(self):
        # Disable mouse handler
        ctx.mainScreen.dontAskCmbAgain = True
        ctx.mainScreen.theme_shortcut.setEnabled(False)
        ctx.mainScreen.ui.system_menu.setEnabled(False)

        # start installer thread
        ctx.logger.debug("Copy system thread is creating...")
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()
        self.queue = Queue()
        self.sys_copier = SystemCopy(self.queue, self.mutex, self.wait_condition, self.retry_answer)

        self.poll_timer.start(500)

        # start installer polling
        ctx.logger.debug("Calling SystemCopy.start...")
        self.sys_copier.start()
        ctx.mainScreen.disableNext()
        ctx.mainScreen.disableBack()

        # start 30 seconds
        self.timer.start(1000 * 30)

        self.installProgress.showInstallProgress()

    def checkQueueEvent(self):

        while True:
            try:
                data = self.queue.get_nowait()
                event = data[0]
            except Empty, msg:
                return

            ctx.logger.debug("checkQueueEvent: Processing %s event..." % event)
            # EventCopy
            if event == EventCopy:
                filename = data[1]
                self.installProgress.ui.info.setText(_("Copying <b>%s</b>" % filename))
                ctx.logger.debug("Copying %s" % filename)
                self.cur += 1
                self.installProgress.ui.progress.setValue(self.cur)

            # EventSetProgress
            elif event == EventSetProgress:
                total = data[1]
                self.installProgress.ui.progress.setMaximum(total)

            # EventCopyFinished
            elif event == EventCopyFinished:
                print "***EventCopyFinished called...."
                self.copyFinished()

            # EventError
            elif event == EventError:
                err = data[1]
                self.installError(err)

            # EventRetry
            elif event == EventRetry:
                package = os.path.basename(data[1])
                self.timer.stop()
                self.poll_timer.stop()
                rc = ctx.interface.messageWindow(_("Warning"),
                                                 _("Following error occured while "
                                                   "installing packages:"
                                                   "<b>%s</b><br><br>"
                                                   "Do you want to retry?")
                                                 % package,
                                                 type="custom", customIcon="warning",
                                                 customButtons=[_("Yes"), _("No")])
                self.retry_answer = not rc

                self.timer.start(1000 * 30)
                self.poll_timer.start(500)
                self.wait_condition.wakeAll()

            # EventAllFinished
            elif event == EventAllFinished:
                self.finished()

    def changeSlideshows(self):
        slide = self.iter_slideshows.next()
        self.ui.slideImage.setPixmap(slide["picture"])
        if slide["description"].has_key(ctx.consts.lang):
            description = slide["description"][ctx.consts.lang]
        else:
            description = slide["description"]["en"]
        self.ui.slideText.setText(description)

    def copyFinished(self):
        yali.postinstall.writeFstab()
        # postscripts depend on 03locale...
        yali.util.writeLocaleFromCmdline()

        #Write InitramfsConf
        yali.postinstall.writeInitramfsConf()

        #Remove autologin as root for virtual terminals
        inittablive = os.path.join(ctx.consts.target_dir,"etc/inittab")
        inittab = file(inittablive).read()
        inittab = inittab.replace("--autologin root ","")
        f = file(inittablive,"w")
        f.write(inittab)
        f.close()

        shutil.copy2(os.path.join(ctx.consts.source_dir,"boot/kernel"),os.path.join(ctx.consts.target_dir,"boot/kernel-%s" %os.uname()[2]))
        print "kernel copied"
        data = [EventAllFinished]
        self.queue.put_nowait(data)

    def execute(self):
        # stop slide show
        self.timer.stop()
        self.poll_timer.stop()
        return True

    def finished(self):
        self.poll_timer.stop()

        if self.has_errors:
            return

        ctx.mainScreen.slotNext()

    def installError(self, error):
        self.has_errors = True
        errorstr = _("""An error occured during the installation of packages.
This may be caused by a corrupted installation medium error:
%s
""") % str(error)
        ctx.interface.exceptionWindow(error, errorstr)
        ctx.logger.error("Package installation failed error with:%s" % error)

class SystemCopy(Process):

    def __init__(self, queue, mutex, wait_condition, retry_answer):
        Process.__init__(self)
        self.queue = queue
        self.mutex = mutex
        self.wait_condition = wait_condition
        self.retry_answer = retry_answer

        self.symlink_dirs = ["opt","lib","bin","sbin","boot","usr"]
        self.copy_dirs = ["etc","root"]
        self.empty_dirs = ["mnt","sys","proc","dev","media","home",
                "var","var/log","var/log/news","var/cache","var/db",
                "var/games","var/lib","var/lib/misc","var/local",
                "var/lock","var/lock/subsys","var/opt","var/run",
                "var/run/pardus","var/spool","var/state","var/tmp","var/yp","tmp"]
        self.symlink_basepath = os.readlink("/usr").replace("/usr","")

        ctx.logger.debug("System Copy Process started.")

    def run(self):
        ctx.logger.debug("System copy process running.")

        #Calculate total size to be copied 
        ctx.logger.debug("Calculating total size")
        total = 0.0
        for dir in self.copy_dirs:
            for (path, dirs, files) in os.walk(dir):
                for file in files:
                    filename = os.path.join(path, file)
                    total += os.stat(filename).st_size

        for dir in self.symlink_dirs:
            for (path, dirs, files) in os.walk(os.path.join("/",self.symlink_basepath,dir)):
                for file in files:
                    filename = os.path.join(path, file)
                    st = os.lstat(filename)
                    mode = stat.S_IMODE(st.st_mode)
                    if stat.S_ISREG(st.st_mode):
                        total += os.stat(filename).st_size

        ctx.logger.debug("Sending EventSetProgress")
        self.cursorlimit = total/100    #for every limit bytes move progress bar one percent
        self.currentbytes = 0
        data = [EventSetProgress, 100]
        self.queue.put_nowait(data)

        try:
            while True:
                try:
                    for dir in self.empty_dirs:
                        os.system("mkdir %s/%s" %(ctx.consts.target_dir, dir))
                    for dir in self.copy_dirs:
                        self.copytree(os.path.join("/",dir),os.path.join(ctx.consts.target_dir,dir))
                    for dir in self.symlink_dirs:
                        self.copytree(os.path.join("/",self.symlink_basepath,dir),
                        os.path.join(ctx.consts.target_dir,dir))
                    break # while
                except Exception, msg:
                    # Lock the mutex
                    self.mutex.lock()

                    # Send error message
                    data = [EventRetry, str(msg)]
                    self.queue.put_nowait(data)

                    # wait for the result
                    self.wait_condition.wait(self.mutex)
                    self.mutex.unlock()

                    if not self.retry_answer:
                        raise msg

        except Exception, msg:
            data = [EventError, msg]
            self.queue.put_nowait(data)
            # wait for the result
            self.wait_condition.wait(self.mutex)

        ctx.logger.debug("System copy finished ...")
        # Copying finished
        data = [EventCopyFinished]
        self.queue.put_nowait(data)


    def copytree(self,src, dst):
        names = os.listdir(src)
        os.makedirs(dst)
        errors = []
        for name in names:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            print srcname
            print dstname
            print "---"
            st = os.lstat(srcname)
            mode = stat.S_IMODE(st.st_mode)
            try:
                if stat.S_ISLNK(st.st_mode):
                    if os.path.lexists(dstname):
                        os.unlink(dstname)
                    linkto = os.readlink(srcname)
                    os.symlink(linkto, dstname)
                elif stat.S_ISDIR(st.st_mode):
                    if not os.path.isdir(dstname):
                        self.copytree(srcname, dstname)
                elif stat.S_ISCHR(st.st_mode):
                    os.mknod(dstname, stat.S_IFCHR | mode, st.st_rdev)
                elif stat.S_ISBLK(st.st_mode):
                    os.mknod(dstname, stat.S_IFBLK | mode, st.st_rdev)
                elif stat.S_ISFIFO(st.st_mode):
                    os.mknod(dstname, stat.S_IFIFO | mode)
                elif stat.S_ISSOCK(st.st_mode):
                    os.mknod(dstname, stat.S_IFSOCK | mode)
                elif stat.S_ISREG(st.st_mode):
                    shutil.copy2(srcname, dstname)
                    self.currentbytes += os.stat(srcname).st_size
                    if self.currentbytes >= self.cursorlimit:
                        data = [EventCopy, "files"]
                        self.queue.put_nowait(data)
                        self.currentbytes -= self.cursorlimit

                os.lchown(dstname, st.st_uid, st.st_gid)
                if not stat.S_ISLNK(st.st_mode):
                    os.chmod(dstname, mode)
                    os.utime(dstname, (st.st_atime, st.st_mtime))

            except (IOError, os.error), why:
                errors.append((srcname, dstname, str(why)))
            # catch the Error from the recursive copytree so that we can
            # continue with other files
            except Error, err:
                errors.extend(err.args[0])

