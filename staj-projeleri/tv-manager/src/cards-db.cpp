/*
  Copyright (c) 2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <QListbox>
#include <QStringList>
#include <KLocale>
#include <KDebug>

extern "C" {
#include "pci.h"
}

#include "cards-db.h"
#include "bttv-cards.h"

CardsDB::CardsDB()
{
    addCards(bttv_cards, BTTV);
}

CardsDB::~CardsDB()
{
    CardVendors::Iterator it;
    for (it = m_vendors.begin(); it != m_vendors.end(); ++it) {
	delete(it.data());
    }
}

void CardsDB::getCards(QString vendor, QStringList *cards)
{
    Cards::ConstIterator it;

    for (it = m_vendors[vendor]->begin(); it != m_vendors[vendor]->end(); it++) {
	cards->append(it->card_name);
    }
}

void CardsDB::getVendors(QStringList *vendors)
{
    CardVendors::ConstIterator it;

    for (it = m_vendors.begin(); it != m_vendors.end(); ++it) {
	vendors->append(it.key());
    }
}

int CardsDB::getCard(QString card_name)
{
    CardVendors::ConstIterator v_it;
    Cards::ConstIterator c_it;

    for (v_it = m_vendors.begin(); v_it != m_vendors.end(); ++v_it) {
	for (c_it = v_it.data()->begin(); c_it != v_it.data()->end(); ++c_it) {
	    if (card_name.compare(c_it->card_name) == 0)
		return c_it->card_id;
	}
    }

    return -1;
}

int CardsDB::getCard(unsigned int card_id, ChipSet chipset, QString &vendor_name, QString &card_name)
{
    CardVendors::ConstIterator v_it;
    Cards::ConstIterator c_it;

    for (v_it = m_vendors.begin(); v_it != m_vendors.end(); ++v_it) {
	for (c_it = v_it.data()->begin(); c_it != v_it.data()->end(); ++c_it) {
	    if (c_it->card_id == card_id && c_it->chipset == chipset) {
		vendor_name = v_it.key();
		card_name = c_it->card_name;
		return card_id;
	    }
	}
    }

    return -1;
}

void CardsDB::addCards(struct card_info *card_infos, ChipSet chipset)
{
    Cards *cards;
    struct Card card;
    struct pci_access *pacc;
    char devbuf[128];

    pacc = pci_alloc();

    for (int i = 0; card_infos[i].card_name != NULL; i++) {

	QString vendor = (card_infos[i].vendor_id == 0xffff ? i18n("Other") : 
			  pci_lookup_name(pacc, devbuf, sizeof(devbuf), PCI_LOOKUP_VENDOR, card_infos[i].vendor_id, 0));

	card.card_id = card_infos[i].card_id;
	card.card_name = card_infos[i].card_name;
	card.chipset = chipset;

	if (!m_vendors.contains(vendor)) {
	    cards = new Cards();
	    m_vendors[vendor] = cards;
	} else {
	    cards = m_vendors[vendor];
	}

	cards->push_back(card);
    }

    pci_cleanup(pacc);
}

