from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "GIT Server",
                 "tr": "GIT Sunucusu"})
serviceDefault = "off"
serviceConf = "git"

@synchronized
def start():
    startService(command="/usr/bin/git-daemon",
                 args="--detach --pid-file=/var/run/git-daemon.pid %s" % config.get("GITDAEMON_OPTS"),
                 pidfile="/var/run/git-daemon.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/git-daemon.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/git-daemon.pid")
