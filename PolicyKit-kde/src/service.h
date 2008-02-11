#ifndef SERVICE_H
#define SERVICE_H

#include "qdbusconnection.h"
#include "qdbusobject.h"

class PolicyService: public QDBusObjectBase
{
public:
    PolicyService(const QDBusConnection& connection);
    virtual ~PolicyService();

protected:
    virtual bool handleMethodCall(const QDBusMessage& message);
    bool handleIntrospect(const QDBusMessage& message);
    bool handleObtainAuthorization(const QDBusMessage& message);
    void sendDBusError(const QDBusMessage& message, const QString& errortype, const QString& errorstr = "org.freedesktop.DBus.Error.InvalidSignature");
    bool obtainAuthorization(const QString& actionId, const uint wid, const uint pid);

private:
    QDBusConnection m_connection;
};

#endif
