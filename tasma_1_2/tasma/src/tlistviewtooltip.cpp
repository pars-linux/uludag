/*
  Copyright (c) 2004, 2008 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - tlistviewtooltip.cpp
  Tooltip implementation for listview.
*/

#include "tlistviewtooltip.h"

 TListViewToolTip::TListViewToolTip( QListView* parent , QString comment )
    : QToolTip( parent->viewport() ), listView( parent )
{
	toolTip = comment;
}
 TListViewToolTip::~TListViewToolTip(){
	delete toolTip;
}
 void TListViewToolTip::maybeTip( const QPoint& p ) {
    if ( !listView )
         return;
    const QListViewItem* item = listView->itemAt( p );
    if ( !item )
         return;
    const QRect itemRect = listView->itemRect( item );
    if ( !itemRect.isValid() )
         return;
    const int col = listView->header()->sectionAt( p.x() );
    const QRect headerRect = listView->header()->sectionRect( col );
    if ( !headerRect.isValid() )
         return;
    const QRect cellRect( headerRect.left(), itemRect.top(),
                           headerRect.width(), itemRect.height() );
    QString tipStr;
    tipStr =  toolTip ; 
    tip( cellRect, tipStr );
}
