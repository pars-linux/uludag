/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - tmodulecategorylist.h
  TModuleCategoryList: categorized view of module groups.
*/

#ifndef T_MODULE_CATEGORY_LIST_H
#define T_MODULE_CATEGORY_LIST_H

#include <klistview.h>

class KServiceGroup;

class TModuleCategoryList : public KListView
{
    Q_OBJECT

public:
    TModuleCategoryList( QWidget *parent = 0, const char *name = 0 );
    ~TModuleCategoryList();

};

#endif // T_MODULE_CATEGORY_LIST_H
