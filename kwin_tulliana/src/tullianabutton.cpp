/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/


#include "tullianabutton.h"
#include "tullianabutton.moc"
#include "tullianaclient.h"

namespace TullianaWin {

  TullianaButton::TullianaButton(ButtonType type, TullianaClient* parent, const char* name)
    : KCommonDecorationButton(type, parent, name),
      _client(parent)
  {
    //empty
  }

  
  TullianaButton::~TullianaButton()
  {
    //empty
  }


  void TullianaButton::reset(unsigned long changed)
  {
    //empty
  }
    

} // TullianaWin

