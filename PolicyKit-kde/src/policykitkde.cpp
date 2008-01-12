#include "qdbusconnection.h"

#include "policykitkde.h"
#include "service.h"

#define POLICYKITKDE_BUSNAME "org.freedesktop.PolicyKit.AuthenticationAgent"

PolicyKitKDE::PolicyKitKDE()
{
    QDBusConnection connection = QDBusConnection::addConnection(QDBusConnection::SessionBus);
    if (!connection.isConnected())
        qFatal("Cannot connect to session bus");

    // try to get a specific service name
    if (!connection.requestName(POLICYKITKDE_BUSNAME))
    {
        qWarning("Requesting name '%s' failed. "
                 "Will only be addressable through unique name '%s'",
                 POLICYKITKDE_BUSNAME, connection.uniqueName().local8Bit().data());
    }
    else
    {
        qDebug("Requesting name '%s' successfull", POLICYKITKDE_BUSNAME);
    }

    PolicyService *service = new PolicyService(connection);

}

PolicyKitKDE::~PolicyKitKDE()
{

}
