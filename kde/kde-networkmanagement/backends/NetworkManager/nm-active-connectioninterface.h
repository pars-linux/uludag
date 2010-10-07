/*
 * This file was generated by qdbusxml2cpp version 0.7
 * Command line was: qdbusxml2cpp -N -i types.h -p nm-active-connectioninterface introspection/nm-active-connection.xml
 *
 * qdbusxml2cpp is Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
 *
 * This is an auto-generated file.
 * Do not edit! All changes made to it will be lost.
 */

#ifndef NM_ACTIVE_CONNECTIONINTERFACE_H
#define NM_ACTIVE_CONNECTIONINTERFACE_H

#include <QtCore/QObject>
#include <QtCore/QByteArray>
#include <QtCore/QList>
#include <QtCore/QMap>
#include <QtCore/QString>
#include <QtCore/QStringList>
#include <QtCore/QVariant>
#include <QtDBus/QtDBus>
#include "types.h"

/*
 * Proxy class for interface org.freedesktop.NetworkManager.Connection.Active
 */
class OrgFreedesktopNetworkManagerConnectionActiveInterface: public QDBusAbstractInterface
{
    Q_OBJECT
public:
    static inline const char *staticInterfaceName()
    { return "org.freedesktop.NetworkManager.Connection.Active"; }

public:
    OrgFreedesktopNetworkManagerConnectionActiveInterface(const QString &service, const QString &path, const QDBusConnection &connection, QObject *parent = 0);

    ~OrgFreedesktopNetworkManagerConnectionActiveInterface();

    Q_PROPERTY(QDBusObjectPath Connection READ connection)
    inline QDBusObjectPath connection() const
    { return qvariant_cast< QDBusObjectPath >(property("Connection")); }

    Q_PROPERTY(bool Default READ getDefault)
    inline bool getDefault() const
    { return qvariant_cast< bool >(property("Default")); }

    Q_PROPERTY(bool Default6 READ default6)
    inline bool default6() const
    { return qvariant_cast< bool >(property("Default6")); }

    Q_PROPERTY(QList<QDBusObjectPath> Devices READ devices)
    inline QList<QDBusObjectPath> devices() const
    { return qvariant_cast< QList<QDBusObjectPath> >(property("Devices")); }

    Q_PROPERTY(QString ServiceName READ serviceName)
    inline QString serviceName() const
    { return qvariant_cast< QString >(property("ServiceName")); }

    Q_PROPERTY(QDBusObjectPath SpecificObject READ specificObject)
    inline QDBusObjectPath specificObject() const
    { return qvariant_cast< QDBusObjectPath >(property("SpecificObject")); }

    Q_PROPERTY(uint State READ state)
    inline uint state() const
    { return qvariant_cast< uint >(property("State")); }

    Q_PROPERTY(bool Vpn READ vpn)
    inline bool vpn() const
    { return qvariant_cast< bool >(property("Vpn")); }

public Q_SLOTS: // METHODS
Q_SIGNALS: // SIGNALS
    void PropertiesChanged(const QVariantMap &properties);
};

#endif
