#include <qapplication.h>
#include <qstring.h>

#include "qdbusconnection.h"

#include "policykitkde.h"
#include "service.h"
#include "debug.h"

PolicyKitKDE::PolicyKitKDE()
{
    QDBusConnection connection = QDBusConnection::addConnection(QDBusConnection::SessionBus);

    if (!connection.isConnected())
    {
        Debug::printError("Could not connect to session bus.");
        qApp->quit();
    }

    // try to get a specific service name
    if (!connection.requestName(POLICYKITKDE_BUSNAME))
        Debug::printWarning(QString("Requesting name '%1' failed, another authentication agent is running already. Will only be addressable through unique name '%2'").arg(POLICYKITKDE_BUSNAME).arg(connection.uniqueName()));
    else
        Debug::printDebug(QString("Requesting name '%1' successfull").arg(POLICYKITKDE_BUSNAME));

    service = new PolicyService(connection);
}

PolicyKitKDE::~PolicyKitKDE()
{
    Debug::printDebug("PolicyKitKDE object deconstructor: Deleting PolicyService");
    delete service;
}
