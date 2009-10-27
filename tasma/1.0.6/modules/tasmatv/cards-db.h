/*
  Copyright (c) 2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef __CARDS_DB_H__
#define __CARDS_DB_H__

#include <qmap.h>
#include <qstring.h>
#include <qobject.h>
#include <qvaluevector.h>
#include <qstringlist.h>

enum ChipSet { BTTV, SAA7134, CX88 };

struct card_info {
  unsigned int vendor_id;
  unsigned int card_id;
  const char *card_name;
};

struct Card
{
    ChipSet chipset;
    unsigned int card_id;
    const char *card_name;
};

typedef QValueVector<struct Card> Cards;
typedef QMap<QString, Cards *> CardVendors;

class CardsDB : public QObject
{
public:
    CardsDB();
    ~CardsDB();
    void addCards(struct card_info *card_infos, ChipSet chipset);
    
    void getCards(QString vendor, QStringList *cards);
    void getVendors(QStringList *vendors);

    int getCard(QString card_name);
    int getCard(unsigned int card_id, ChipSet chipset, QString &vendor_name, QString &card_name);

private:
    CardVendors m_vendors;
};

#endif
