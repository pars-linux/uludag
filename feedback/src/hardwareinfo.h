/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef HARDWAREINFO_H
#define HARDWAREINFO_H

#include "hardwareinfodlg.h"

class HardwareInfo : public HardwareInfoDlg
{
public:
	HardwareInfo( QWidget *parent = 0, const char* name = 0 );
};

#endif // HARDWAREINFO_H
