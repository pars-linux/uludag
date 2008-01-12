#include <qstringlist.h>
#include <qvariant.h>

#include "qdbuserror.h"
#include "qdbusmessage.h"

#include "service.h"

PolicyService::PolicyService(const QDBusConnection& connection) : m_connection(connection)
{
    m_connection.registerObject("/", this);
}

PolicyService::~PolicyService()
{
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
        QDBusError error(errortype, errorstr);

        qDebug("message: %s, error:%s", errorstr.ascii(), errortype.ascii());
        qWarning("Method call error:%s  Interface:%s Method:%s", errorstr.ascii(), message.interface().ascii(), message.member().ascii());
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

    reply << QVariant(introspection);
    m_connection.send(reply);

    return true;
}

bool PolicyService::handleObtainAuthorization(const QDBusMessage& message)
{
    QDBusMessage reply = QDBusMessage::methodReply(message);

    reply << QVariant(true);
    m_connection.send(reply);

    return true;
}

