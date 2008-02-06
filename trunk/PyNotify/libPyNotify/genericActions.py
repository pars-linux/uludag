# -*- coding: utf-8 -*-

import os
import pynotify
import statvfs
import inspect

class genericActions:
    def __init__(self):
        pass

    def popupDialog(self, device, subject, content, urgency = pynotify.URGENCY_NORMAL, timeout = pynotify.EXPIRES_DEFAULT):
        ''' Popups notification dialog '''
        if (0):
            """ FIXME: disabled """
            whoCalledMe = inspect.getframeinfo((inspect.currentframe().f_back))[2]

            print '--------------------------------------------'
            print 'info.product: %s' % device.info_product
            print 'info.category: %s' % device.info_category
            print 'info.capabilities: %s' % device.info_capabilities
            print 'storage.bus: %s' % device.storage_bus
            print 'called from: %s' % whoCalledMe
            print '--------------------------------------------'

        pynotify.init(device.udi)
        n = pynotify.Notification(subject, '<b>%s</b> %s'
                                  % (device.info_product, content),
                                  'file:///home/caglar/workspace/PyNotify/icons/%s.png' % device.info_category)

        n.set_urgency(urgency)
        n.set_timeout(timeout)
        n.show()

    def checkDiskSpace(self):
        """ stupid function for testing """
        def emptyTrash(n, action):
            # os.system('ktrash --empty')
            n.set_timeout(3)
            n.set_urgency(pynotify.URGENCY_NORMAL)
            n.clear_actions() 
            n.update('Trash emptied', 'Trash deleted', 'file:///home/caglar/workspace/PyNotify/icons/trashcan_empty.png')
            n.show()

        def ignoreAction(n, action):
            n.close()

        st = os.statvfs('/')
        a = st[statvfs.F_BSIZE] * st[statvfs.F_BFREE]

        if a < 20 * (1024 * 1024 * 1024):
            pynotify.init('diskFull')
            n = pynotify.Notification('Low disk space',
                              'You can free up some disk space by emptying the trash can.',
                              'file:///home/caglar/workspace/PyNotify/icons/trashcan_full.png')

            n.set_urgency(pynotify.URGENCY_CRITICAL)
            n.set_timeout(0)

            n.add_action('ignore', 'Ignore', ignoreAction)
            n.add_action('empty', 'Empty Trash', emptyTrash)
            n.show()

        return False
