import os 
po_dir = "po"
prog_dir = "sahip"
setup_file = "setup.py"
digest_dir = "/home/emre/Desktop/sahip-0.1"



os.system("mkdir %s" % digest_dir)
os.system("cp -rf %s %s" % (po_dir, digest_dir))
os.system("cp -rf %s %s" % (prog_dir, digest_dir))
os.system("cp %s %s" % (setup_file, digest_dir))

os.system("rm -rf %s/%s/.svn" % (digest_dir, po_dir))
os.system("rm -rf %s/%s/*.pot" % (digest_dir, po_dir))
os.system("rm -rf %s/%s/*.mo" % (digest_dir, po_dir))
os.system("rm -rf %s/%s/.svn" % (digest_dir, prog_dir))
os.system("rm -rf %s/%s/*.pyc" % (digest_dir, prog_dir))

files_to_delete = []
files = os.listdir(digest_dir+"/"+prog_dir)
for file in files:
	if file[-3:]=='.ui':
		name = file[:-3]
		pyfile = name+".py"
		if pyfile in files:
			files_to_delete.append(digest_dir+"/"+prog_dir+"/"+pyfile)
	elif file[-6:] == '_rc.py':
		files_to_delete.append(digest_dir+"/"+prog_dir+"/"+file)
			
if files_to_delete:
	os.system("rm "+" ".join(files_to_delete))