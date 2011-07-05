# -*- coding: utf-8 -*-
import os, dbus, comar, pisi
import shell_tools

SYS_DIRS = ["dev", "proc", "sys"]

class PardusDbus:
  
    def __init__(self, path):
        self.path = path
        for _dir in SYS_DIRS:
            tgt = os.path.join(path, _dir)
            _dir = os.path.join("/", _dir)
            shell_tools.mount(_dir, tgt, param="--bind")

        shell_tools.chroot_run(path, "/sbin/ldconfig")
        shell_tools.chroot_run(path, "/sbin/update-environment")
        shell_tools.chroot_run(path, "/bin/service dbus start")

        self.socket_file = os.path.join(path, "var/run/dbus/system_bus_socket")

        dbus.bus.BusConnection(address_or_type="unix:path=%s" % self.socket_file)
        self.link = comar.Link(socket=self.socket_file)
        self.baselayout = self.link.User.Manager["baselayout"]

        options = pisi.config.Options()
        options.yes_all = True
        options.ignore_dependency = True
        options.ignore_safety = True
        options.destdir = path

     #   dbus.SystemBus()

        pisi.api.set_dbus_sockname(self.socket_file)
        pisi.api.set_dbus_timeout(1200)
        pisi.api.set_options(options)
        pisi.api.set_comar(True)
        pisi.api.set_signal_handling(False)

    def get_userlist(self):
        users = self.baselayout.userList()
        temp = filter(lambda user: user[0]==0 or 
                          (user[0]>=1000 and user[0]<=65000), users)
        return temp

    def set_userpass(self, uid, password):
        try:
            info = self.baselayout.userInfo(uid)
            if self.baselayout.setUser(uid, info[1], info[3], info[4], password, info[5]):
                return ["message", "The password could not be updated"]
            else:
                return ["message", "The password was updated"]
        except dbus.DBusException as error:
            return ["error", error.message]

    def get_history(self, limit=50):
        pdb = pisi.db.historydb.HistoryDB()
        result = []
        i = 0
        for operation in pdb.get_last():
            # Dont add repo updates to history list
            actions = pisi.operations.history.get_takeback_actions(operation.no)
            if operation.type != 'repoupdate' and len(actions) > 0:
                result.append(operation)
                i += 1
                if i == limit:
                    break
        return result

    def take_back(self, operation):
        # dirty hack for COMAR to find scripts.
        #os.symlink("/", self.path + "/tmp/pisihistory")
        self.link.System.Manager["pisi"].takeBack(operation)

       # pisi.api.takeback(operation)
        #os.unlink(self.path + "/tmp/pisihistory" )

    def get_history_actions(self, number):
        return pisi.operations.history.get_takeback_actions(number)

    def finalize_chroot(self):
        pisi.db.invalidate_caches()

        # stop dbus
        shell_tools.chroot_run(self.path, "/bin/service dbus stop")

        # kill comar in chroot if any exists
        shell_tools.chroot_run(self.path, "/bin/killall comar")

        # unmount sys dirs
        temp = SYS_DIRS
        temp.reverse()
        for _dir in temp:
            tgt = os.path.join(self.path, _dir)
            shell_tools.umount(tgt)

        # swap off if it is opened
        shell_tools.run_quiet("swapoff -a")


