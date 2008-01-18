
#include <dbus/dbus-python.h>
#include <qapplication.h>
#include <qevent.h>
#include <qmetaobject.h>
#include <qsocketnotifier.h>
#include <qtimer.h>

#include "mainloop.h"

QDBusConnectionPrivate::QDBusConnectionPrivate(QObject *parent)
    : QObject(parent), dispatcher(0)
{
    dispatcher = new QTimer(this);
    QObject::connect(dispatcher, SIGNAL(timeout()), this, SLOT(dispatch()));

    connections.setAutoDelete(true);
}

QDBusConnectionPrivate::~QDBusConnectionPrivate()
{
//    if (dbus_error_is_set(&error))
//        dbus_error_free(&error);

//    closeConnection();
}

void QDBusConnectionPrivate::scheduleDispatch()
{
    dispatcher->start(0);
}

void QDBusConnectionPrivate::dispatch()
{
    DBusConnection *con;

    for (con = connections.first(); con; con = connections.next())
    {
        while (dbus_connection_dispatch(con) == DBUS_DISPATCH_DATA_REMAINS);
        dispatcher->stop();
    }
}

void QDBusConnectionPrivate::purgeRemovedWatches()
{
    if (removedWatches.isEmpty()) return;

    WatcherList::iterator listIt = removedWatches.begin();
    for (; listIt != removedWatches.end(); ++listIt)
    {
        delete (*listIt).read;
        delete (*listIt).write;
    }
    removedWatches.clear();

    uint count = 0;
    WatcherHash::iterator it = watchers.begin();
    while (it != watchers.end())
    {
        WatcherList& list = *it;
        listIt = list.begin();
        while (listIt != list.end())
        {
            if (!((*listIt).read) && !((*listIt).write))
            {
                listIt = list.erase(listIt);
                ++count;
            }
        }

        if (list.isEmpty())
        {
            WatcherHash::iterator copyIt = it;
            ++it;
            watchers.erase(copyIt);
        }
        else
            ++it;
    }
}

void QDBusConnectionPrivate::timerEvent(QTimerEvent *e)
{
    DBusTimeout *timeout = timeouts[e->timerId()];
    dbus_timeout_handle(timeout);
}

void QDBusConnectionPrivate::socketWrite(int fd)
{
    WatcherHash::const_iterator it = watchers.find(fd);

    if (it != watchers.end()) 
    {
        const WatcherList& list = *it;

        for (WatcherList::const_iterator wit = list.begin(); wit != list.end(); ++wit) 
        {
            if ((*wit).write && (*wit).write->isEnabled()) 
            {
                (*wit).write->setEnabled(false);
                if (!dbus_watch_handle((*wit).watch, DBUS_WATCH_WRITABLE))
                    qDebug("OUT OF MEM");
                (*wit).write->setEnabled(true);
                break;
            }
        }
    }
}

void QDBusConnectionPrivate::socketRead(int fd)
{
    WatcherHash::const_iterator it = watchers.find(fd);

    if (it != watchers.end())
    {
        const WatcherList& list = *it;

        for (WatcherList::const_iterator wit = list.begin(); wit != list.end(); ++wit) 
        {
            if ((*wit).read && (*wit).read->isEnabled()) 
            {
                (*wit).read->setEnabled(false);
                if (!dbus_watch_handle((*wit).watch, DBUS_WATCH_READABLE))
                    qDebug("OUT OF MEM");
                (*wit).read->setEnabled(true);
                break;
            }
        }
    }

    scheduleDispatch();
}

////////////////// DBUS REQUIREMENTS ////////////////////////////////

