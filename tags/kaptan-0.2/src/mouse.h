/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef MOUSE_H
#define MOUSE_H

#include <kapplication.h>

#include "mousesetupdlg.h"

#define RIGHT_HANDED 0
#define LEFT_HANDED  1

class MouseSetup : public MouseSetupDlg
{
    Q_OBJECT

public:
    MouseSetup( QWidget *parent = 0, const char* name = 0 );
    ~MouseSetup();

    void apply();
    void save();

private:
    void setHandedness( int val );
    int handed;

private slots:
    void slotLeftHanded() { setHandedness( LEFT_HANDED ); }
    void slotRightHanded() { setHandedness( RIGHT_HANDED ); };

};

#endif // MOUSE_H
