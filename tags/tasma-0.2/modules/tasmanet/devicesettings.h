/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef DEVICE_SETTINGS_H
#define DEVICE_SETTINGS_H

#include "devicesettingsdlg.h"

class QRegExp;
class QValidator;

class DeviceSettings : public DeviceSettingsDlg
{
    Q_OBJECT

public:
    DeviceSettings( QWidget *parent, QString dev, bool wifi );
    ~DeviceSettings();

protected slots:
    void slotApply();
    void slotCancel();

    void slotIPChanged();

    void automaticToggled( bool on );
    void manualToggled( bool on );

    void startDhcpcd();

    void addDns();
    void removeDns();

private:
    QRegExp *rx;
    QValidator *validator;
    QString _dev;
    bool _wifi;
    int sockets_open();
    int set_iface( const char *dev, const char *ip,
		   const char *bc, const char *nm );
    int set_default_route( const char *ip );
    void writeSettings();
    QStringList getDnsList();
    int writeDnsList();

};

#endif // DEVICE_SETTINGS_H
