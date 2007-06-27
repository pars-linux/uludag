import string
import commands
import os

import registry

def getPartitions():
	"get all partitions in the form: '/mnt/hda9'"
	partitions=[]
	df = commands.getoutput("df")
	df = string.split(df,"\n")
	for i in df[1:]:
		i = string.split(i," ")
		partitions.append(i[-1])
	return partitions

def isWindowsPart(partition):
	"check which partitions have windows installed"
	possible_files=["boot.ini","command.com","bootmgr"]
	for a in possible_files:
		if os.path.exists(os.path.join(partition,a)):
			return True
	return False

def getWindowsUsers(partition):
    # User: (partition, parttype, username, userdir)
    
    users = []
    
    possiblehivefiles = ["Windows/System32/config/SOFTWARE", "WINDOWS/system32/config/software"]
    hivefile = ""
    for possiblehivefile in possiblehivefiles:
        possiblehivefile = os.path.join(partition,possiblehivefile)
        if os.path.isfile(possiblehivefile):
            hivefile = possiblehivefile     # registry dosyasi bulundu
            break
    
    if hivefile != "":      # kullanicilari bulmaya calisiyorum
        try:
            hive = registry.Hive(os.path.join(partition,"Windows/System32/config/SOFTWARE"))
            key = hive.getKey("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
            subkeys = key.subKeys()
            for subkey in subkeys:
                key2 = key.getSubKey(subkey)
                path = key2.getValue("ProfileImagePath")
                path = path.split("\\",1)[1]
                path = path.replace("\\", "/")
                path = os.path.join(partition, path)
                if os.path.isfile(os.path.join(path, "NTUSER.DAT")):        # bir kullanici buldum
                    if os.path.isfile(os.path.join(partition, "bootmgr")):
                        users.append((partition, "Windows Vista", os.path.basename(path), path))
                    else:
                        users.append((partition, "Windows XP", os.path.basename(path), path))
        except:     # hata durumunda bir seyler yap
            raise
    
    return users