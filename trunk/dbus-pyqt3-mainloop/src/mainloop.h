#ifndef QDBUSCONNECTION_P_H
#define QDBUSCONNECTION_P_H

#include <qguardedptr.h>
#include <qmap.h>
#include <qobject.h>
#include <qvaluelist.h>

#include <dbus/dbus.h>

#include "qdbusatomic.h"
//#include "dbus/qdbuserror.h"
//#include "dbus/qdbusobject.h"

//class QDBusMessage;
class QSocketNotifier;
class QTimer;
class QTimerEvent;

typedef struct DBusConnection;
typedef struct DBusServer;

class QDBusConnectionPrivate: public QObject
{
    Q_OBJECT
public:
    QDBusConnectionPrivate(QObject *parent = 0);
    ~QDBusConnectionPrivate();

//    void bindToApplication();

//    void setConnection(DBusConnection *connection);
//    void setServer(DBusServer *server);
//    void closeConnection();
    void timerEvent(QTimerEvent *e);

//    bool handleSignal(DBusMessage *msg);
//    bool handleObjectCall(DBusMessage *message);
//    bool handleError();

//    void emitPendingCallReply(const QDBusMessage& message);

//signals:
//    void dbusSignal(const QDBusMessage& message);
//    void dbusPendingCallReply(const QDBusMessage& message);

public slots:
    void socketRead(int);
    void socketWrite(int);

//    void objectDestroyed(QObject* object);

    void purgeRemovedWatches();

    void scheduleDispatch();
    void dispatch();

public:
//    DBusError error;
//    QDBusError lastError;

    enum ConnectionMode { InvalidMode, ServerMode, ClientMode };

    // FIXME QAtomic ref;
    Atomic ref;
    //ConnectionMode mode;
    DBusConnection *connection;
//    DBusServer *server;

    QTimer* dispatcher;

//    static int messageMetaType;
//    static int registerMessageMetaType();
//    int sendWithReplyAsync(const QDBusMessage &message, QObject *receiver, const char *method);
    void flush();

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

    typedef QMap<int, DBusTimeout*> TimeoutHash;
    TimeoutHash timeouts;

//    typedef QMap<QString, QDBusObjectBase*> ObjectMap;
//    ObjectMap registeredObjects;

    QValueList<DBusTimeout *> pendingTimeouts;

/*    struct QDBusPendingCall
    {
        QGuardedPtr<QObject> receiver;
        QCString method;
        DBusPendingCall *pending;
    };

    typedef QMap<DBusPendingCall*, QDBusPendingCall*> PendingCallMap;
    PendingCallMap pendingCalls;
*/
};

#endif
