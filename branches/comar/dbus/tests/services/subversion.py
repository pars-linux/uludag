from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "SVN Server",
                 "tr": "SVN Sunucusu"})
serviceConf = "svnserve"

@synchronized
def start():
    import os
    if not os.path.exists("/var/svn"):
        run("/usr/bin/svnadmin create /var/svn")

    startService(command="/usr/bin/svnserve",
                 args="--foreground --daemon %s" % config.get("SVNSERVE_OPTS", "--root=/var/svn"),
                 chuid="%s:%s" % (config.get("SVNSERVE_USER", "apache"), config.get("SVNSERVE_GROUP", "apache")),
                 detach=True,
                 pidfile="/var/run/svnserve.pid",
                 makepid=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/svnserve.pid")

def status():
    return isServiceRunning("/var/run/svnserve.pid")
