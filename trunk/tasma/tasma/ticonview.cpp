/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - ticonview.h
  TIconView implementation.
*/

#include <assert.h>
#include <qstring.h>
#include <qapplication.h>
#include <kicontheme.h>
#include <kiconloader.h>
#include <kservicegroup.h>
#include <kcmodule.h>
#include <kcmoduleinfo.h>
#include <kcmoduleloader.h>
#include <krun.h>
#include <kdebug.h>

#include "ticonview.h"

TIconView::TIconView( QWidget *parent, const char* name )
    : KIconView( parent, name )
{
    setResizeMode( Adjust );
    setItemsMovable( false );

    setItemTextPos( Right );

    setGridX( 200 );
    setGridY( 70 );

    QFont f = font();
    f.setWeight( QFont::Bold );
    setFont( f );

    connect( this, SIGNAL( executed( QIconViewItem* ) ),
             this, SLOT( slotItemSelected( QIconViewItem* ) ) );

}

void TIconView::setCategory( const QString& path )
{
    this->clear();

    QPixmap _icon = DesktopIcon(  "go",  KIcon::SizeMedium ); // defaultIcon

    KServiceGroup::Ptr category = KServiceGroup::group( path );
    if ( !category || !category->isValid() )
        return;

    TIconViewItem *_item;
    KServiceGroup::List list = category->entries(  true,  true );
    KServiceGroup::List::ConstIterator it = list.begin();
    KServiceGroup::List::ConstIterator end = list.end();
    for (  ; it != end; ++it )
    {
        KSycocaEntry *p = (  *it );
        if (  p->isType(  KST_KService ) )
        {
            // KCModuleInfo(KService*)
            KCModuleInfo *minfo = new KCModuleInfo(
                static_cast<KService*>(  p ) );

            if (  minfo->icon() )
                _icon = DesktopIcon(  minfo->icon(),  KIcon::SizeLarge );
            _item = new TIconViewItem( this,
                                       minfo->moduleName(),
                                       _icon, minfo );

        } // ignore second level subGroups!
    }
    list.clear();
}

void TIconView::slotItemSelected( QIconViewItem* item )
{
    TIconViewItem *_item = static_cast<TIconViewItem*>( item );
    
    _module = KCModuleLoader::loadModule( *( _item->moduleinfo() ) );

    /* tricky:
       if we don't disconnect before emitting this signal,
       signal will be emitted for all TIconViewItem(s) loaded.
       But why?*/
    disconnect( SIGNAL( executed( QIconViewItem* ) ) );

    if ( _module ) {
        emit signalModuleSelected( _module, _item->moduleinfo()->icon(), _item->text() );
    }

    connect( this, SIGNAL( executed( QIconViewItem* ) ),
             this, SLOT( slotItemSelected( QIconViewItem* ) ) );
}

void TIconView::contentsMousePressEvent(QMouseEvent* e)
{
  if(e->button() == LeftButton)
    {
      dragPos = e->pos();
      dragItem = static_cast<TIconViewItem*>(findItem(e->pos()));
    }
  KIconView::contentsMousePressEvent(e);
}

void TIconView::contentsMouseMoveEvent(QMouseEvent* e)
{
  if(e->state() && LeftButton)
    {
      int distance = (e->pos() - dragPos).manhattanLength();
      if(distance > QApplication::startDragDistance())
	startDrag();
    }
  // This creates a mouse pointer problem don't do this
  //KIconView::contentsMouseMoveEvent(e);
}

void TIconView::startDrag()
{
  if(dragItem)
    {
      QStrList uri;
      uri.append(dragItem->moduleinfo()->fileName().local8Bit());
      QUriDrag* drag = new QUriDrag(uri, this);
      drag->drag();
    }
}

TIconView::~TIconView()
{
    delete _module;
}


TIconViewItem::TIconViewItem( TIconView *parent, const QString& text,
                              const QPixmap& icon, KCModuleInfo* moduleinfo)
    : KIconViewItem( parent, text, icon )
{
    _moduleinfo = moduleinfo;
}

KCModuleInfo* TIconViewItem::moduleinfo() const
{
    assert(_moduleinfo != NULL);
    return _moduleinfo;
}

TIconViewItem::~TIconViewItem()
{
    delete _moduleinfo;
}

#include "ticonview.moc"
