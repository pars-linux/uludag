from pardus.serviceutils import *
import os

serviceType = "local"
serviceDesc = _({"en": "Ejabberd Jabber Server",
                 "tr": "Ejabberd Jabber Sunucusu"})

@synchronized
def start():
    loadEnvironment()

    # Use more than 1024 connections... (~6MB more memory will be used)
    os.environ["ERL_MAX_PORTS"] = "32000"

    startService(command="/usr/bin/erl",
                 args="-pa /usr/lib/erlang/lib/ejabberd-1.1.3/ebin \
                       -sname ejabberd \
                       -s ejabberd \
                       -ejabberd config \"/etc/jabber/ejabberd.cfg\" \
                                 log_path \"/var/log/jabber/ejabberd.log\" \
                       -mnesia dir \"/var/lib/jabber/spool\" \
                       -kernel inetrc \"/etc/jabber/inetrc\" \
                       -detached",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/ejabberdctl",
                args="ejabberd@localhost stop",
                donotify=True)

def status():
    ret = run("/usr/sbin/ejabberdctl ejabberd@localhost status")
    if ret != 0:
        return False
    return True
