from PyQt4 import QtCore
import hashlib

import logger
log = logger.getLogger("MD5sum")

class MD5sum():
    "MD5 sum driver class."
    def encryptFile(self, path):
        """Encrypts given file at 'path' parameter.
        Precondition: path is an absolute path to an existing file.
        Returns 32-byte hash string.
        Adapted from ActiveState Code Python Recipe #266486.
        see http://code.activestate.com/recipes/266486-simple-md5-sum-utiliy/
        for more. Removed deprecated md5 package and using hashlib instead.
        """
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

class ThreadedChecksum(QtCore.QThread):
    """
    Threaded checksummer using given checksum engine and file path.
    """

    def __init__(self, cryptEngine, path, callback):
        """Initializes thread with crypt engine, file path and callback method.
        Precondition: Given path is true and an absolute path."""
        QtCore.QThread.__init__(self)
        self.engine = cryptEngine
        self.path = path
        if callable(callback): self.callback = callback

    def run(self):
        """
        Hashes given file at path.
        Postcondition: self.hash has the hash value of the file.
                       self.callback is invoked.
        """
        self.hash = self.engine.encryptFile(self.path)
        self.callback() # upon finish.
        self.exit() # terminate.
