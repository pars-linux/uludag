/*
  Copyright (c) 2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <QListWidget>
#include <QStringList>
#include <KLocale>
#include <KDebug>

extern "C" {
#include "pci.h"
}

#include "tuners-db.h"

static struct TUNER {
  unsigned int vendor_id;
  unsigned int tuner_id;
  const char *tuner_name;
} card_tuners[] = {
  {0x1114, 0, "Temic PAL (4002 FH5)" },
  {0x1131, 1, "Philips PAL_I (FI1246 and compatibles)" },
  {0x1131, 2, "Philips NTSC (FI1236,FM1236 and compatibles)" },
  {0x1131, 3, "Philips (SECAM+PAL_BG) (FI1216MF, FM1216MF, FR1216MF)" },
  {0xffff, 4, "NoTuner" },
  {0x1131, 5, "Philips PAL_BG (FI1216 and compatibles)" },
  {0x1114, 6, "Temic NTSC (4032 FY5)" },
  {0x1114, 7, "Temic PAL_I (4062 FY5)" },
  {0x1114, 8, "Temic NTSC (4036 FY5)" },
  {0x10e9, 9, "Alps HSBH1" },
  {0x10e9, 10, "Alps TSBE1" },
  {0x10e9, 11, "Alps TSBB5" },
  {0x10e9, 12, "Alps TSBE5" },
  {0x10e9, 13, "Alps TSBC5" },
  {0x1114, 14, "Temic PAL_BG (4006FH5)" },
  {0x10e9, 15, "Alps TSCH6" },
  {0x1114, 16, "Temic PAL_DK (4016 FY5)" },
  {0x1131, 17, "Philips NTSC_M (MK2)" },
  {0x1114, 18, "Temic PAL_I (4066 FY5)" },
  {0x1114, 19, "Temic PAL* auto (4006 FN5)" },
  {0x1114, 20, "Temic PAL_BG (4009 FR5) or PAL_I (4069 FR5)" },
  {0x1114, 21, "Temic NTSC (4039 FR5)" },
  {0x1114, 22, "Temic PAL/SECAM multi (4046 FM5)" },
  {0x1131, 23, "Philips PAL_DK (FI1256 and compatibles)" },
  {0x1131, 24, "Philips PAL/SECAM multi (FQ1216ME)" },
  {0x1854, 25, "LG PAL_I+FM (TAPC-I001D)" },
  {0x1854, 26, "LG PAL_I (TAPC-I701D)" },
  {0x1854, 27, "LG NTSC+FM (TPI8NSR01F)" },
  {0x1854, 28, "LG PAL_BG+FM (TPI8PSB01D)" },
  {0x1854, 29, "LG PAL_BG (TPI8PSB11D)" },
  {0x1114, 30, "Temic PAL* auto + FM (4009 FN5)" },
  {0x13bd, 31, "SHARP NTSC_JP (2U5JF5540)" },
  {0x1099, 32, "Samsung PAL TCPM9091PD27" },
  {0xffff, 33, "MT20xx universal" },
  {0x1114, 34, "Temic PAL_BG (4106 FH5)" },
  {0x1114, 35, "Temic PAL_DK/SECAM_L (4012 FY5)" },
  {0x1114, 36, "Temic NTSC (4136 FY5)" },
  {0x1854, 37, "LG PAL (newer TAPC series)" },
  {0x1131, 38, "Philips PAL/SECAM multi (FM1216ME MK3)" },
  {0x1854, 39, "LG NTSC (newer TAPC series)" },
  {0xffff, 40, "HITACHI V7-J180AT" },
  {0x1131, 41, "Philips PAL_MK (FI1216 MK)" },
  {0x1131, 42, "Philips 1236D ATSC/NTSC daul in" },
  {0x1131, 43, "Philips NTSC MK3 (FM1236MK3 or FM1236/F)" },
  {0x1131, 44, "Philips 4 in 1 (ATI TV Wonder Pro/Conexant)" },
  {0x1851, 45, "Microtune 4049 FM5" },
  {0xffff, 46, "Panasonic VP27s/ENGE4324D" },
  {0x1854, 47, "LG NTSC (TAPE series)" },
  {0xffff, 48, "Tenna TNF 8831 BGFF)" },
  {0x1851, 49, "Microtune 4042 FI5 ATSC/NTSC dual in" },
  {0xffff, 50, "TCL 2002N" },
  {0x1131, 51, "Philips PAL/SECAM_D (FM 1256 I-H3)" },
  {0xffff, 52, "Thomson DDT 7610 (ATSC/NTSC)" },
  {0x1131, 53, "Philips FQ1286" },
  {0xffff, 54, "tda8290+75" },
  {0x1854, 55, "LG PAL (TAPE series)" },
  {0x1131, 56, "Philips PAL/SECAM multi (FQ1216AME MK4)" },
  {0x1131, 57, "Philips FQ1236A MK4" },
  {0xffff, 58, "Ymec TVision TVF-8531MF/8831MF/8731MF" },
  {0xffff, 59, "Ymec TVision TVF-5533MF" },
  {0xffff, 60, "Thomson DDT 7611 (ATSC/NTSC)" },
  {0xffff, 61, "Tena TNF9533-D/IF/TNF9533-B/DF" },
  {0x1131, 62, "Philips TEA5767HN FM Radio" },
  {0x1131, 63, "Philips FMD1216ME MK3 Hybrid Tuner" },
  {0x1854, 64, "LG TDVS-H062F/TUA6034" },
  {0xffff, 65, "Ymec TVF66T5-B/DFF" },
  {0x1854, 66, "LG NTSC (TALN mini series)" },
  {0, 0, NULL }
};

TunersDB::TunersDB()
{
    initVendors();
}

TunersDB::~TunersDB()
{
    TunerVendors::Iterator it;
    for (it = m_vendors.begin(); it != m_vendors.end(); ++it) {
	delete(it.value());
    }
}

void TunersDB::getTuners(QString vendor, QStringList *tuners)
{
    Tuners::ConstIterator it;

    for (it = m_vendors[vendor]->begin(); it != m_vendors[vendor]->end(); it++) {
	tuners->append(it->tuner_name);
    }
}

void TunersDB::getVendors(QStringList *vendors)
{
    TunerVendors::ConstIterator it;

    for (it = m_vendors.begin(); it != m_vendors.end(); ++it) {
	vendors->append(it.key());
    }
}

int TunersDB::getTuner(QString tuner_name)
{
    TunerVendors::ConstIterator v_it;
    Tuners::ConstIterator t_it;

    for (v_it = m_vendors.begin(); v_it != m_vendors.end(); ++v_it) {
	for (t_it = v_it.value()->begin(); t_it != v_it.value()->end(); ++t_it) {
	    if (tuner_name.compare(t_it->tuner_name) == 0)
		return t_it->tuner_id;
	}
    }

    return -1;
}

int TunersDB::getTuner(unsigned int tuner_id, QString &vendor_name, QString &tuner_name)
{
    TunerVendors::ConstIterator v_it;
    Tuners::ConstIterator t_it;
    
    for (v_it = m_vendors.begin(); v_it != m_vendors.end(); ++v_it) {
	for (t_it = v_it.value()->begin(); t_it != v_it.value()->end(); ++t_it) {
	    if (t_it->tuner_id == tuner_id) {
		vendor_name = v_it.key();
		tuner_name = t_it->tuner_name;
		return tuner_id;
	    }
	}
    }

    return -1;
}

void TunersDB::initVendors()
{
    Tuners *tuners;
    struct Tuner tuner;
    struct pci_access *pacc;
    char devbuf[128];

    pacc = pci_alloc();

    for (int i = 0; card_tuners[i].tuner_name != NULL; i++) {

	QString vendor = (card_tuners[i].vendor_id == 0xffff ? i18n("Other") : 
			  pci_lookup_name(pacc, devbuf, sizeof(devbuf), PCI_LOOKUP_VENDOR, card_tuners[i].vendor_id, 0));

	tuner.tuner_id = card_tuners[i].tuner_id;
	tuner.tuner_name = card_tuners[i].tuner_name;

	if (!m_vendors.contains(vendor)) {
	    tuners = new Tuners();
	    m_vendors[vendor] = tuners;
	} else {
	    tuners = m_vendors[vendor];
	}

	tuners->push_back(tuner);
    }

    pci_cleanup(pacc);
}

