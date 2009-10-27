from pardus.serviceutils import *

serviceType = "script"
serviceDesc = _({"en": "Serial Port Modifier",
                 "tr": "Seri Port Değiştirici"})

def start():
    try:
        f = file("/etc/serial.conf")
        d = [a.lstrip() for a in f]
        d = filter(lambda x: not (x.startswith("#") or x == ""), d)
        f.close()

        for k in d:
            ret = run("/bin/setserial -b %s" % k)
            if ret != 0:
                fail("Error setting %s" % k)
        notify("System.Service.changed", "started")
    except:
        fail("Unable to start service")

def stop():
    notify("System.Service.changed", "stopped")
