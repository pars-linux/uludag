import os
import ftplib
import getpass
import commands

tarname = "sahip-0.1.tar.gz"
packagedir="/home/emre/svn/paketler/sahip/"
desktop = "/home/emre/Desktop/"
packagepspec=packagedir+"pspec.xml"

os.chdir(desktop)
os.system("tar cfz %s sahip-0.1/"%tarname)  


# FTP
u = getpass.getpass()
p = getpass.getpass()

s = ftplib.FTP('ftp.emrealadag.com', u, p)
s.cwd("www/dosyalar/pardus")
f = open(desktop+tarname)
s.storbinary("STOR "+tarname, f)

f.close()
s.quit()
print "Ftp transmission has ended..."
# ftp end---------

o = commands.getoutput("sha1sum "+ desktop + tarname)
shasum = o.split(" ")[0]
print "Sha1sum : %s" % shasum

#Restoring backup
f = open(packagedir+"yedek.xml")
fw = open(packagepspec,"w")
fw.write(f.read())
fw.close()
f.close()

print "Pspec Restoration finished"


# Update pspec.xml hash
print "Now updating pspec.xml"
output = ""

f = open(packagepspec)
for line in f:
	print line
	if "<Archive sha1sum=" in line:
		toadd = '\n\t\t<Archive sha1sum="%s" type="targz">http://www.emrealadag.com/dosyalar/pardus/sahip-0.1.tar.gz</Archive>\n\t' % shasum
	else:
		toadd = line
	output+=toadd
f.close()
print "Read it"
f = open(packagepspec,"w")
f.write(output)
f.close()
print "Wrote it"
os.chdir(packagedir)
os.system("sudo pisi rm sahip")
os.system("sudo pisi bi pspec.xml -d")
os.system("sudo pisi it sahip-0.1-1.pisi -d")
