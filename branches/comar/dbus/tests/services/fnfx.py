from pardus.serviceutils import *

serviceType = "local"
serviceDesc = _({"en": "fnfx Daemon",
                 "tr": "fnfx Sunucusu"})

@synchronized
def start():
    reply = run("/sbin/modprobe toshiba_acpi")
    if reply != 0:
        fail("cannot load toshiba acpi module")
    
    startService(command="/usr/sbin/fnfxd",
                 pidfile="/var/run/fnfxd.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/usr/sbin/fnfxd",
                donotify=True)

def status():
    return isServiceRunning("/var/run/fnfxd.pid")
