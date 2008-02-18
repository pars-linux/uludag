/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - tasmamainwin.cpp
  TasmaMainWindow implementation.
*/

#include <klocale.h>
#include <qhbox.h>
#include <qwidgetstack.h>
#include <kaction.h>
#include <klistview.h>
#include <kservicegroup.h>
#include <kcmodule.h>
#include <kaboutapplication.h>

#include "aboutview.h"
#include "tcategoryview.h"
#include "tmodulegroup.h"
#include "tmodulecategorylist.h"
#include "tmoduleview.h"
#include "tasmamainwin.h"
#include "tasmamainwin.moc"

TasmaMainWin::TasmaMainWin( const char* name )
    : KMainWindow( 0, name, WStyle_ContextHelp ),
      _moduleview( 0 ),
      _currentModule( 0 ),
      _currentCategory( 0 )
{
    setupActions();

    _hbox = new QHBox( this );
    _hbox->setSpacing( 4 );

    // module groups
    _index = new TModuleCategoryList( _hbox );
    connect( _index, SIGNAL( selectionChanged( QListViewItem* ) ),
             this, SLOT( categorySelected( QListViewItem* ) ) );
    connect( _index, SIGNAL( clicked( QListViewItem* ) ),
             this, SLOT( categorySelected( QListViewItem* ) ) );

    // central widget
    _wstack = new QWidgetStack( _hbox );
    _wstack->setFrameStyle( QFrame::StyledPanel | QFrame::Sunken );
    _wstack->setLineWidth( 2 );

    // modules in a group (iconview)
    _categoryview = new TCategoryView( this );
    _wstack->addWidget( _categoryview );

    // about widget
    _about = new AboutView( this );
    _wstack->addWidget( _about );
    _wstack->raiseWidget( _about );

    connect( _categoryview, SIGNAL( signalModuleSelected( KCModule*, const QString&, const QString&, const QString&, bool ) ),
             this, SLOT( moduleSelected( KCModule*, const QString&, const QString&, const QString&, bool ) ) );

    setCentralWidget( _hbox );
}

TasmaMainWin::~TasmaMainWin()
{
}

void TasmaMainWin::setupActions()
{
    KStdAction::quit( this,  SLOT( close() ),  actionCollection() );

    _about_module = new KAction( i18n( "About Current Module" ), 0,
                                this, SLOT( aboutModule() ), actionCollection(),
                                "help_about_module" );

    _about_module->setEnabled( false );

    createGUI( "tasmaui.rc" );
}

void TasmaMainWin::categorySelected( QListViewItem* category )
{
    if( _moduleview )
    {
        delete _moduleview;
        _moduleview = 0;
    }

    if ( !category ) {
        // clicked on an empty area in listview.
        return;
    }

    TModuleGroup *_mg = static_cast<TModuleGroup*>( category );

    // If visible widget is a moduleview (or aboutview), than we should remove it.
    if ( _wstack->visibleWidget() != _categoryview ) {
        QWidget *w = _wstack->visibleWidget();
        _wstack->removeWidget( w );
    }

    _wstack->raiseWidget( _categoryview );
    _categoryview->setCategory( _mg->path(), _mg->icon(), _mg->caption() );

    // set the current category
    _currentCategory = category;

    // no module is selected
    _about_module->setEnabled( false );
}

void TasmaMainWin::moduleSelected( KCModule *module, const QString& icon_path, const QString& text, const QString& filename, bool needsRootPrivileges)
{
    if ( _moduleview ) {
        delete _moduleview;
        _moduleview = 0;
    }

    _currentModule = module;
    if ( _currentModule->aboutData() ) {
        _about_module->setEnabled( true );
    }
    else {
        _about_module->setEnabled( false );
    }

    _moduleview = new TModuleView( this, module, icon_path, text, filename, needsRootPrivileges);
    _wstack->addWidget( _moduleview );
    _wstack->raiseWidget( _moduleview );
}

void TasmaMainWin::backToCategory()
{
    /* to activate a category first unselect than select it again.
       funny, but works :) */
    _index->setSelected( _currentCategory, false );
    _index->setSelected( _currentCategory, true );
}

void TasmaMainWin::aboutModule()
{
    KAboutApplication about( _currentModule->aboutData() );
    about.exec();
}
