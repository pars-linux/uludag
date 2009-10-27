/*
  Copyright (c) TUBITAK/UEKAE

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
#include <qregexp.h>

#include <kicontheme.h>
#include <kiconloader.h>
#include <kservicegroup.h>
#include <kcmodule.h>
#include <kcmoduleinfo.h>
#include <kcmoduleloader.h>
#include <krun.h>
#include <ksimpleconfig.h>
#include <kstandarddirs.h>
#include <kdebug.h>
#include <kprocess.h>
#include "ticonview.h"

TIconView::TIconView( QWidget *parent, const char* name )
  : KIconView( parent, name ), _module(0L)
{
  setResizeMode( Adjust );
  setItemsMovable( false );

  setItemTextPos( Right );

  setGridX( 200 );
  setGridY( 70 );

  QFont f = font();
  f.setWeight( QFont::Bold );
  setFont( f );

  setShowToolTips( false );

  KConfig *config = KGlobal::config();
  config->setGroup("Extra");
  showExtras = config->readNumEntry( "Selected" );

  toolTip = 0;

  connect( this, SIGNAL( executed( QIconViewItem* ) ), SLOT( slotItemSelected( QIconViewItem* ) ) );

  /* comment those signals due to bug#7761
  connect( this, SIGNAL( executed( QIconViewItem* ) ), SLOT( removeToolTip()) );
  connect( this, SIGNAL( onItem( QIconViewItem* ) ), SLOT( showToolTip( QIconViewItem* ) ) );
  connect( this, SIGNAL( onViewport() ),  SLOT( removeToolTip() ) );
  */

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

          if (showExtras == false)
            {
              KSimpleConfig cfg(minfo->fileName());

              cfg.setDesktopGroup();
              if ( cfg.readEntry("Categories").contains("X-KDE-tasma-extra") )
                continue;
            }

          if (  minfo->icon() )
                _icon = DesktopIcon(  minfo->icon(),  KIcon::SizeLarge );
                _item = new TIconViewItem( this,
                                     minfo->moduleName(),
                                     _icon, minfo , minfo->comment());
        } // ignore second level subGroups!
    }
  list.clear();
}

void TIconView::slotItemSelected( QIconViewItem* item )
{
  // kdWarning() << "LU LU LU I got some apple" << endl;
  TIconViewItem *_item = static_cast<TIconViewItem*>( item );
  KSimpleConfig cfg(_item->moduleinfo()->fileName(),true);
  cfg.setDesktopGroup();

  if(cfg.readBoolEntry("X-Tasma-Fork"))
    {
      KProcess proc;
      QStringList args = QStringList::split(QRegExp("\\s{1}"),cfg.readEntry("Exec"));

      QStringList::ConstIterator it = args.constBegin();

      while( it != args.constEnd() )
        {
          if (!(*it).startsWith("%"))
            proc << *it;
          ++it;
        }

      proc.start(KProcess::DontCare);
      return;
    }

  _module = KCModuleLoader::loadModule( *( _item->moduleinfo() ), KCModuleLoader::Dialog );

  if ( _module ) {
    emit signalModuleSelected( _module, _item->moduleinfo()->icon(), _item->text(),
                               _item->moduleinfo()->fileName(), _item->moduleinfo()->needsRootPrivileges());
  }
}

void TIconView::contentsMouseDoubleClickEvent (QMouseEvent *event)
{
  _module = 0L;

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
/*
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
} //this event causes crashing. commented but no feature lack yet.
*/ 
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
   removeToolTip();
}

void TIconView::keyPressEvent(QKeyEvent* event)
{
  if( (event->key() ==  Qt::Key_Return) || (event->key() == Qt::Key_Enter) )
    slotItemSelected(currentItem());

  QIconView::keyPressEvent(event);
}

TIconViewItem::TIconViewItem( TIconView *parent, const QString& text,
                              const QPixmap& icon, KCModuleInfo* moduleinfo, QString itemComment)
  : KIconViewItem( parent, text, icon )
{
  _moduleinfo = moduleinfo;
   comment = itemComment;

}

void TIconView::focusInEvent ( QFocusEvent* event ) {

  if(event->reason() == QFocusEvent::Tab)
    setSelected(firstItem(), true);

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

void TIconView::showToolTip( QIconViewItem *item ){

  TIconViewItem *_item = static_cast<TIconViewItem*>( item );

    delete toolTip;
    toolTip = 0;

    if ( !item )
    return;

    if(! _item->comment)
        return;

    toolTip = new QLabel( QString::fromUtf8(" %1 ").arg(_item->comment), 0,
                  "tasma",
                  WStyle_StaysOnTop | WStyle_Customize | WStyle_NoBorder | WStyle_Tool | WX11BypassWM );
    toolTip->setFrameStyle( QFrame::Plain | QFrame::Box );
    toolTip->setLineWidth( 1 );
    toolTip->setAlignment( AlignLeft | AlignTop );
    toolTip->move( QCursor::pos() + QPoint( 4, 4 ) );
    toolTip->adjustSize();
    QRect screen = QApplication::desktop()->screenGeometry(
        QApplication::desktop()->screenNumber(QCursor::pos()));
    if (toolTip->x()+toolTip->width() > screen.right()) {
        toolTip->move(toolTip->x()+screen.right()-toolTip->x()-toolTip->width(), toolTip->y());
    }
    if (toolTip->y()+toolTip->height() > screen.bottom()) {
        toolTip->move(toolTip->x(), screen.bottom()-toolTip->y()-toolTip->height()+toolTip->y());
    }
    toolTip->setFont( QToolTip::font() );
    toolTip->setPalette( QToolTip::palette(), true );
    toolTip->show();


}
void TIconView::removeToolTip(){
    delete toolTip;
    toolTip = 0;
}

#include "ticonview.moc"
