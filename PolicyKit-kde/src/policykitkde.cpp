#include <qapplication.h>
#include <qstring.h>

#include "qdbusconnection.h"

#include "policykitkde.h"
#include "service.h"
#include "debug.h"

PolicyKitKDE::PolicyKitKDE()
{
    //TODO: Reset environment
    //Check for root user

    QDBusConnection connection = QDBusConnection::addConnection(QDBusConnection::SessionBus);
    if (!connection.isConnected())
    {
        Debug::printError("Could not connect to session bus.");
        qApp->quit();
    }

    // try to get a specific service name
    if (!connection.requestName(POLICYKITKDE_BUSNAME))
    {
        Debug::printWarning(QString("Requesting name '%s' failed. "
                 "Will only be addressable through unique name '%s'").arg(POLICYKITKDE_BUSNAME).arg(connection.uniqueName()));
    }
    else
        Debug::printDebug(QString("Requesting name %s successfull").arg(POLICYKITKDE_BUSNAME));

    service = new PolicyService(connection);
}

PolicyKitKDE::~PolicyKitKDE()
{
    delete service;
}
