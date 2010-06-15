#Adapted from ActiveState Code Python Recipe #266486
#see http://code.activestate.com/recipes/266486-simple-md5-sum-utility/
#for more. Removed deprecated md5 package and using hashlib instead.

import hashlib

from logger import getLogger
log = getLogger("MD5sum")

class MD5sum():
    def encryptFile(self, path):
	m = hashlib.md5()

	try:
	    fobj = open(path, 'rb')
	    while fobj:
		d = fobj.read(8096)
		if not d: break
		m.update(d)

	    fobj.close()
	except:
	    log.error('Could not open file at %s' % path)

	return m.hexdigest()