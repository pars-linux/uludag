serviceType = "server"
serviceDesc = _({"en": "Cyrus-SASL Daemon",
                 "tr": "Cyrus-SASL Sunucusu"})
serviceConf = "saslauthd"

from pardus.serviceutils import *

@synchronized
def start():
    startService(command="/usr/sbin/saslauthd",
                 args=config.get("SASLAUTHD_OPTS", ""),
                 pidfile="/var/lib/sasl2/saslauthd.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/lib/sasl2/saslauthd.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/lib/sasl2/saslauthd.pid")
