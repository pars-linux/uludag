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