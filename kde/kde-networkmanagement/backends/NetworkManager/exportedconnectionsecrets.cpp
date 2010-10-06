/*
 * This file was generated by qdbusxml2cpp version 0.7
 * Command line was: qdbusxml2cpp -a exportedconnectionsecrets -N -i marshalarguments.h -i types.h -i busconnection.h -l BusConnection -c SecretsAdaptor introspection/nm-connection-secrets.xml
 *
 * qdbusxml2cpp is Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
 *
 * This is an auto-generated file.
 * Do not edit! All changes made to it will be lost.
 */

#include "exportedconnectionsecrets.h"
#include <QtCore/QMetaObject>
#include <QtCore/QByteArray>
#include <QtCore/QList>
#include <QtCore/QMap>
#include <QtCore/QString>
#include <QtCore/QStringList>
#include <QtCore/QVariant>

/*
 * Implementation of adaptor class SecretsAdaptor
 */

SecretsAdaptor::SecretsAdaptor(BusConnection *parent)
    : QDBusAbstractAdaptor(parent)
{
    // constructor
    setAutoRelaySignals(true);
}

SecretsAdaptor::~SecretsAdaptor()
{
    // destructor
}

QVariantMapMap SecretsAdaptor::GetSecrets(const QString &setting_name, const QStringList &hints, bool request_new, const QDBusMessage & message)
{
    // handle method call org.freedesktop.NetworkManagerSettings.Connection.Secrets.GetSecrets
    return parent()->GetSecrets(setting_name, hints, request_new, message);
}

