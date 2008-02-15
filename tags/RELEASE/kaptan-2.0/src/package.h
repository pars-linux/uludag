/*
  Copyright (c) 2004,2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef PACKAGE_H
#define PACKAGE_H

#include "packagedlg.h"

class Package:public PackageDlg
{
    Q_OBJECT
public:
    Package(QWidget *parent = 0, const char* name = 0);
    void apply();

protected slots:
    void traySelected(bool);
    void updateSelected(bool);
};

#endif // PACKAGE_H
