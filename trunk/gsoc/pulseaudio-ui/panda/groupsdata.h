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
#ifndef PANDA_GROUPSDATA_H
#define PANDA_GROUPSDATA_H

#include <kconfig.h>

struct GroupData
{
    QString name;
    QString icon;
};

void save_groups(const QList<GroupData> &groups, KConfig *config);
QList<GroupData> load_groups(KConfig *config);

#endif