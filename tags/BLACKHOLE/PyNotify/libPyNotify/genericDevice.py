# -*- coding: utf-8 -*-

import dbus

from genericActions import genericActions
from iconFinder import iconFinder

class genericDevice:
    ''' Base class for a generic HAL device '''

    # storage.bus (string)
    storageBus = ['ide', "usb", "ieee1394", "scsi", "sata", "platform"]

    # storage.drive_type (string)
    storageDriveType = ['disk', "cdrom", "floppy", "tape", "compact_flash", 'memory_stick', "smart_media", "sd_mmc"]

    capabilitiesMap = {
        'ac_adapter' : genericActions.popupDialog,
        'alsa' : '',
        'battery' : '',
        'block' : '',
        'bluetooth_hci' : genericActions.popupDialog,
        'button' : '',
        'camera' : '',
        'dvb' : '',
        'fan' : '',
        'hiddev' : '',
        'input' : '',
        'input.joystick' : '',
        'input.keyboard' : '',
        'input.keys' : '',
        'input.mouse' : genericActions.popupDialog,
        'input.tablet' : '',
        'laptop_panel' : '',
        'mmc_host' : '',
        'net' : '', 
        'net.80203' : '',
        'net.80211' : '',
        'oss' : '',
        'pda' : '',
        'portable_audio_player' : '',
        'printer' : '',
        'processor' : '',
        'scsi_generic' : '',
        'scsi_host' : '',
        'serial' : '',
        'storage' : '',
        'tape' : '',
        'usbraw' : '',
        'video4linux' : '',
        'volume' : genericActions.popupDialog,
        'volume.disc' : ''
    }

    def __init__(self, udi, systemBus):
        serviceName = 'org.freedesktop.Hal'
        managerName = 'org.freedesktop.Hal.Device'

        self.udi = udi
        self.device = systemBus.get_object(serviceName, self.udi)
        self.deviceInterface = dbus.Interface(self.device, managerName)
        self.genericActions = genericActions(iconFinder())

        for key in self.deviceInterface.GetAllProperties():
            setattr(self, key.replace('.', "_"), self.deviceInterface.GetProperty(key))

    def __getattr__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]
        else:
            return None

    def deviceAdded(self):
        # Popup for only devices has capabilities
        if not self.info_capabilities:
            return

        for i in self.info_capabilities:
            try:
                if self.capabilitiesMap[i] != '':
                    self.capabilitiesMap[i](self.genericActions, self, 'Device Added To System', "added to system...")
            except KeyError:
                pass

    def deviceRemoved(self):
        # Popup for only devices has capabilities
        if not self.info_capabilities:
            return

        for i in self.info_capabilities:
            try:
                if self.capabilitiesMap[i] != '':
                    self.capabilitiesMap[i](self.genericActions, self, 'Device Removed From System', "removed from system...")
            except KeyError:
                pass

    def propertyModified(self, udi, msg):
        print 'property=%s %s' % (udi, msg)

    def connectPropertyModified(self):
        self.deviceInterface.connect_to_signal('PropertyModified', self.propertyModified)
