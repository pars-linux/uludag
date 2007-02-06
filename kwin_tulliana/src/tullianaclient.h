/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef TULLIANA_CLIENT_H
#define TULLIANA_CLIENT_H

#include <kcommondecoration.h>
#include "tulliana.h"

namespace TullianaWin {

 class TullianaClient: public KCommonDecoration
  {

  public:
    TullianaClient(KDecorationBridge* bridge, KDecorationFactory* factory);
    ~TullianaClient();

    virtual QString visibleName() const;
    virtual QString defaultButtonsLeft() const;
    virtual QString defaultButtonsRight() const;

    virtual KCommonDecorationButton* createButton(ButtonType type);

    virtual void paintEvent(QPaintEvent* e);
  };

} // TullianaWin

#endif // TULLIANA_CLIENT_H
