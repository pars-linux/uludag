'''
Created on Sep 3, 2009

@author: rcakirerk
'''

from Disk import disk


d = disk()

disk = d.open("sdb")
#d.clear_disk()
#print d.list_partitions()

part = disk.next_partition()

print part