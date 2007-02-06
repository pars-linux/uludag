/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef TULLIANA_H
#define TULLIANA_H

#include <kdecoration.h>
#include <kdecorationfactory.h>

namespace TullianaWin {

 class TullianaFactory: public QObject, public KDecorationFactory
  {
  Q_OBJECT

  public:
    TullianaFactory();
    ~TullianaFactory();

    virtual KDecoration* createDecoration(KDecorationBridge*);
    virtual bool reset(unsigned long changed);
    //    static Qt::AlignmentFlags titleAlign();

  private:
    void readConfig();
  };


TullianaFactory* Factory();

} // TullianaWin

#endif // TULLIANA_H
