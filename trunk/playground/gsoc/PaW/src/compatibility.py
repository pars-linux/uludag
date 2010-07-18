import sys
import commands
import platform
import ctypes

import logger
log = logger.getLogger("Compatibility")

# TODO: Write an wrapper class for CD, LogicalDisk and USB.
class LogicalDisk():
    "Class for harddisk partitions."

    DeviceID, Name, FreeSpace, Size, FileSystem = None, None, 0, 0, None
    
    def __init__(self, id, name, free, size, filesystem = None):
	self.DeviceID = id
        self.Name = name
	self.FreeSpace = free
	self.Size = size
	self.FileSystem = filesystem # TODO: redundant? maybe for initrd?

    def __repr__(self):
	return 'Disk: '+' '.join(map(str, (self.DeviceID, self.Name, self.FreeSpace, self.Size)))

class CD():
    "Class for CD/DVD-ROM devices."

    DeviceID, Name, FreeSpace, Size = None, None, 0, 0

    def __init__(self, id, name, free = 0, size = 0):
	self.DeviceID = id
        self.Name = name
	self.FreeSpace = free
	self.Size = size

    def __repr__(self):
	return 'CD: '+' '.join(map(str, (self.DeviceID, self.Name, self.FreeSpace, self.Size)))

class USB():
    "Class for USB devices."

    DeviceID, Name, FreeSpace, Size = None, None, 0, 0
    
    def __init__(self, id, name, free = 0, size = 0):
	self.DeviceID = id
        self.Name = name
	self.FreeSpace = free
	self.Size = size

    def __repr__(self):
	return 'USB: '+' '.join(map(str, (self.DeviceID, self.Name, self.FreeSpace, self.Size)))






class Compatibility():
    """A class that handles many OS operations such as rebooting,
    determining CPU arch, CD/DVD-ROMs, USB drives, harddisk partitions. etc.
    """
    totalMemory, architectureBit, architectureName = None, 0, None
    disks, cds, usbs = [], [], []
    OS, wmi = None, None

    def __init__(self):
        """
        Initializes WMI object.
        Forces to determine CPU architecture and total physical memory.
        """
	try:
	    from tools.wmi import wmi
            self.wmi = wmi.WMI(privileges=["Shutdown"]) # priv. to reboot.
            log.debug('Running on Windows.')
            self.winTotalMemory()
	    self.winArchitecture()
            self.OS = self.wmi.Win32_OperatingSystem()[0] # for .SystemDrvie
	except ImportError as e:
	    log.error('Could not execute WMI: %s' % e)
            sys.exit(1)
	    # TODO: Windows systems without WMI (ME, 98, NT, 3.1 checks)
	    self.wmi = None
            # TODO: Linux populate CDs

	log.debug('Running on %d bit (%s).' % (self.architectureBit,self.architectureName))

    def winArchitecture(self):
        """
        Finds CPU arch on Windows systems on Win 2000 or newer.
        
        Notice: Takes almost 2.5 seconds on an avg laptop running Win 7.
        Considerably slower than all other WMI operations. May take longer on
        older PCs.
        
        Postcondition: self.architectureBit, self.architecturename,
                       self.os updated.
        """
        # TODO: Still causes performance bottleneck, find alternative.
	if(self.wmi):
	        if(self.wmi.Win32_Processor(Architecture = 0x9)):
		    name = 'x86_64'
		    bits = 64
                else:
		    name = 'x86'
		    bits = 32

		self.architectureBit, self.architectureName = bits, name
		self.os = 'Windows'

