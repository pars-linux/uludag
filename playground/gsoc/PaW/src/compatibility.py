import commands
import platform

from logger import getLogger
log = getLogger("Compatibility")

class LogicalDisk():
    DeviceID, FreeSpace, Size, Path = None, 0, 0, None

    def __init__(self, id, free, size, path = None):
	self.DeviceID = id
	self.FreeSpace = free
	self.Size = size
	self.Path = path

    def __repr__(self):
	return 'Disk: '+' '.join(map(str, (self.DeviceID, self.FreeSpace, self.Size, self.Path)))


class Compatibility():

    totalMemory, architectureBit, architectureName = None, None, None
    disks = []
    OS, wmi = None, None

    def __init__(self):

	try:
	    from wmi import wmi
	    self.wmi = wmi.WMI()
            self.winTotalMemory()
	    self.winPopulateDisks()
	    self.winArchitecture()
            self.OS = self.wmi.Win32_OperatingSystem()[0] # for .SystemDrvie
	    log.debug('Running on Windows.')
	except (NameError, ImportError):
	    log.debug('Running on Linux.')
	    # TODO: Windows systems without WMI (ME, 98, NT, 3.1 checks)
	    self.wmi = None
	    self.unixTotalMemory()
	    self.unixArchitecture()
	    self.unixPopulateDisks()

	log.debug('Running on %d bit (%s).' % (self.architectureBit,self.architectureName))

    def winArchitecture(self):
        """
        Notice: Takes almost 2.5 seconds on my avg laptop running Win 7.
        Considerably slower than all other WMI operations. May take longer on
        older PCs.
        """
        # TODO: Still causes performance bottleneck, find alternative.
	if(self.wmi):
	        if(self.wmi.Win32_Processor(Architecture = 0x9)):
		    name = 'x64'
		    bits = 64
                else:
		    name = 'x32'
		    bits = 32

		self.architectureBit, self.architectureName = bits, name
		self.os = 'Windows'

    def unixArchitecture(self):
	out = commands.getstatusoutput('grep lm /proc/cpuinfo')[1] #if lm exists x64.

	if(out):
	    name = 'x64'
	    bits = 64
	else:
	    name = 'x86'
	    bits = 32

	self.architectureBit, self.architectureName = bits, name

	self.os = 'Windows'

    def unixTotalMemory(self):
	file = open('/proc/meminfo')
	if file:
	    self.totalMemory = long(file.read().split('\n')[0].split()[1])*1024
	    #\n splitting lines of /proc/meminfo
	    #[0] is MemTotal:   123123123 kB line.
	    #.split()[1] gets 123123123 part
	    #1024 for kb to byte conversion
	file.close()

    def winTotalMemory(self):
	cs = self.wmi.Win32_ComputerSystem()
	totalMemory = None
	for o in cs:
	    if o.TotalPhysicalMemory != None:
		totalMemory = long(o.TotalPhysicalMemory.encode('utf8'))
		break

	self.totalMemory = totalMemory

    def winPopulateDisks(self):
	self.disks = []
	for disk in self.wmi.Win32_LogicalDisk(DriveType=3):
	    self.disks.append(LogicalDisk(str(disk.DeviceID.encode('utf8')), long(disk.FreeSpace), long(disk.Size), str(disk.DeviceID.encode('utf8'))))# #Caption, Size, FreeSpace, FileSystem


    def unixPopulateDisks(self):
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
#            wmi.WMI().Win32_OperatingSystem()[0].Version

        try:
            return platform.version().split('.')[0]
        except:
            return 0
