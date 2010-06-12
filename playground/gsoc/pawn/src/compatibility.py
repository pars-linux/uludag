import psutil, commands

from logger import getLogger
log = getLogger("Compatibility")

class LogicalDisk():
    DeviceID, FreeSpace, Size = None, 0, 0

    def __init__(self, id, free, size):
	self.DeviceID = id
	self.FreeSpace = free
	self.Size = size

    def __repr__(self):
	return 'Disk: '+' '.join(map(str, (self.DeviceID, self.FreeSpace, self.Size)))
	

class Compatibility():

    totalMemory, architectureBit, architectureName = None, None, None
    disks = []
    os, wmi = None, None

    def __init__(self):
	self.getTotalMemory()

	try:
	    import wmi
	    self.wmi = wmi.WMI()
	    self.winArchitectureBit()
	    self.winPopulateDisks()
	except (NameError, ImportError) as e:
	    # TODO: Windows systems without WMI (ME, 98, NT, 3.1 checks)
	    self.wmi = None
	    self.unixArchitectureBit()
	    self.unixPopulateDisks()

	log.info('Running on %d bit (%s).' % (self.architectureBit,self.architectureName))

    def winArchitectureBit(self):
	if(self.wmi):
	        if(wmiDriver.Win32_Processor(Architecture = 0x0)):
		    name = 'x86'
		    bits = 32
		elif(wmiDriver.Win32_Processor(Architecture = 0x9)):
		    name = 'x64'
		    bits = 64
		else:
		    name = 'Intel Itanium, MIPS or PowerPC'
		    bits = 32

		self.architectureBit, self.architectureName = result, name
		self.os = 'Windows'

    def unixArchitectureBit(self):
	out = commands.getstatusoutput('grep lm /proc/cpuinfo')[1] #if lm exists x64.

	if(out):
	    name = 'x64'
	    bits = 64
	else:
	    name = 'x86'
	    bits = 32

	self.architectureBit, self.architectureName = bits, name

	self.os = 'Windows'

    def getTotalMemory(self):
	self.totalMemory = psutil.TOTAL_PHYMEM # cross-platform
	return self.totalMemory


    def winPopulateDisks(self):
	self.disks = []
	for disk in wmiDriver.Win32_LogicalDisk(DriveType=3):
	    self.disks.append(LogicalDisk(DeviceID, disk.FreeSpace, disk.Size))# #Caption, Size, FreeSpace, FileSystem


    def unixPopulateDisks(self):
	self.disks = []
	for disk in commands.getstatusoutput('df --block-size=1')[1].split('\n')[1:]:
	    p=disk.split()
	    name = p[0]
	    free = long(p[3])
	    size = long(p[2])+long(p[3])
	    self.disks.append(LogicalDisk(name,free,size))