#!/bin/bash

qdbusxml2cpp -a exportedconnection -N -i marshalarguments.h -i types.h -i busconnection.h -l BusConnection -c ConnectionAdaptor introspection/nm-exported-connection.xml
qdbusxml2cpp -a exportedconnection -N -i marshalarguments.h -i types.h -i busconnection.h -l BusConnection -c ConnectionAdaptor introspection/nm-exported-connection.xml
qdbusxml2cpp -a exportedconnectionsecrets -N -i marshalarguments.h -i types.h -i busconnection.h -l BusConnection -c SecretsAdaptor introspection/nm-connection-secrets.xml
qdbusxml2cpp -a exportedconnectionsecrets -N -i marshalarguments.h -i types.h -i busconnection.h -l BusConnection -c SecretsAdaptor introspection/nm-connection-secrets.xml
qdbusxml2cpp -N -i types.h -p nm-active-connectioninterface introspection/nm-active-connection.xml
qdbusxml2cpp -N -i types.h -p nm-active-connectioninterface introspection/nm-active-connection.xml
qdbusxml2cpp -i types.h -N -p nm-exported-connectioninterface introspection/nm-exported-connection.xml
qdbusxml2cpp -i types.h -N -p nm-exported-connectioninterface introspection/nm-exported-connection.xml
qdbusxml2cpp -N -i types.h -p nm-settingsinterface introspection/nm-settings.xml
qdbusxml2cpp -N -i types.h -p nm-settingsinterface introspection/nm-settings.xml
qdbusxml2cpp -m -p nm-vpn-connectioninterface introspection/nm-vpn-connection.xml
qdbusxml2cpp -m -p nm-vpn-connectioninterface introspection/nm-vpn-connection.xml

# default name is forbidden as a property name, change it to getDefault
sed -i -e "s,Q_PROPERTY(bool Default READ default),Q_PROPERTY(bool Default READ getDefault)," nm-active-connectioninterface.h
sed -i -e "s,inline bool default() const,inline bool getDefault() const," nm-active-connectioninterface.h
