/*
  Copyright (c) 2004, 2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef MOUSE_H
#define MOUSE_H

#include <kapplication.h>

#include "mousedlg.h"

#define RIGHT_HANDED 0
#define LEFT_HANDED  1

class Mouse:public MouseDlg
{
    Q_OBJECT

public:
    Mouse(QWidget *parent = 0, const char* name = 0);
    void apply();

protected slots:
    void setHandedness(int);

private:
    int handed;
};

#endif // MOUSE_H
