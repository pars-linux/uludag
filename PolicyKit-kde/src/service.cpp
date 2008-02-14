#include <qvariant.h>

//policykit header
#include <polkit/polkit.h>
#include <polkit-dbus/polkit-dbus.h>

//backport headers
#include "qdbuserror.h"
#include "qdbusmessage.h"

#include "service.h"
#include "authdialog.h"
#include "debug.h"

PolicyService::PolicyService(const QDBusConnection& connection) : m_connection(connection)
{
    Debug::printDebug("Registering object: /");
    m_connection.registerObject("/", this);
}

PolicyService::~PolicyService()
{
    Debug::printDebug("Unregistering object: /");
    m_connection.unregisterObject("/");
}

bool PolicyService::handleMethodCall(const QDBusMessage& message)
{
    if (message.interface() == "org.freedesktop.DBus.Introspectable" && message.member() == "Introspect")
    {
        if (message.count() != 0)
        {
            sendDBusError(message, "No argument expected");
            return false;
        }

        else
            return handleIntrospect(message);
    }

    if (message.interface() == "org.freedesktop.PolicyKit.AuthenticationAgent" && message.member() == "ObtainAuthorization")
    {
        if (message.count() != 3 || message[0].type() != QVariant::String || message[1].type() != QVariant::UInt || message[2].type() != QVariant::UInt)
        {
            sendDBusError(message, "Wrong signature, three arguments expected: (String, UINT, UINT)");
            return false;
        }

        else
            return handleObtainAuthorization(message);
    }

    return false;
}

void PolicyService::sendDBusError(const QDBusMessage& message, const QString& errorstr, const QString& errortype)
{
        Debug::printError(QString("Method call error:'%1'  Interface:'%2' Method:'%3'").arg(errorstr).arg(message.interface()).arg(message.member()));

        QDBusError error(errortype, errorstr);
        QDBusMessage reply = QDBusMessage::methodError(message, error);

        m_connection.send(reply);
}

bool PolicyService::handleIntrospect(const QDBusMessage& message)
{
    QDBusMessage reply = QDBusMessage::methodReply(message);

    QString introspection = ""
"<!DOCTYPE node PUBLIC \"-//freedesktop//DTD D-BUS Object Introspection 1.0//EN\"\n"
"\"http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd\">\n"
"<node>\n"
"   <interface name=\"org.freedesktop.DBus.Introspectable\">\n"
"       <method name=\"Introspect\">\n"
"           <arg name=\"xml_data\" type=\"s\" direction=\"out\" />\n"
"       </method>\n"
"   </interface>\n"
"   <interface name=\"org.freedesktop.PolicyKit.AuthenticationAgent\">\n"
"       <method name=\"ObtainAuthorization\" >\n"
"           <!-- IN: PolicyKit action identifier; see PolKitAction -->\n"
"           <arg direction=\"in\" type=\"s\" name=\"action_id\" />\n"
"           <!-- IN: X11 window ID for the top-level X11 window the dialog will be transient for. -->\n"
"           <arg direction=\"in\" type=\"u\" name=\"xid\" />\n"
"           <!-- IN: Process ID to grant authorization to -->\n"
"           <arg direction=\"in\" type=\"u\" name=\"pid\" />\n"
"           <!-- OUT: whether the user gained the authorization -->\n"
"           <arg direction=\"out\" type=\"b\" name=\"gained_authorization\" />\n"
"       </method>\n"
"   </interface>\n"
"</node>";

    Debug::printDebug("Handling introspect() call");
    reply << QVariant(introspection);
    m_connection.send(reply);

    return true;
}

bool PolicyService::handleObtainAuthorization(const QDBusMessage& message)
{
    QDBusMessage reply = QDBusMessage::methodReply(message);

    Debug::printDebug("Handling obtainAuthorization() call");

    bool auth = obtainAuthorization(message[0].toString(), message[1].toUInt(), message[2].toUInt());
    reply << QVariant(auth);

    m_connection.send(reply);

    return true;
}

bool PolicyService::obtainAuthorization(const QString& actionId, const uint wid, const uint pid)
{
    PolKitError *error = NULL;

    PolKitContext* context = polkit_context_new();
    polkit_context_set_load_descriptions(context);
    if (!polkit_context_init (context, &error))
    {
        if (polkit_error_is_set(error))
        {
            Debug::printError(QString("Could not initialize polkit: %1").arg(polkit_error_get_error_message(error)));
        }
        else
            Debug::printError("Could not initialize polkit.");

        return false;
    }

    PolKitAction *action = polkit_action_new();
    if (action == NULL)
    {
        Debug::printError("Could not create new action.");
        return false;
    }

    polkit_bool_t setActionResult = polkit_action_set_action_id(action, actionId.ascii());
    if (!setActionResult)
    {
        Debug::printError("Could not set actionid.");
        return false;
    }

    Debug::printDebug("Getting policy cache...");
    PolKitPolicyCache *cache = polkit_context_get_policy_cache(context);
    if (cache == NULL)
    {
        Debug::printWarning("Could not get policy cache.");
    //    return false;
    }

    Debug::printDebug("Getting policy cache entry for an action...");
    PolKitPolicyFileEntry *entry = polkit_policy_cache_get_entry(cache, action);
    if (entry == NULL)
    {
        Debug::printWarning("Could not get policy entry for action.");
    //    return false;
    }

    Debug::printDebug("Getting action message...");
    const char *message = polkit_policy_file_entry_get_action_message(entry);
    if (message == NULL)
    {
        Debug::printWarning("Could not get action message for action.");
    //    return false;
    }
    else
    {
        Debug::printDebug(QString("Message of action: '%1'").arg(message));
    }

    DBusError dbuserror;
    dbus_error_init (&dbuserror);
    DBusConnection *bus = dbus_bus_get (DBUS_BUS_SYSTEM, &dbuserror);
    if (bus == NULL) 
    {
        Debug::printError("Could not connect to system bus.");
        return false;
    }

    PolKitCaller *caller = polkit_caller_new_from_pid(bus, pid, &dbuserror);
    if (caller == NULL)
    {
        QDBusError *qerror = new QDBusError((const DBusError *)&dbuserror);
        Debug::printError(QString("Could not define caller from pid: %1").arg(qerror->message()));
        return false;
    }

    PolKitResult polkitresult;

    polkitresult = polkit_context_is_caller_authorized(context, action, caller, false, &error);
    if (polkit_error_is_set (error))
    {
        Debug::printError("Could not determine if caller is authorized for this action.");
        return false;
    }

    //TODO: Determine AdminAuthType, user, group...

    try
    {
        AuthDialog* dia = new AuthDialog(message, polkitresult);
        dia->show();
    }
    catch (QString exc)
    {
        Debug::printError(exc);
        return false;
    }

    // check again if user is authorized
    polkitresult = polkit_context_is_caller_authorized(context, action, caller, false, &error);
    if (polkit_error_is_set (error))
    {
        Debug::printError("Could not determine if caller is authorized for this action.");
        return false;
    }

    return false;
}
