# -*- coding: utf-8 -*-

from shellTools import run_quiet

def installGrub(pardusDisk,option):
  
  root_path = "(%s,%s)" % (pardusDisk[0], pardusDisk[1])
  if option == 0:
    setupto = "(%s)" % pardusDisk[0]
  elif option == 1:
    setupto = "(%s,%s)" % (pardusDisk[0], pardusDisk[1]) 
  elif option == 2:
    setupto = "(%s)" % pardusDisk[2]
	
  batch_template = """root %s
setup %s
quit
""" % (root_path, setupto)

  fd =  file('/tmp/_grub','w')
  fd.write(batch_template)
  fd.close()
        
        
  #run_quiet("grup -no-floppy --batch < /tmp/_grub")
    
def installWindowsBootLoader(windows):
    run_quiet("./install-mbr  -i n -p D -t  %d %s"%(windows[1],windows[0]))