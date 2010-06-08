from PyQt4.QtNetwork import QFtp

from logger import getLogger
log = getLogger("FTPDownloader")

class FTPDownloader():
    '''
    ISO downloader via ftp protocol specialized for
    Mirror object.
    '''

    def __init__(self, mirror):
        ftp = QFtp()
        ftp.connectToHost(mirror.hostname)
        if (mirror.login=='true'):
            ftp.login(mirror.username, mirror.password)
        ftp.cd(mirror.path)
        ftp.get(mirror.filename)
        ftp.close() 
        # TODO: need improvement
        
        

from versionmanager import Mirror
m = Mirror()
m.hostname='ftp.pardus.org.tr'
m.login='true'
m.username='anonymous'
m.password='anonymous'
m.port='21'
m.path='pub/pardus/kurulan/2009.1/'
m.filename='Pardus_2009.1_Anthropoides_virgo.iso'

d = FTPDownloader(m)
