/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include "tulliana.h"
#include "tulliana.moc"
#include "tullianaclient.h"

namespace TullianaWin {

  TullianaFactory::TullianaFactory()
  {
    reset(0);
  }


  TullianaFactory::~TullianaFactory()
  {
    //empty
  }


  bool reset(unsigned long changed)
  {
    //empty
  }


  KDecoration* TullianaFactory::createDecoration(KDecorationBridge* bridge)
  {
    return new TullianaClient(bridge, this);
  }
    

  static TullianaFactory* factory = 0;
  TullianaFactory* Factory()
  {
    return factory;
  }

} // namespace TullianaWin


extern "C"
{
    KDE_EXPORT KDecorationFactory *create_factory()
    {
        TullianaWin::factory = new TullianaWin::TullianaFactory();
        return TullianaWin::factory;
    }
}
