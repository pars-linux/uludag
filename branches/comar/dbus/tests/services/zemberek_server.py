from pardus.serviceutils import *
import os

serviceType = "local"
serviceDesc = _({"en": "Zemberek Spell Checker",
                 "tr": "Zemberek Yazım Denetimi"})

@synchronized
def start():
    loadEnvironment()

    if not os.environ.has_key("JAVA_HOME"):
        fail("JAVA_HOME is not set")
    javapath = os.environ["JAVA_HOME"]

    os.environ["LC_ALL"] = "tr_TR.UTF-8"
    os.chdir("/opt/zemberek-server")

    startService(command="%s/bin/java" % javapath,
                 args="-DConfigFile=/opt/zemberek-server/config/conf.ini -Djava.library.path=/opt/zemberek-server/lib \
                       -Xverify:none -Xms12m -Xmx14m -jar /opt/zemberek-server/zemberek_server-0.7.jar",
                 detach=True,
                 pidfile="/var/run/zemberek.pid",
                 makepid=True,
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/zemberek.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/zemberek.pid")
