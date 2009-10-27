serviceType = "script"
serviceDesc = _({"en": "System Resource Accounting Utility",
                 "tr": "Sistem Kaynakları Hesaplama Uygulaması"})

from pardus.serviceutils import *

@synchronized
def start():
    startService(command="/usr/sbin/accton",
                 args=config.get("ACCT_LOG", "/var/account/pacct"),
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/accton",
                args="",
                donotify=True)
