#ifndef SERVICE_H
#define SERVICE_H

#include "qdbusconnection.h"
#include "qdbusobject.h"

struct PolKitContext;

class PolicyService: public QDBusObjectBase
{
public:
    PolicyService(QDBusConnection *sessionBus);
    virtual ~PolicyService();

protected:
    bool handleMethodCall(const QDBusMessage& message);
    bool handleIntrospect(const QDBusMessage& message);
    bool handleObtainAuthorization(const QDBusMessage& message);
    void sendDBusError(const QDBusMessage& message, const QString& errortype, const QString& errorstr = "org.freedesktop.DBus.Error.InvalidSignature");
    bool obtainAuthorization(const QString& actionId, const uint wid, const uint pid);

protected slots:
    void slotBusNameOwnerChanged(const QDBusMessage& msg);

private:
    QDBusConnection *m_sessionBus;
    QDBusConnection *m_systemBus;
    PolKitContext *m_context;
    bool m_authInProgress;
};

#endif
