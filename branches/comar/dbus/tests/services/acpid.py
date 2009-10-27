from pardus.serviceutils import *

serviceType = "local"
serviceDesc = _({"en": "ACPI Daemon",
                 "tr": "ACPI Sunucusu"})
serviceDefault = "on"

def check_config():
    import os
    if not os.path.exists("/proc/acpi"):
        fail("ACPI support has not been found")

@synchronized
def start():
    check_config()
    startService(command="/usr/sbin/acpid",
                 args="-c /etc/acpi/events",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/acpid",
                donotify=True)

def reload():
    import signal
    stopService(command="/usr/sbin/acpid",
                signal=signal.SIGHUP)

def status():
    return isServiceRunning(command="/usr/sbin/acpid")