#    def unixArchitecture(self):
#        """
#        Finds CPU arch on unix systems.
#        Postcondition: self.architectureBit, self.architecturename,
#                       self.os updated.
#        """
#	out = commands.getstatusoutput('grep lm /proc/cpuinfo')[1] #if lm exists x64.
#
#	if(out):
#	    name = 'x64'
#	    bits = 64
#	else:
#	    name = 'x86'
#	    bits = 32
#
#	self.architectureBit, self.architectureName = bits, name
#
#	self.os = 'Linux'
#
#    def unixTotalMemory(self):
#        """
#        Finds total physical memory on unix systems by parsing /proc/meminfo.
#        Postcondition: self.totalMemory is in bytes.
#        """
#	file = open('/proc/meminfo')
#	if file:
#	    self.totalMemory = long(file.read().split('\n')[0].split()[1])*1024
#	    #\n splitting lines of /proc/meminfo
#	    #[0] is MemTotal:   123123123 kB line.
#	    #.split()[1] gets 123123123 part
#	    #1024 for kb to byte conversion
#	file.close()

    def winTotalMemory(self):
        """
        Finds total physical memory on Windows.
        Postcondition: self.totalMemory is in bytes.
        """
	cs = self.wmi.Win32_ComputerSystem()
	totalMemory = None
	for o in cs: # CPU loop.
	    if o.TotalPhysicalMemory != None:
		totalMemory = long(o.TotalPhysicalMemory.encode('utf8'))
		break # There may be additional CPU's. Break on first.

	self.totalMemory = totalMemory

    def winPopulateDisks(self):
        """
        Finds hdd partitions and creates collection of instances in self.disks.
        Note: Only the partitions can be seen under My Computer are detected.
        For example, WinRE(rescue) or Unix partitions (ext3, ext4, squashfs)
        will not be detected due to WMI.
        
        Postcondition: self.disks has hard drive partitions.
        """
	self.disks = []
	for disk in self.wmi.Win32_LogicalDisk(DriveType=3):
	    self.disks.append(LogicalDisk(str(disk.DeviceID.encode('utf8')), str(disk.VolumeName.encode('utf8')), long(disk.FreeSpace), long(disk.Size), str(disk.FileSystem.encode('utf8'))))# Caption, Size, VolumeName, FreeSpace, FileSystem

    def winPopulateCDs(self):
        """
        Finds CD/DVD-ROM drives and creates CD object collections in self.cds.
        """
	self.cds = []
	for cd in self.wmi.Win32_LogicalDisk(DriveType=5):
            # TODO: TBD: First 2 letters of combobox is drive letter + colon.
            # This may fail in the future.
            DeviceID, VolumeName, Size, FreeSpace = None, None, 0, 0
            if hasattr(cd, 'DeviceID') and cd.DeviceID: DeviceID = str(cd.DeviceID.encode('utf8'))
            if hasattr(cd, 'VolumeName') and cd.VolumeName: VolumeName = str(cd.VolumeName.encode('utf8'))
            if hasattr(cd, 'FreeSpace') and cd.FreeSpace: FreeSpace = long(cd.FreeSpace) or 0
            if hasattr(cd, 'Size') and cd.Size: Size = long(cd.Size) or 0

            self.cds.append(CD(DeviceID, VolumeName, FreeSpace,Size)) # Caption, Size, VolumeName, FreeSpace

    def winPopulateUSBs(self):
        "Finds USB drives and creates CD object collections in self.usbs"
        from time import time as t
	self.usbs = []
	for usb in self.wmi.Win32_LogicalDisk(DriveType=2):
            # TODO: TBD: First 2 letters of combobox is drive letter + colon.
            # This may fail in the future.
            DeviceID, VolumeName, Size, FreeSpace = None, None, 0, 0
            if hasattr(usb, 'DeviceID') and usb.DeviceID: DeviceID = str(usb.DeviceID.encode('utf8'))
            if hasattr(usb, 'VolumeName') and usb.VolumeName: VolumeName = str(usb.VolumeName.encode('utf8'))
            if hasattr(usb, 'FreeSpace') and usb.FreeSpace: FreeSpace = long(usb.FreeSpace) or 0
            if hasattr(usb, 'Size') and usb.Size: Size = long(usb.Size) or 0

            self.usbs.append(USB(DeviceID, VolumeName, FreeSpace,Size)) # Caption, Size, VolumeName, FreeSpace
            
    def unixPopulateDisks(self):
        """
        Finds harddisk partitions on unix and populates self.disks with
        collection of LogicalDisk instances.
        """
	self.disks = []
	for disk in commands.getstatusoutput('df --block-size=1')[1].split('\n')[1:]:
	    #--block-size=1  for getting result in bytes
	    #[1] for .getstatusoutput returns [int status, str output]
	    #\n separates each logical disk
	    #[1:] for removing description line from df output.

	    p=disk.split()
	    name = p[0]
	    free = long(p[3])
	    size = long(p[2])+long(p[3])
	    path = str(p[5])

	    self.disks.append(LogicalDisk(name,free,size, path))

    def winMajorVersion(self):
        """
        Returns major versions for Microsoft(tm) Windows(r) family.
        In fact, just returns v from v.m.b version sequence.
        Here are a few:
            0: Unknown, undetermined.
            1: Windows 1.0
            2: Windows 2.0
            3: Windows 3.0, NT 3.1
            4: Windows 95, Windows 98, Windows Me
            5: Windows 2000, Windows XP, Windows Server 2003
            6: Windows Vista, Windows 7

        Notice: WMI is slower than platform.version here.
        """
#        Alternative:
#            str(wmi.WMI().Win32_OperatingSystem()[0].Version.encode('utf8'))
        try:
            return int(platform.version().split('.')[0])
        except:
            return 0

    def isAdministrator(self):
        "Returns true if the user of the program has administrator privileges."
        return bool(ctypes.windll.shell32.IsUserAnAdmin())

    def reboot(self):
        """
        Reboots the computer immediately by sending command to primary OS
        via WMI.
        """
        self.wmi.Win32_OperatingSystem(Primary=1)[0].Reboot()