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

#include "device.h"
#include "devicesettingsdlg.h"

class QValidator;

class DeviceSettings : public DeviceSettingsDlg, public Device
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

    void addDns();
    void removeDns();

    void slotStartDhcpcd();

    void slotScanWifi();
    void slotEssidSelected( int );

private:
    QString _dev;
    bool _wifi;
    QValidator *validator;
    void writeSettings();

};

#endif // DEVICE_SETTINGS_H
