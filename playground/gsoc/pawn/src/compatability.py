import psutil

class Compatability():

    totalMemory, architectureBit = None,None

    def __init__(self):
	self.totalMemory = psutil.TOTAL_PHYMEM
	

c=Compatability()
print c.totalMemory