# -*- coding: utf-8 -*-

####################################
#
# Written By : Şükrü BEZEN
#
# Email : sukru@sukrubezen.com
#
####################################

import os, glob, sys

class VT: 
  def lddCheck(self, user, package):
    # check if package is executable or library ? 
    self.ldd_outfile = open("/home/" + user + "/ldd_outfile","w")

    real_package = glob.glob("/var/lib/pisi/package/" + package + "*")[0] + "/"
    real_path = real_package + "files.xml"
    f = open(real_path,"r")
    to_be_searched = f.read()

    self.ldd_outfile.write(package + " paketi için bulunan çıktılar :\n")

    while(1):
      lhs = to_be_searched.find("<Path>")
      if(lhs == -1):
          break
      to_be_searched = to_be_searched[lhs + len("<Path>"):]
      rhs = to_be_searched.find("</Path>")
      _path = to_be_searched[:rhs]
      to_be_searched = to_be_searched[rhs + len("</Path"):]

      #-----------------------------------------------------------------------
      lhs = to_be_searched.find("<Type>")
      to_be_searched = to_be_searched[lhs + len("<Type>"):]
      rhs = to_be_searched.find("</Type>")
      _type = to_be_searched[:rhs]
      to_be_searched = to_be_searched[rhs + len("</Type>"):]

      if(_path[0] != "/"): 
          _path = "/" + _path

      if(_type == "library" or _type == "executable"):
          if(os.path.islink(_path) == False):
              commandLib = os.popen("ldd -u -r " + _path)
              outputLib = commandLib.read()
              self.ldd_outfile.write(_path + " alt dosyasi icin :\n")
              self.ldd_outfile.write(outputLib) 

  def readLddFile(self,user):
     readLddFile = open("/home/" + user + "/ldd_outfile","r")
     outldd = readLddFile.read()
     print "\n" + outldd


lddObject = VT()

if(sys.argv[1] == "start"):
  lddObject.lddCheck(sys.argv[2],sys.argv[3])
elif(sys.argv[1] == "end"):
  lddObject.readLddFile(sys.argv[2])
