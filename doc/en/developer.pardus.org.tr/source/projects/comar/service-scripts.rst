.. highlightlang:: python

Service Scripts
===============

Service scripts are Python scripts used by ``COMAR`` to manage system services and comes with ``PiSi`` packages. Any System.Service call made to ``COMAR`` (start, stop, info, ...) will be handled by service scripts.
Service script, is a Python file like below. There are three methods. Two for starting and stopping service, one for giving status of service. Implementation of these three scripts is up to package maintainer. However, COMAR API package provides Service API, which contains useful methods for writing service scripts::

    serviceType = "server"
    serviceDesc = _({"en": "Server",
                     "tr": "Sunucu"})

    from comar.service import *

    @synchronized
    def start():
        startService(command="/usr/bin/myserver",
                     args="start",
                     pidfile="/var/run/sunucu.pid",
                     donotify=True)

    @synchronized
    def stop():
        stopService(command="/usr/bin/myserver",
                    args="stop",
                    donotify=True)

    def status():
        return isServiceRunning("/var/run/myserver.pid")

serviceType
-----------

Possible values::

    local   : Local services
    server  : Servers
    script  : Scripts

This value is used to group services only.

serviceDesc
-----------

A service description may include some language options::

    serviceDesc = _({"en": "My Server",
                     "tr": "Sunucum"})

This value is used by System.Service GUIs. ``_()`` is used for localization.

@synchronized Decorator
-----------------------

In boot sequence, service scripts can start other services. To prevent any race condition, ``@synchronized`` decorator should be used.

Service API
===========

startService()
--------------

This method starts the service with given parameters if available.

Arguments::

    command  : Application to execute [str]
    args     : Arguments (optional) [str]
    pidfile  : PID file for application. (optional) [str]
               (Application won't be started if it's already running.)
    makepid  : If application doesn't create any PID file, API creates one. Generally used with ''detach'' argument (optional) [True/False]
    nice     : Niceness of process (optional) [int]
    chuid    : Owner of the process. Format: user:group (optional) [str:str]
    detach   : Fork process (optional) [True/False]
    donotify : Emit a System.Service.changed signal and notify all GUIs (optional) [True/False]
               (This should be used. It's optional because some service scripts start more than one process.)

stopService()
-------------

This method stops the given service.

Arguments::

    pidfile  : PID file of the running process (optional) [str]
    command  : Application to stop (optional) [str]
               (Scans /proc and kills all running applications having that /path/to/name)
    args     : Arguments (To stop application by calling it with an argument) (optional) [str]
               (/proc won't be scanned, <command args> will be executed)
    chuid    : Owner of the process. Format: user:group (optional) [str:str]
    user     : Username associated with process. (optional) [str]
    signalno : Signal to be sent to running process (optional) [int]
    donotify : Emit a System.Service.changed signal and notify all GUIs (optional) [True/False]
               (This should be used. It's optional because some service scripts stop more than one process.)

isServiceRunning()
------------------

This method checks whether or not the given service is running.

Arguments::

    pidfile  : Process ID of the service is kept in this file when running. [str]
    command  : Check processes running this executable. [str]

startDependencies()
-------------------

This method starts the dependent services given as parameter.

Arguments::

    services : A list of dependent service names that will be started. [str]

stopDependencies()
------------------

This method stops the dependent services given as parameter.

Arguments::

    services : A list of dependent service names that will be stopped. [str]

