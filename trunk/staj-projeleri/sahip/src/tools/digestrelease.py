"""
Copies program, po files and setup.py to a new directory,
cleans the unnecessary files (.svn, mo, pot, ui.py, rc.py)
"""

import os 
po_dir = "po"
prog_dir = "sahip"
setup_file = "setup.py"
digest_dir = "/home/%s/Desktop/sahip-0.1" %  os.getenv("USER")

# Remove disgest dir.
if os.path.exists(digest_dir):
	os.system("sudo rm -rf %s" % digest_dir)

os.system("mkdir %s" % digest_dir)				# Create digest dir
os.system("cp -rf %s %s" % (po_dir, digest_dir))		# Copy po dir
os.system("cp -rf %s %s" % (prog_dir, digest_dir))		# Copy program dir
os.system("cp %s %s" % (setup_file, digest_dir))		# Copy setup.py file

os.system("rm -rf %s/%s/.svn" % (digest_dir, po_dir))		# Remove .svn dir in po dir
os.system("rm -rf %s/%s/*.pot" % (digest_dir, po_dir))		# Remove pot file
os.system("rm -rf %s/%s/*.mo" % (digest_dir, po_dir))		# Remove mo files

os.system("rm -rf %s/%s/.svn" % (digest_dir, prog_dir))		# Remove .svn dir in program dir
os.system("rm -rf %s/%s/*.pyc" % (digest_dir, prog_dir))	# Remove pyc files in program dir

files_to_delete = []						# Additional check for gui->py files.
files = os.listdir(digest_dir+"/"+prog_dir)			# List program files.
for file in files:
	if file[-3:]=='.ui':					# For each ui file,
		name = file[:-3]
		pyfile = name+".py"
		if pyfile in files:				# If there's a corresponding py file,
								# Mark it to be deleted.
			files_to_delete.append(digest_dir+"/"+prog_dir+"/"+pyfile)
	elif file[-6:] == '_rc.py':				# Else If file is a resource py file,
								# Also mark it.
		files_to_delete.append(digest_dir+"/"+prog_dir+"/"+file)
			
if files_to_delete:						# If there are files to delete,
	os.system("rm "+" ".join(files_to_delete))		# Delete all of them
