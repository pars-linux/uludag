/*
  Copyright (c) 2004,2005 TUBITAK/UEKAE
  Copyright (c) 1999 Matthias Hoelzer-Kluepfel <hoelzer@kde.org>
    
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

#include <X11/Xlib.h>
#include <fixx11h.h>

#include <qlayout.h>
#include <qlabel.h>
#include <qsizepolicy.h>
#include <qscrollview.h>
#include <qvbox.h>
#include <qxembed.h>

#include <kprocess.h>
#include <kpushbutton.h>
#include <kstdguiitem.h>
#include <kicontheme.h>
#include <kiconloader.h>
#include <kseparator.h>
#include <kstandarddirs.h>
#include <klocale.h>
#include <kcmodule.h>

#include "tmoduleview.h"

TModuleView::TModuleView( QWidget *parent, KCModule* module, const QString& icon_path, const QString& text, const QString& filename, 
                          bool needsRootPrivileges )
  : QWidget( parent ), _proc(0L), _embedWidget(0L), _embedLayout(0L)
{
    contentView = new TMContent( this, module );

    // Name of the desktop file
    _filename = filename.section('/',-1);
    
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

    _runAsRoot = new KPushButton( KGuiItem( i18n( "&Administrator Mode" ), "" ), this );
    _runAsRoot->setFixedSize( _runAsRoot->sizeHint() );

    if( !needsRootPrivileges )
        _runAsRoot->hide();
    
    QHBoxLayout *buttons = new QHBoxLayout( vbox, 5);
    buttons->addWidget( _back, 0, AlignLeft );
    buttons->addWidget( _default, 0, AlignLeft );
    buttons->addWidget( _runAsRoot, 0, AlignLeft );

    buttons->addStretch( 1 );

    buttons->addWidget( _apply, 0, AlignRight );
    buttons->addWidget( _reset, 0, AlignRight );

    // set buttons visibility
    #if 0
    int b = contentView->module()->buttons();
    if ( !( b & KCModule::Default ) ) _default->hide();
    if ( !( b & KCModule::Apply ) ) {
        _apply->hide();
        _reset->hide();
    }
    #endif

    connect( _back, SIGNAL( clicked() ), parent, SLOT( backToCategory() ) );

    connect( _default, SIGNAL( clicked() ), SLOT( defaultClicked() ) );
    connect( _apply, SIGNAL( clicked() ), SLOT( applyClicked() ) );
    connect( _reset, SIGNAL( clicked() ), SLOT( resetClicked() ) );
    connect( _runAsRoot, SIGNAL( clicked() ), SLOT( runAsRoot() ) );

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

void TModuleView::runAsRoot()
{
  delete _proc;
  delete _embedWidget;
  delete _embedLayout;

  _embedLayout = new QVBoxLayout(parentWidget());
  _embedFrame = new QVBox(parentWidget());
  _embedFrame->setFrameStyle( QFrame::Box | QFrame::Raised );
  QPalette pal( red );
  pal.setColor( QColorGroup::Background, parentWidget()->colorGroup().background() );
  _embedFrame->setPalette( pal );
  _embedFrame->setLineWidth( 2 );
  _embedFrame->setMidLineWidth( 2 );
  _embedLayout->addWidget(_embedFrame,1);
  _embedWidget = new QXEmbed(_embedFrame);
  hide();
  _embedFrame->show();
  QLabel *_busy = new QLabel(i18n("<big>Loading...</big>"), _embedWidget);
  _busy->setAlignment(AlignCenter);
  _busy->setTextFormat(RichText);
  _busy->setGeometry(0,0, width(), height());
  _busy->show();

  // run the process
  QString kdesu = KStandardDirs::findExe("kdesu");
  
  _proc = new KProcess;
  *_proc << kdesu;
  *_proc << "--nonewdcop";
  // We have to disable the keep-password feature because
  // in that case the modules is started through kdesud and kdesu
  // returns before the module is running and that doesn't work.
  // We also don't have a way to close the module in that case.
  *_proc << "-n"; // Don't keep password.
  *_proc << QString("kcmshell %1 --embed-proxy %2 --lang %3").arg(_filename).arg(_embedWidget->winId()).arg(KGlobal::locale()->language());
 
  connect(_proc, SIGNAL(processExited(KProcess*)), this, SLOT(killRootProcess()));
  
  if ( !_proc->start(KProcess::NotifyOnExit) )
    {
      delete _proc;
      _proc = 0L;
    }
}

void TModuleView::killRootProcess()
{
  if (_embedWidget &&  _embedWidget->embeddedWinId())
    XKillClient(qt_xdisplay(), _embedWidget->embeddedWinId());

  delete _embedWidget;
  _embedWidget = 0;

  delete _proc;
  _proc = 0;

  delete _embedLayout;
  _embedLayout = 0;
  
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
    killRootProcess();
    
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
  delete contentWidget;
}

KCModule* TMContent::module() const
{
    return _module;
}

#include "tmoduleview.moc"
