#ifndef QDBUSCONNECTION_P_H
#define QDBUSCONNECTION_P_H

#include <qmap.h>
#include <qptrlist.h>
#include <qobject.h>
#include <qvaluelist.h>

#include <dbus/dbus.h>

class QSocketNotifier;
class QTimer;
class QTimerEvent;

typedef struct DBusConnection;

class QDBusConnectionPrivate: public QObject
{
    Q_OBJECT

public:
    QDBusConnectionPrivate(QObject *parent = 0);
    ~QDBusConnectionPrivate();
    void timerEvent(QTimerEvent *e);

public slots:
    void socketRead(int);
    void socketWrite(int);

    void purgeRemovedWatches();

    void scheduleDispatch();
    void dispatch();

public:

    QTimer* dispatcher;

    struct Watcher
    {
        Watcher(): watch(0), read(0), write(0) {}
        DBusWatch *watch;
        QSocketNotifier *read;
        QSocketNotifier *write;
    };

    typedef QValueList<Watcher> WatcherList;
    WatcherList removedWatches;

    typedef QMap<int, WatcherList> WatcherHash;
    WatcherHash watchers;

    typedef QPtrList<DBusConnection>Connections;
    Connections connections;

    typedef QMap<int, DBusTimeout*> TimeoutHash;
    TimeoutHash timeouts;

    QValueList<DBusTimeout *> pendingTimeouts;

};

#endif
