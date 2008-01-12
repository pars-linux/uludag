// Qt DBUS includes
#include "../dbus-qt3-backport/dbus/qdbusconnection.h"
#include "policykitkde.h"

#define POLICYKITKDE_BUSNAME "org.kde.PoliyKit"

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

}

PolicyKitKDE::~PolicyKitKDE()
{

}
