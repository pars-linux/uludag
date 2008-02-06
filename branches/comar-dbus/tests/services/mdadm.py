from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "RAID monitor daemon",
                 "tr": "RAID izleme servisi"})
serviceConf = "mdadm"

@synchronized
def start():
    startService(command="mdadm",
                 args="--monitor --scan --daemonise --pid-file /var/run/mdadm.pid %s" % config.get("MDADM_OPTS"),
                 pidfile="/var/run/mdadm.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/mdadm.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/mdadm.pid")
