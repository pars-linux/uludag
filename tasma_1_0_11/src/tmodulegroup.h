/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - tmodulegroup.h
  A KListView item that holds tasma module group.
*/

#ifndef T_MODULE_GROUP_H
#define T_MODULE_GROUP_H

#include <klistview.h>

class KServiceGroup;

class TModuleGroup : public KListViewItem
{

 public:
  TModuleGroup( KListView *parent, const QString &text,
                const QPixmap &pix, KServiceGroup *group );

  ~TModuleGroup();

  QString path() const;
  QString icon() const;
  QString caption() const;

 private:
  QString _path;
  QString _icon;
  QString _caption;
};

#endif // T_MODULE_GROUP_H
