/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef TULLIANA_BUTTON_H
#define TULLIANA_BUTTON_H

#include <kcommondecoration.h>
#include "tulliana.h"


namespace TullianaWin {

  class TullianaClient;


 class TullianaButton: public KCommonDecorationButton
  {
  Q_OBJECT

  public:
    TullianaButton(ButtonType type, TullianaClient* parent, const char* name);
    ~TullianaButton();

    void reset(unsigned long changed);

    TullianaClient* client() { return _client; }

  private:
    TullianaClient* _client;
  };

    

} // TullianaWin

#endif // TULLIANA_BUTTON_H
