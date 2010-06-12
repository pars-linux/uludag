import psutil

class Compatibility():

    totalMemory, architectureBit = None,None

    def __init__(self)
	self.totalMemory = psutil.TOTAL_PHYMEM
	
	

c=Compatibility()
print c.totalMemory