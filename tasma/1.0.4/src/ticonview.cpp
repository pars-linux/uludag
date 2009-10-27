/*
  Copyright (c) 2004,2005 TUBITAK/UEKAE

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
  : KIconView( parent, name ), _module(0L), _oldModuleInfo(0L)
{
    setResizeMode( Adjust );
    setItemsMovable( false );

    setItemTextPos( Right );

    setGridX( 200 );
    setGridY( 70 );

    QFont f = font();
    f.setWeight( QFont::Bold );
    setFont( f );

    connect( this, SIGNAL( executed( QIconViewItem* ) ), SLOT( slotItemSelected( QIconViewItem* ) ) );

}

void TIconView::setCategory( const QString& path )
{
    clear();

    QPixmap _icon = DesktopIcon( "go", KIcon::SizeMedium ); // defaultIcon

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
  
    if(_oldModuleInfo) KCModuleLoader::unloadModule(*_oldModuleInfo);
    _module = KCModuleLoader::loadModule( *( _item->moduleinfo() ), KCModuleLoader::Dialog );
    _oldModuleInfo = _item->moduleinfo();

    if ( _module ) {
        emit signalModuleSelected( _module, _item->moduleinfo()->icon(), _item->text(),
                                 _item->moduleinfo()->fileName(), _item->moduleinfo()->needsRootPrivileges());
    }
}

void TIconView::contentsMouseDoubleClickEvent (QMouseEvent *event)
{
  _module = 0L;
  _oldModuleInfo = 0L;
  
  KIconView::contentsMouseDoubleClickEvent(event);
}

void TIconView::contentsMousePressEvent(QMouseEvent* event)
{
  if(event->button() == LeftButton)
    {
      dragPos = event->pos();
      dragItem = static_cast<TIconViewItem*>(findItem(event->pos()));
    }
  KIconView::contentsMousePressEvent(event);
}

void TIconView::contentsMouseMoveEvent(QMouseEvent* event)
{
  if(event->state() && LeftButton)
    {
      int distance = (event->pos() - dragPos).manhattanLength();
      if(distance > QApplication::startDragDistance())
	startDrag();
    }
  // This creates a mouse pointer problem don't do this
  //KIconView::contentsMouseMoveEvent(event);
}

void TIconView::startDrag()
{
  if(dragItem)
    {
      QStrList uri;
      uri.append(dragItem->moduleinfo()->fileName().local8Bit());
      QUriDrag* uriDrag = new QUriDrag(uri, this);
      uriDrag->drag();
    }
}

TIconView::~TIconView()
{   
}

void TIconView::keyPressEvent(QKeyEvent* event)
{
    if( event->key() & Qt::Key_Return || event->key() & Qt::Key_Enter )
        slotItemSelected(currentItem());

    QIconView::keyPressEvent(event);
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
