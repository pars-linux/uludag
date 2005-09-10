/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qlabel.h>
#include <qlayout.h>
#include <kiconloader.h>

#include "ticonview.h"
#include "tcategoryview.h"
#include "tcategoryview.moc"

TCategoryView::TCategoryView( QWidget *parent, const char* name )
    : QFrame( parent, name )
{
    QVBoxLayout *vbox = new QVBoxLayout( this, 10 );

    _title = new CategoryTitle( this );

    _iconview = new TIconView( this );
    connect ( _iconview, SIGNAL( signalModuleSelected(  KCModule*,  const QString&,  const QString& ) ),
              this, SIGNAL( signalModuleSelected(  KCModule*,  const QString&,  const QString& ) ) );

    vbox->addWidget( _title );
    vbox->addWidget( _iconview );
}

TCategoryView::~TCategoryView()
{
    delete _iconview;
    delete _title;
}

void TCategoryView::setCategory( const QString& path, const QString& icon, const QString& title )
{
    QPixmap _icon = DesktopIcon( icon, KIcon::SizeLarge );
    _title->setPixmap( _icon );

    _title->setText( title );

    _iconview->setCategory( path );
}

CategoryTitle::CategoryTitle( TCategoryView *view )
    : QFrame( view )
{
    QHBoxLayout *hbox = new QHBoxLayout( this, 5 );
    _pix = new QLabel( this );

    _caption = new QLabel( this );

    hbox->addWidget( _pix );
    hbox->addWidget( _caption, 0, AlignLeft );
};

void CategoryTitle::setText( const QString& text )
{
    _caption->setText( text );
    QFont f = _caption->font();
    f.setPointSize( 20 );
    f.setWeight( QFont::Bold );
    _caption->setFont( f );
}

void CategoryTitle::setPixmap( const QPixmap& icon )
{
    _pix->setPixmap( icon );
    _pix->setFixedSize( _pix->minimumSizeHint() );

}
