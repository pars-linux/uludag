#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

''' Gettext Support '''
import gettext
__trans = gettext.translation('PyNotify', fallback=True)
_  =  __trans.ugettext

''' PyQt and PyKDE Modules'''
from qt import *
from kdecore import *
from kdeui import *

''' D-Bus Modules '''
import dbus
import dbus.mainloop.qt3

''' libPyNotify '''
from libPyNotify.genericDevice import genericDevice
from libPyNotify.iconFinder import setIconFinder

class SystemTray(KSystemTray):
    def __init__(self, *args):
        apply(KSystemTray.__init__, (self,) + args)

        ''' Add /usr/share/PyNotify to KStandardDirs '''
        self.KStandardDirs =  KStandardDirs()
        self.KStandardDirs.addResourceDir('icon', '/usr/share/PyNotify')

        ''' Create tray icon Loader '''
        self.icons = KIconLoader('PyNotify', self.KStandardDirs)

        ''' Load icon '''
        self.setPixmap(self.icons.loadIcon('goto', KIcon.Desktop, 22))

        ''' connect shutDown signal to slot for preventing crashes at shutdown '''
        self.connect(app, SIGNAL('shutDown()'), self.slotQuit)

        self.show()

    def slotQuit(self):
        self.deleteLater()
        app.quit()


def deviceAdded(udi):
    ''' DeviceAdded callback function '''
    if not allDevices.__contains__(udi):
        allDevices[udi] = genericDevice(udi, systemBus)

    allDevices[udi].deviceAdded()

def deviceRemoved(udi):
    ''' DeviceRemoved callback function '''
    allDevices[udi].deviceRemoved()

    if allDevices.__contains__(udi):
        allDevices.__delitem__(udi)


if __name__ == '__main__':
    appName = 'PyNotify'
    programName = 'PyNotify'
    description = 'Python Notifier'
    license = KAboutData.License_GPL_V2
    version = '0.1'
    copyright = '(C) 2008 S.Çağlar Onur <caglar@pardus.org.tr>'

    aboutData = KAboutData(appName, programName, version, description, license, copyright)

    aboutData.addAuthor('S.Çağlar Onur', 'Maintainer', 'caglar@uludag.org.tr')

    KCmdLineArgs.init(sys.argv, aboutData)

    ''' Use KUniqueApplication and initialize'''
    gettext.install(appName)
    if not KUniqueApplication.start():
        print _("PyNotify is already running!")
        sys.exit(1)

    app = KUniqueApplication(True, True, True)
    trayWindow = SystemTray(None, appName)

    app.setMainWidget(trayWindow)

    # Create D-Bus mainloop
    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    serviceName = 'org.freedesktop.Hal'
    interfaceName =  '/org/freedesktop/Hal/Manager'
    managerName = 'org.freedesktop.Hal.Manager'

    # Connect to SystemBus
    systemBus = dbus.SystemBus()
    dbusService = systemBus.get_object(serviceName, interfaceName)
    halInterface = dbus.Interface(dbusService, managerName)

    # Set icon finder from KDE
    setIconFinder(lambda icon: str(trayWindow.icons.iconPath(icon, KIcon.Desktop)))

    # Generate Global Device List
    allDevices = {}
    for device in halInterface.GetAllDevices():
        allDevices[device] = genericDevice(device, systemBus)

    # Connect to Device{Added/Removed} signals
    systemBus.add_signal_receiver(deviceAdded, 'DeviceAdded',  managerName, serviceName, interfaceName)
    systemBus.add_signal_receiver(deviceRemoved, 'DeviceRemoved',  managerName, serviceName, interfaceName)

    ''' Enter main loop '''
    sys.exit(app.exec_loop())

