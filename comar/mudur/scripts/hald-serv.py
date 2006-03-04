import os
import socket
import subprocess
import time

def run(*cmd):
    """Run a command without running a shell"""
    return subprocess.call(cmd)

def wait_for_bus(unix_name, retry=10, wait=0.2):
    sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    count = 0
    while count < retry:
        try:
            sock.connect(unix_name)
            return True
        except:
            count += 1
        time.sleep(wait)
    return False

#

def get_state():
    s = get_profile("System.Service.setState")
    if s:
        state = s["state"]
    else:
        state = "on"
    
    return state

#

def info():
    state = get_state()
    return "local\n" + state + "\nHardware Abstraction Layer"

def start():
    call("System.Service.start", "dbus")
    call("System.Service.start", "acpid")
    wait_for_bus("/var/lib/dbus/system_bus_socket")
    run("/sbin/start-stop-daemon", "--start", "-q",
        "--exec", "/usr/sbin/hald", "--", "--retain-privileges")

def stop():
    run("/sbin/start-stop-daemon", "--stop", "-q", "--pidfile", "/var/run/hald.pid")

def ready():
    s = get_state()
    if s == "on":
        start()

def setState(state=None):
    if state == "on":
        start()
    elif state == "off":
        stop()
    else:
        fail("Unknown state '%s'" % state)
