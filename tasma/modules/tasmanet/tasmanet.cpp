/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/


#include <kaboutdata.h>
#include <kdialog.h>
#include <qlayout.h>

#include "tasmanetwidget.h"
#include "tasmanet.h"
#include "tasmanet.moc"

extern "C"
{
    KCModule *create_tasmanet( QWidget *parent, const char* name )
    {
        return new TasmaNet( parent, name );
    }
};

TasmaNet::TasmaNet( QWidget* parent, const char *name )
    : KCModule( parent, name )
{
    TasmaNetAbout = new KAboutData (  "tasmanet",  I18N_NOOP(  "TASMA Network Configuration Module" ),  "0.1",
                                      I18N_NOOP(  "TASMA Network Configuration Module" ),  KAboutData::License_GPL,
                                      I18N_NOOP(  "(c) 2005, TUBITAK - UEKAE" ) );
    TasmaNetAbout->addAuthor( "Barış Metin",  I18N_NOOP( "Current Maintainer" ),  "baris@uludag.org.tr" );
    TasmaNetAbout->addAuthor( "Necati Demir", I18N_NOOP( "Contributor" ), "ndemir@demir.web.tr" );
    TasmaNetAbout->setTranslator( "Barış Metin", "baris@uludag.org.tr" );

    setSizePolicy( QSizePolicy( QSizePolicy::Expanding, QSizePolicy::Expanding ) );

    QVBoxLayout *v = new QVBoxLayout( this, 0, KDialog::spacingHint() );

    mainWidget = new TasmaNetWidget( this );
    v->addWidget( mainWidget );
    setButtons( KCModule::Help );
    load();
}

void TasmaNet::load()
{
}

void TasmaNet::save()
{
}

void TasmaNet::defaults()
{
}

QString TasmaNet::quickHelp() const
{
    return i18n( "A network configuration module for TASMA." );
}

void TasmaNet::configChanged()
{
    emit changed( true );
}
