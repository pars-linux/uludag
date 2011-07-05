/*
  Copyright (c) 2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef __TUNERS_DB_H__
#define __TUNERS_DB_H__

#include <QMap>
#include <QString>
#include <QObject>
#include <Q3ValueVector>
#include <QStringList>

struct Tuner
{
    unsigned int tuner_id;
    const char *tuner_name;
};

typedef Q3ValueVector<struct Tuner> Tuners;
typedef QMap<QString, Tuners *> TunerVendors;

class TunersDB : public QObject
{
public:
    TunersDB();
    ~TunersDB();
    void getTuners(QString vendor, QStringList *tuners);
    void getVendors(QStringList *vendors);

    int getTuner(QString tuner_name);
    int getTuner(unsigned int tuner_id, QString &vendor_name, QString &tuner_name);

private:
    TunerVendors m_vendors;
    void initVendors();
};

#endif
