/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - tmoduleview.cpp
  TModuleView implementation.
*/

#include <kpushbutton.h>
#include <kstdguiitem.h>
#include <kicontheme.h>
#include <kiconloader.h>
#include <kseparator.h>
#include <klocale.h>
#include <qlayout.h>
#include <qlabel.h>
#include <qsizepolicy.h>
#include <qscrollview.h>
#include <kcmodule.h>

#include "tmoduleview.h"
#include "tmoduleview.moc"

TModuleView::TModuleView( QWidget *parent, KCModule* module, const QString& icon_path, const QString& text )
    : QWidget( parent )
{
    contentView = new TMContent( this, module );

    QVBoxLayout *vbox = new QVBoxLayout( this, 3 );
    QHBoxLayout *header = new QHBoxLayout( vbox, 5 );

    QPixmap pix = DesktopIcon( icon_path, KIcon::SizeSmallMedium );
    _icon = new QLabel( this );
    _icon->setPixmap( pix );
    _icon->setFixedSize( _icon->minimumSizeHint() );

    _moduleName = new QLabel( this );
    QString name = QString( "<b>" ) + text + QString( "</b>" );
    _moduleName->setText( name );
    header->addWidget( _icon );
    header->addWidget( _moduleName );

    _sep = new KSeparator( KSeparator::HLine, this );

    // main content
    vbox->addWidget( contentView );
    vbox->addWidget( _sep );

    _back = new KPushButton( KGuiItem( i18n( "&Back" ), "back" ), this );
    _back->setFixedSize( _back->sizeHint() );

    _default = new KPushButton( KStdGuiItem::defaults(), this );
    _default->setFixedSize( _default->sizeHint() );

    _apply = new KPushButton( KStdGuiItem::apply(), this );
    _apply->setFixedSize( _apply->sizeHint() );

    _reset = new KPushButton( KGuiItem( i18n( "&Reset" ), "undo" ), this );
    _reset->setFixedSize( _reset->sizeHint() );

    QHBoxLayout *buttons = new QHBoxLayout( vbox, 5);
    buttons->addWidget( _back, 0, AlignLeft );
    buttons->addWidget( _default, 0, AlignLeft );

    buttons->addStretch( 1 );

    buttons->addWidget( _apply, 0, AlignRight );
    buttons->addWidget( _reset, 0, AlignRight );

    // set buttons visibility
    int b = contentView->module()->buttons();
    if ( !( b & KCModule::Default ) ) _default->hide();
    if ( !( b & KCModule::Apply ) ) {
        _apply->hide();
        _reset->hide();
    }

    connect( _back, SIGNAL( clicked() ), parent, SLOT( backToCategory() ) );

    connect( _default, SIGNAL( clicked() ), SLOT( defaultClicked() ) );
    connect( _apply, SIGNAL( clicked() ), SLOT( applyClicked() ) );
    connect( _reset, SIGNAL( clicked() ), SLOT( resetClicked() ) );

    connect( contentView->module(), SIGNAL( changed( bool ) ),
             SLOT( contentChanged( bool ) ) );

    _apply->setEnabled( false );
    _reset->setEnabled( false );
}

void TModuleView::applyClicked()
{
    contentView->module()->save();
    contentChanged( false );
}

void TModuleView::resetClicked()
{
    contentView->module()->load();
    contentChanged( false );
}

void TModuleView::defaultClicked()
{
    contentView->module()->defaults();
    contentChanged( true );
}

void TModuleView::contentChanged( bool state )
{
    _apply->setEnabled( state );
    _reset->setEnabled( state );
}

TModuleView::~TModuleView()
{
    delete _apply;
    delete _reset;

    delete _icon;
    delete _moduleName;

    delete contentView;
}

TMContent::TMContent( QWidget *parent, KCModule *module )
    : QScrollView( parent )
{
    _module = module;

    setFrameStyle( NoFrame );
    setResizePolicy( AutoOneFit );
    // hacky;
    contentWidget = new ContentWidget( viewport() );
    _module->reparent( contentWidget,
                       0,
                       QPoint( 0, 0)
                       ,true);

    vbox = new QVBoxLayout( contentWidget );
    vbox->addWidget( _module );
    vbox->activate();

    addChild( contentWidget );
}

TMContent::~TMContent()
{
    delete _module;

    delete contentWidget;
}

KCModule* TMContent::module() const
{
    return _module;
}

