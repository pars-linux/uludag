#include "qdbusconnection.h"

#include "policykitkde.h"
#include "service.h"

PolicyKitKDE::PolicyKitKDE()
{
    //TODO: Reset environment
    //Check for root user

    QDBusConnection connection = QDBusConnection::addConnection(QDBusConnection::SessionBus);
    if (!connection.isConnected())
        qFatal("Cannot connect to session bus.");

    // try to get a specific service name
    if (!connection.requestName(POLICYKITKDE_BUSNAME))
    {
        qWarning("Requesting name '%s' failed. "
                 "Will only be addressable through unique name '%s'",
                 POLICYKITKDE_BUSNAME, connection.uniqueName().local8Bit().data());
    }
    else
    {
        qDebug("DEBUG: Requesting name '%s' successfull", POLICYKITKDE_BUSNAME);
    }

    service = new PolicyService(connection);
}

PolicyKitKDE::~PolicyKitKDE()
{
    delete service;
}
