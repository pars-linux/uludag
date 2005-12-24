/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - tmodulegroup.cpp
  A KListView item that holds tasma module group.
*/

#include <kservicegroup.h>

#include "tmodulegroup.h"

TModuleGroup::TModuleGroup( KListView *parent, const QString &text,
                            const QPixmap &pix, KServiceGroup *group )
    : KListViewItem( parent, text )
{
    if ( group->isValid() ) {
        _path = group->relPath();
        _icon = group->icon();
        _caption = group->caption();
    }

    setPixmap( 0, pix );
}

TModuleGroup::~TModuleGroup()
{

}

QString TModuleGroup::path() const
{
    return _path;
}

QString TModuleGroup::icon() const
{
    return _icon;
}

QString TModuleGroup::caption() const
{
    return _caption;
}

