from pardus.serviceutils import *

serviceType="server"
serviceDesc = _({"en": "MySQL Database Server",
                 "tr": "MySQL Veritabanı Sunucusu"})

def check_mysql():
    import os.path
    if not os.path.exists("/var/lib/mysql"):
        fail("MySQL is not installed")

@synchronized
def start():
    check_mysql()
    startService(command="/usr/sbin/mysqld",
                 pidfile="/var/run/mysqld/mysqld.pid",
                 detach=True,
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/mysqld/mysqld.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/mysqld/mysqld.pid")
