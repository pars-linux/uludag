/*
  Copyright (c) 2004,2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef GOODBYE_H
#define GOODBYE_H

#include "goodbyedlg.h"

class Goodbye:public GoodbyeDlg
{
    Q_OBJECT

public:
    Goodbye(QWidget *parent = 0, const char* name = 0);

protected slots:
    void startTasma();
};

#endif // WELCOME_H