extern "C" {static dbus_bool_t qDBusAddTimeout(DBusTimeout *timeout, void *data);}
static dbus_bool_t qDBusAddTimeout(DBusTimeout *timeout, void *data)
{
    Q_ASSERT(timeout);
    Q_ASSERT(data);

  //  qDebug("addTimeout %d", dbus_timeout_get_interval(timeout));

    QDBusConnectionPrivate *d = static_cast<QDBusConnectionPrivate *>(data);

    if (!dbus_timeout_get_enabled(timeout))
        return true;

    if (!qApp) {
        d->pendingTimeouts.append(timeout);
        return true;
    }
    int timerId = d->startTimer(dbus_timeout_get_interval(timeout));
    if (!timerId)
        return false;

    d->timeouts[timerId] = timeout;
    return true;
}

extern "C" {static void qDBusRemoveTimeout(DBusTimeout *timeout, void *data);}
static void qDBusRemoveTimeout(DBusTimeout *timeout, void *data)
{
    Q_ASSERT(timeout);
    Q_ASSERT(data);

  //  qDebug("removeTimeout");

    QDBusConnectionPrivate *d = static_cast<QDBusConnectionPrivate *>(data);
    for (QValueList<DBusTimeout*>::iterator it = d->pendingTimeouts.begin();
         it != d->pendingTimeouts.end();) {
        if ((*it) == timeout) {
            it = d->pendingTimeouts.erase(it);
        }
      else
        ++it;
    }

    QDBusConnectionPrivate::TimeoutHash::iterator it = d->timeouts.begin();
    while (it != d->timeouts.end()) {
        if (it.data() == timeout) {
            d->killTimer(it.key());
            QDBusConnectionPrivate::TimeoutHash::iterator copyIt = it;
            ++it;
            d->timeouts.erase(copyIt);
        } else {
            ++it;
        }
    }
}

extern "C" {static void qDBusToggleTimeout(DBusTimeout *timeout, void *data);}
static void qDBusToggleTimeout(DBusTimeout *timeout, void *data)
{
    Q_ASSERT(timeout);
    Q_ASSERT(data);

    //qDebug("ToggleTimeout");

    qDBusRemoveTimeout(timeout, data);
    qDBusAddTimeout(timeout, data);
}

extern "C" {static dbus_bool_t qDBusAddWatch(DBusWatch *watch, void *data);}
static dbus_bool_t qDBusAddWatch(DBusWatch *watch, void *data)
{
    Q_ASSERT(watch);
    Q_ASSERT(data);

    QDBusConnectionPrivate *d = static_cast<QDBusConnectionPrivate *>(data);

    int flags = dbus_watch_get_flags(watch);
    int fd = dbus_watch_get_unix_fd(watch);

    QDBusConnectionPrivate::Watcher watcher;
    if (flags & DBUS_WATCH_READABLE) {
        bool enabled = dbus_watch_get_enabled(watch);
        //qDebug("addReadWatch %d %s", fd, (enabled ? "enabled" : "disabled"));
        watcher.watch = watch;
        if (qApp) {
            watcher.read = new QSocketNotifier(fd, QSocketNotifier::Read, d);
            if (!enabled) watcher.read->setEnabled(false);
            d->connect(watcher.read, SIGNAL(activated(int)), SLOT(socketRead(int)));
        }
    }
    if (flags & DBUS_WATCH_WRITABLE) {
        bool enabled = dbus_watch_get_enabled(watch);
        //qDebug("addWriteWatch %d %s", fd, (enabled ? "enabled" : "disabled"));
        watcher.watch = watch;
        if (qApp) {
            watcher.write = new QSocketNotifier(fd, QSocketNotifier::Write, d);
            if (!enabled) watcher.write->setEnabled(false);
            d->connect(watcher.write, SIGNAL(activated(int)), SLOT(socketWrite(int)));
        }
    }
    // FIXME-QT4 d->watchers.insertMulti(fd, watcher);
    QDBusConnectionPrivate::WatcherHash::iterator it = d->watchers.find(fd);
    if (it == d->watchers.end())
    {
        it = d->watchers.insert(fd, QDBusConnectionPrivate::WatcherList());
    }
    it.data().append(watcher);

    return true;
}

