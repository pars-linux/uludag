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
#include <qsettings.h>

#include "gozluksettings.h"

GozlukSettings::GozlukSettings( QWidget *parent, const char *name )
    : QDialog( parent, name )
{
    setCaption( QString::fromUtf8( "Gözlük Yapılandırması" ) );

    QVBoxLayout *vbox = new QVBoxLayout( this, 10 );

    QHBoxLayout *hbox1 = new QHBoxLayout( vbox, 5 );
    QLabel *pathLabel = new QLabel ( QString::fromUtf8( "Sözlük dosyası :" ), this );
    sozlukPath = new QLineEdit( this );
    hbox1->addWidget( pathLabel );
    hbox1->addWidget( sozlukPath );

    QHBoxLayout *hbox2 = new QHBoxLayout( vbox, 5 );
    applyButton = new QPushButton( "Tamam", this );
    cancelButton = new QPushButton( QString::fromUtf8( "İptal" ), this );
    hbox2->addWidget( applyButton );
    hbox2->addWidget( cancelButton );

    connect( applyButton, SIGNAL( clicked() ),
             this, SLOT( slotApply() ) );
    connect( cancelButton, SIGNAL( clicked() ),
             this, SLOT( slotCancel() ) );

    // get xml file
    QSettings settings;
    settings.setPath(  "Uludag",  "Gozluk" );
    QString dictFile = settings.readEntry(  "sozluk/xml",  "none" );
    if ( dictFile )
        sozlukPath->setText( dictFile );

}

void GozlukSettings::slotApply()
{
    QSettings settings;

    settings.setPath( "Uludag", "Gozluk" );
    settings.writeEntry( "sozluk/xml", sozlukPath->text()  );

    done( 0 );
}

void GozlukSettings::slotCancel()
{
    reject();
}
