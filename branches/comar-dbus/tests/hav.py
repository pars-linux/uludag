#!/usr/bin/env python

import os
import sys

try:
    import dbus
    import dbus.mainloop.glib
except ImportError:
    print 'python-dbus package is not installed.'
    sys.exit(1)

def printUsage():
    print '''Usage: %(name)s [command] <args>
    
Commands:
  %(name)s call <app> <model> <method> [args]
  %(name)s list-apps [model]
  %(name)s list-models [app]
  %(name)s listen
  %(name)s register <app> <model> <script>
  %(name)s remove <app>
''' % {'name': sys.argv[0]}


def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    try:
        object = bus.get_object('tr.org.pardus.comar', '/system', introspect=False)
        iface = dbus.Interface(object, 'tr.org.pardus.comar')
    except dbus.exceptions.DBusException, e:
        print 'Error:'
        print ' ', e
        return 1

    try:
        cmd = sys.argv[1]
    except IndexError:
        printUsage()
        return 1

    try:
        if cmd == 'call':
            try:
                app = sys.argv[2]
                model = sys.argv[3]
                method = sys.argv[4]
            except IndexError:
                printUsage()
                return 1

            args = []
            if len(sys.argv) > 5:
                args = sys.argv[5:]

            object = bus.get_object('tr.org.pardus.comar', '/package/%s' % app, introspect=False)
            iface = dbus.Interface(object, 'tr.org.pardus.comar.%s' % model)
            call = getattr(iface, method)

            print call(*args)
        elif cmd == 'list-apps':
            try:
                model = sys.argv[2]
            except IndexError:
                for app in iface.listApplications():
                    print app
            else:
                for app in iface.listModelApplications(model):
                    print app
        elif cmd == 'list-models':
            try:
                app = sys.argv[2]
            except IndexError:
                for model in iface.listModels():
                    print model
            else:
                for model in iface.listApplicationModels(app):
                    print model
        elif cmd == 'listen':
            def handleSignal(*args, **kwargs):
                dbus_interface = kwargs['dbus_interface']
                member = kwargs['member']
                if dbus_interface.startswith('tr.org.pardus.comar.'):
                    print '%s.%s - %s' % (dbus_interface, member, args)

            bus.add_signal_receiver(handleSignal, interface_keyword='dbus_interface', member_keyword='member')

            try:
                import gobject
            except ImportError:
                print 'gobject package is not installed.'
                sys.exit(1)

            try:
                loop = gobject.MainLoop()
                loop.run()
            except KeyboardInterrupt:
                return 0
        elif cmd == 'register':
            try:
                app = sys.argv[2]
                model = sys.argv[3]
                script = sys.argv[4]
            except IndexError:
                printUsage()
                return 1
            script = os.path.realpath(script)
            if iface.register(app, model, script):
                print 'Registering %s/%s' % (model, app)
        elif cmd == 'remove':
            try:
                app = sys.argv[2]
            except IndexError:
                printUsage()
                return 1
            if iface.remove(app):
                print 'Removing %s' % app
        else:
            printUsage()
            return 1
    except dbus.exceptions.DBusException, e:
        print 'Error:'
        print ' ', e


if __name__ == '__main__':
    sys.exit(main())
