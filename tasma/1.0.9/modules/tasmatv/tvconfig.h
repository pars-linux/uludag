/*
  Copyright (c) 2005-2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef TV_CONFIG_H
#define TV_CONFIG_H

#include <kdialog.h>

#include "tvconfigui.h"
#include "cards-db.h"
#include "tuners-db.h"

#define AUTO_TUNER  4

class TvConfig : public TvConfigUI
{
    Q_OBJECT

public:
    TvConfig(QWidget *parent);
    ~TvConfig();

    void loadModule();
    void removeModule();
    void saveOptions();

    void tunerVendorChanged();
    void tvVendorChanged();

    void selectCard(int card_id);
    void selectTuner(int tuner_id);

private:
    void setCard(int card_id);
    void setTuner(int tuner_id);
    int getCard();
    int getTuner();

    CardsDB cardsDB;
    TunersDB tunersDB;
};

#endif // TV_CONFIG_H
