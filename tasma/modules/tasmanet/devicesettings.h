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

class DeviceSettings : public DeviceSettingsDlg
{
    Q_OBJECT

public:
    DeviceSettings( QWidget *parent, QString dev, bool wifi );

protected slots:
    void slotApply();
    void slotCancel();

    void automaticToggled( bool on );
    void manualToggled( bool on );

private:
    QString _dev;
    bool _wifi;
    int sockets_open();
    int set_iface( const char *dev, const char *ip,
		   const char *bc, const char *nm );

};

#endif // DEVICE_SETTINGS_H
