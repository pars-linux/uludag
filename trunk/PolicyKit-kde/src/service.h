#include "qdbusconnection.h"
#include "qdbusobject.h"

class QStringList;

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

private:
    QDBusConnection m_connection;

private:
    QStringList sortStrings(const QStringList& list);
};

