/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - tmodulecategorylist.cpp
  TModuleCategoryList implementation.
  Gathering module group informations and viewing them in a categorized way
  (in a listview).
*/

// visible widgets
#include <kicontheme.h>
#include <kiconloader.h>
#include <qheader.h> // klistview->header()

// kservice goodies
#include <kservicegroup.h>

#include "tmodulegroup.h"
#include "tmodulecategorylist.h"

TModuleCategoryList::TModuleCategoryList( QWidget *parent, const char *name )
  : KListView( parent, name )
{
  addColumn(  QString::null );
  setSizePolicy(  QSizePolicy(  QSizePolicy::Maximum,
                                QSizePolicy::Preferred ) );
  header()->hide();

  QPixmap _icon = DesktopIcon(  "go",  KIcon::SizeMedium ); // defaultIcon

  // read the .desktop entries, find toplevel ServiceGroups...
  KServiceGroup::Ptr group = KServiceGroup::baseGroup( "settings" );
  if ( !group || !group->isValid() ) {
    return;
  }

  // iterate over group list.
  TModuleGroup *_mg;
  KServiceGroup::List list = group->entries( true, true );
  KServiceGroup::List::ConstIterator it = list.begin();
  KServiceGroup::List::ConstIterator end = list.end();
  for ( ; it != end; ++it )
    {
      KSycocaEntry *p = ( *it );
      // we're just going to deal with toplevel ServiceGroups here
      if ( p->isType( KST_KServiceGroup ) )
        {
          KServiceGroup *_group = static_cast<KServiceGroup*>( p );

          // we just need Tasma's own categories
          if ( !_group->directoryEntryPath().contains( "tasma" ) ) {
            continue;
          }

          if ( _group->icon() )
            _icon = DesktopIcon( _group->icon(),  KIcon::SizeLarge );

          _mg = new TModuleGroup( this,
                                  _group->caption(),
                                  _icon,
                                  _group );
        }
    }
  list.clear();
  // we need a little bit more space for this listview
  setColumnWidth( 0, columnWidth( 0 ) + 10 );

}

TModuleCategoryList::~TModuleCategoryList()
{

}

#include "tmodulecategorylist.moc"
