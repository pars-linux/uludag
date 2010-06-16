import commands

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
    os, wmi = None, None

    def __init__(self):

	try:
	    from wmi import wmi
	    self.wmi = wmi.WMI()
	    self.winArchitecture()
	    self.winTotalMemory()
	    self.winPopulateDisks()
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
	if(self.wmi):
	        if(self.wmi.Win32_Processor(Architecture = 0x0)):
		    name = 'x86'
		    bits = 32
		elif(self.wmi.Win32_Processor(Architecture = 0x9)):
		    name = 'x64'
		    bits = 64
		else:
		    name = 'Intel Itanium, MIPS or PowerPC'
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
