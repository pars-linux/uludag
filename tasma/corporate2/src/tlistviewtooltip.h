/*
  Copyright (c) TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef TListViewToolTip_H
#define TListViewToolTip_H
#include <qtooltip.h>
#include <qlistview.h>
#include <qheader.h>

class TListViewToolTip : public QToolTip
{
public:
    TListViewToolTip( QListView* parent, QString comment);
    ~TListViewToolTip();
protected:
    void maybeTip( const QPoint& p );
private:
    QListView* listView;
    QString toolTip;
};

#endif /* TListViewToolTip_H */

