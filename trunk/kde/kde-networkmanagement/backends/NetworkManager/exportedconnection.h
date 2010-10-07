/*
 * This file was generated by qdbusxml2cpp version 0.7
 * Command line was: qdbusxml2cpp -a exportedconnection -N -i marshalarguments.h -i types.h -i busconnection.h -l BusConnection -c ConnectionAdaptor introspection/nm-exported-connection.xml
 *
 * qdbusxml2cpp is Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
 *
 * This is an auto-generated file.
 * This file may have been hand-edited. Look for HAND-EDIT comments
 * before re-generating it.
 */

#ifndef EXPORTEDCONNECTION_H
#define EXPORTEDCONNECTION_H

#include <QtCore/QObject>
#include <QtDBus/QtDBus>
#include "marshalarguments.h"
#include "types.h"
#include "busconnection.h"
class QByteArray;
template<class T> class QList;
template<class Key, class Value> class QMap;
class QString;
class QStringList;
class QVariant;

/*
 * Adaptor class for interface org.freedesktop.NetworkManagerSettings.Connection
 */
class ConnectionAdaptor: public QDBusAbstractAdaptor
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "org.freedesktop.NetworkManagerSettings.Connection")
    Q_CLASSINFO("D-Bus Introspection", ""
"  <interface name=\"org.freedesktop.NetworkManagerSettings.Connection\">\n"
"    <tp:docstring>\n"
"            Represents a single network connection configuration.\n"
"        </tp:docstring>\n"
"    <method name=\"Update\">\n"
"      <tp:docstring>\n"
"            Update the connection with new settings and properties, replacing all previous settings and properties.\n"
"          </tp:docstring>\n"
"      <annotation value=\"impl_exported_connection_update\" name=\"org.freedesktop.DBus.GLib.CSymbol\"/>\n"
"      <annotation value=\"\" name=\"org.freedesktop.DBus.GLib.Async\"/>\n"
"      <arg direction=\"in\" type=\"a{sa{sv}}\" name=\"properties\">\n"
"        <annotation value=\"QVariantMapMap\" name=\"com.trolltech.QtDBus.QtTypeName.In0\"/>\n"
"        <tp:docstring>\n"
"              New connection properties.\n"
"            </tp:docstring>\n"
"      </arg>\n"
"    </method>\n"
"    <method name=\"Delete\">\n"
"      <tp:docstring>\n"
"            Delete the connection.\n"
"          </tp:docstring>\n"
"      <annotation value=\"impl_exported_connection_delete\" name=\"org.freedesktop.DBus.GLib.CSymbol\"/>\n"
"      <annotation value=\"\" name=\"org.freedesktop.DBus.GLib.Async\"/>\n"
"    </method>\n"
"    <method name=\"GetSettings\">\n"
"      <tp:docstring>\n"
"                Get the settings maps describing this object.\n"
"            </tp:docstring>\n"
"      <annotation value=\"impl_exported_connection_get_settings\" name=\"org.freedesktop.DBus.GLib.CSymbol\"/>\n"
"      <arg direction=\"out\" tp:type=\"String_String_Variant_Map_Map\" type=\"a{sa{sv}}\" name=\"settings\">\n"
"        <annotation value=\"QVariantMapMap\" name=\"com.trolltech.QtDBus.QtTypeName.Out0\"/>\n"
"        <tp:docstring>\n"
"                    The nested settings maps describing this object.\n"
"                </tp:docstring>\n"
"      </arg>\n"
"    </method>\n"
"    <signal name=\"Updated\">\n"
"      <tp:docstring>\n"
"                Emitted when some settings changed.\n"
"            </tp:docstring>\n"
"      <arg tp:type=\"String_String_Variant_Map_Map\" type=\"a{sa{sv}}\" name=\"settings\">\n"
"        <annotation value=\"QVariantMapMap\" name=\"com.trolltech.QtDBus.QtTypeName.In0\"/>\n"
"        <tp:docstring>\n"
"                    Contains complete connection setting parameters, including changes.\n"
"                </tp:docstring>\n"
"      </arg>\n"
"    </signal>\n"
"    <signal name=\"Removed\">\n"
"      <tp:docstring>\n"
"                Emitted when this connection has been deleted/removed.  After receipt of this signal, the object no longer exists.\n"
"            </tp:docstring>\n"
"    </signal>\n"
"  </interface>\n"
        "")
public:
    ConnectionAdaptor(BusConnection *parent);
    virtual ~ConnectionAdaptor();

    inline BusConnection *parent() const
    { return static_cast<BusConnection *>(QObject::parent()); }

public: // PROPERTIES
public Q_SLOTS: // METHODS
    void Delete();
    QVariantMapMap GetSettings();
    void Update(const QVariantMapMap &properties);
Q_SIGNALS: // SIGNALS
    void Removed();
    void Updated(const QVariantMapMap &settings);
};

#endif
