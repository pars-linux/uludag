serviceType = "server"
serviceDesc = _({"en": "Memory Caching Server",
                 "tr": "Hafıza Önbellekleme Sunucusu"})

from pardus.serviceutils import *

@synchronized
def start():
    args = (
        config.get("PORT", "11211"),
        config.get("LISTENON", "127.0.0.1"),
        config.get("MEMUSAGE", "64"),
        config.get("MAXCONN", "1024"),
        config.get("MEMCACHED_RUNAS", "memcached"),
    )
    startService(command="/usr/bin/memcached",
                 args="-d -P /var/run/memcached.pid -p %s -l %s -m %s -c %s -u %s" % args,
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/bin/memcached",
                donotify=True)

def status():
    return isServiceRunning(command="/usr/bin/memcached")