extern "C" {static void qDBusRemoveWatch(DBusWatch *watch, void *data);}
static void qDBusRemoveWatch(DBusWatch *watch, void *data)
{
    Q_ASSERT(watch);
    Q_ASSERT(data);

    //qDebug("remove watch");

    QDBusConnectionPrivate *d = static_cast<QDBusConnectionPrivate *>(data);
    int fd = dbus_watch_get_unix_fd(watch);

    QDBusConnectionPrivate::WatcherHash::iterator it = d->watchers.find(fd);
    if (it != d->watchers.end())
    {
        QDBusConnectionPrivate::WatcherList& list = *it;
        for (QDBusConnectionPrivate::WatcherList::iterator wit = list.begin();
             wit != list.end(); ++wit)
        {
            if ((*wit).watch == watch)
            {
                // migth be called from a function triggered by a socket listener
                // so just disconnect them and schedule their delayed deletion.

                d->removedWatches.append(*wit);
                if ((*wit).read)
                {
                    (*wit).read->disconnect(d);
                    (*wit).read = 0;
                }
                if ((*wit).write)
                {
                    (*wit).write->disconnect(d);
                    (*wit).write = 0;
                }
                (*wit).watch = 0;
            }
        }
    }

    if (d->removedWatches.count() > 0)
        QTimer::singleShot(0, d, SLOT(purgeRemovedWatches()));
}

extern "C" {static void qDBusToggleWatch(DBusWatch *watch, void *data);}
static void qDBusToggleWatch(DBusWatch *watch, void *data)
{
    Q_ASSERT(watch);
    Q_ASSERT(data);

    //qDebug("toggle watch");

    QDBusConnectionPrivate *d = static_cast<QDBusConnectionPrivate *>(data);
    int fd = dbus_watch_get_unix_fd(watch);

    QDBusConnectionPrivate::WatcherHash::iterator it = d->watchers.find(fd);
    if (it != d->watchers.end()) {
        QDBusConnectionPrivate::WatcherList& list = *it;
        for (QDBusConnectionPrivate::WatcherList::iterator wit = list.begin(); wit != list.end();
             ++wit)
        {
            if ((*wit).watch == watch) {
                bool enabled = dbus_watch_get_enabled(watch);
                int flags = dbus_watch_get_flags(watch);

//                 qDebug("toggle watch %d to %d (write: %d, read: %d)",
//                         dbus_watch_get_unix_fd(watch), enabled,
//                         flags & DBUS_WATCH_WRITABLE, flags & DBUS_WATCH_READABLE);

                if (flags & DBUS_WATCH_READABLE && (*wit).read)
                    (*wit).read->setEnabled(enabled);
                if (flags & DBUS_WATCH_WRITABLE && (*wit).write)
                    (*wit).write->setEnabled(enabled);
                return;
            }
        }
    }
}

// The callback to delete a helper instance.
extern "C" {static void dbus_qt_delete_helper(void *data);}
static void dbus_qt_delete_helper(void *data)
{
    delete reinterpret_cast<QDBusConnectionPrivate *>(data);
}

// The callback to wakeup the event loop.
extern "C" {static void wakeup_main(void *data);}
static void wakeup_main(void *data)
{
    QDBusConnectionPrivate *hlp = reinterpret_cast<QDBusConnectionPrivate *>(data);

    // This all seems to work (with responses coming at the same time as with
    // GLib) but it doesn't seem right.  In effect this is being used as a
    // polling function and the QSocketNotifiers never get fired.
    //if (dbus_connection_get_dispatch_status(hlp->connection) == DBUS_DISPATCH_DATA_REMAINS)

    hlp->scheduleDispatch();
}


