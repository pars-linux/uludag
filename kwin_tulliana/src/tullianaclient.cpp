/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/


#include <klocale.h>
#include "tullianaclient.h"
#include "tullianabutton.h"

namespace TullianaWin {

  TullianaClient::TullianaClient(KDecorationBridge* bridge, KDecorationFactory* factory)
    :KCommonDecoration(bridge, factory)
  {
    //empty
  }


  TullianaClient::~TullianaClient()
  {
    //empty
  }


  QString TullianaClient::visibleName() const
  {
    return i18n("Tulliana");
  }


  QString TullianaClient::defaultButtonsLeft() const
  {
    return "M";
  }


  QString TullianaClient::defaultButtonsRight() const
  {
    return "HIAX";
  }


  KCommonDecorationButton* TullianaClient::createButton(ButtonType type)
  {
    switch(type)
      {
      case MenuButton:
	return new TullianaButton(MenuButton, this, "menu");

      case OnAllDesktopsButton:
	return new TullianaButton(OnAllDesktopsButton, this, "on_all_desktops");

      case HelpButton:
	return new TullianaButton(HelpButton, this, "help");

      case MinButton:
	return new TullianaButton(MinButton, this, "minimize");

      case MaxButton:
	return new TullianaButton(MaxButton, this, "maximize");

      case CloseButton:
	return new TullianaButton(CloseButton, this, "close");

      case AboveButton:
	return new TullianaButton(AboveButton, this, "above");
	
      case BelowButton:
	return new TullianaButton(BelowButton, this, "below");

      case ShadeButton:
	return new TullianaButton(ShadeButton, this, "shade");

      default:
	return 0;
      }
  }


  void paintEvent(QPaintEvent* e)
  {
    // empty (test)
  }


} // TullianaWin

