
/*
    Copyright (c) 2009      by Marcin Kurczych          <tharkang@gmail.com>

    *************************************************************************
    *                                                                       *
    * This program is free software; you can redistribute it and/or modify  *
    * it under the terms of the GNU General Public License as published by  *
    * the Free Software Foundation; either version 2 of the License, or     *
    * (at your option) any later version.                                   *
    *                                                                       *
    *************************************************************************
*/
#ifndef PANDA_RULESDATA_H
#define PANDA_RULESDATA_H

#include <QString>
#include <QList>
#include <kconfig.h>

struct RuleData
{
    QString key;
    QString value;
    QString group;
    QString name;
};

void save_rules(const QList<RuleData> &rules, KConfig *config);
QList<RuleData> load_rules(KConfig *config);

#endif