// The callback to set up a DBus connection.
extern "C" {static dbus_bool_t dbus_qt_conn(DBusConnection *conn, void *data);}
static dbus_bool_t dbus_qt_conn(DBusConnection *conn, void *data)
{
    bool rc;

    Py_BEGIN_ALLOW_THREADS

    QDBusConnectionPrivate *hlp = reinterpret_cast<QDBusConnectionPrivate *>(data);

    hlp->connections.append(conn);

    if (!dbus_connection_set_watch_functions(conn, qDBusAddWatch, qDBusRemoveWatch, qDBusToggleWatch, data, 0))
        rc = false;
    else if (!dbus_connection_set_timeout_functions(conn, qDBusAddTimeout, qDBusRemoveTimeout, qDBusToggleTimeout, data, 0))
        rc = false;
    else
        rc = true;

    dbus_connection_set_wakeup_main_function(conn, wakeup_main, hlp, 0);

    Py_END_ALLOW_THREADS

    return rc;
}

// The callback to set up a DBus server.
extern "C" {static dbus_bool_t dbus_qt_srv(DBusServer *srv, void *data);}
static dbus_bool_t dbus_qt_srv(DBusServer *srv, void *data)
{
    bool rc;

    Py_BEGIN_ALLOW_THREADS

    if (!dbus_server_set_watch_functions(srv, qDBusAddWatch, qDBusRemoveWatch, qDBusToggleWatch, data, 0))
        rc = false;
    else if (!dbus_server_set_timeout_functions(srv, qDBusAddTimeout, qDBusRemoveTimeout, qDBusToggleTimeout, data, 0))
        rc = false;
    else
        rc = true;

    Py_END_ALLOW_THREADS

    return rc;
}

//////////////////// PYTHON ///////////////////////////////

PyDoc_STRVAR(DBusQtMainLoop__doc__,
"DBusQtMainLoop([set_as_default=False]) -> NativeMainLoop\n"
"\n"
"Return a NativeMainLoop object.\n"
"\n"
"If the keyword argument set_as_default is given and is True, set the new\n"
"main loop as the default for all new Connection or Bus instances.\n");

extern "C" {static PyObject *DBusQtMainLoop(PyObject *, PyObject *args, PyObject *kwargs);}
static PyObject *DBusQtMainLoop(PyObject *, PyObject *args, PyObject *kwargs)
{
    if (PyTuple_Size(args) != 0)
    {
        PyErr_SetString(PyExc_TypeError, "DBusQtMainLoop() takes no positional arguments");
        return 0;
    }

    int set_as_default = 0;
    static char *argnames[] = {"set_as_default", 0};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|i", argnames, &set_as_default))
        return 0;

    QDBusConnectionPrivate *hlp = new QDBusConnectionPrivate;

    PyObject *mainloop = DBusPyNativeMainLoop_New4(dbus_qt_conn, dbus_qt_srv,
                dbus_qt_delete_helper, hlp);

    if (!mainloop)
    {
        delete hlp;
        return 0;
    }

    if (set_as_default)
    {
        PyObject *func = PyObject_GetAttrString(_dbus_bindings_module, "set_default_main_loop");

        if (!func)
        {
            Py_DECREF(mainloop);
            return 0;
        }

        PyObject *res = PyObject_CallFunctionObjArgs(func, mainloop, 0);
        Py_DECREF(func);

        if (!res)
        {
            Py_DECREF(mainloop);
            return 0;
        }

        Py_DECREF(res);
    }

    return mainloop;
}


// The table of module functions.
static PyMethodDef module_functions[] = {
    {"DBusQtMainLoop", (PyCFunction)DBusQtMainLoop, METH_VARARGS|METH_KEYWORDS,
    DBusQtMainLoop__doc__},
    {0, 0, 0, 0}
};

// The module entry point.
PyMODINIT_FUNC initqt3()
{
    // Import the generic part of the Python DBus bindings.
    if (import_dbus_bindings("dbus.mainloop.qt3") < 0)
        return;

    Py_InitModule("qt3", module_functions);
}

#include "mainloop.moc"
