#ifndef SERVICE_H
#define SERVICE_H

#include <polkit/polkit.h>
#include <qobject.h>
#include <qmap.h>
#include <qsocketnotifier.h>

#include "qdbusconnection.h"
#include "qdbusobject.h"

class PolicyService: public QObject, public QDBusObjectBase
{
    Q_OBJECT

public:
    PolicyService(QDBusConnection sessionBus);
    virtual ~PolicyService();

protected:
    bool handleMethodCall(const QDBusMessage& message);
    bool handleIntrospect(const QDBusMessage& message);
    bool handleObtainAuthorization(const QDBusMessage& message);
    void sendDBusError(const QDBusMessage& message, const QString& errortype, const QString& errorstr = "org.freedesktop.DBus.Error.InvalidSignature");
    bool obtainAuthorization(const QString& actionId, const uint wid, const uint pid);

protected slots:
    void slotBusNameOwnerChanged(const QDBusMessage& msg);
    void watchActivated(int fd);

private:
    QDBusConnection m_sessionBus;
    QDBusConnection m_systemBus;

    PolKitContext *m_context;
    PolKitError *m_error;

    bool m_authInProgress;
    static PolicyService* m_self;

    QMap<int, QSocketNotifier*> m_watches;

    static int polkit_add_watch(PolKitContext *context, int fd);
    static void polkit_remove_watch(PolKitContext *context, int fd);
};

#endif
