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
#include <qfiledialog.h>
#include <qsettings.h>

#include "gozluksettings.h"

GozlukSettings::GozlukSettings( QWidget *parent, const char *name )
    : QDialog( parent, name )
{
    setCaption( QString::fromUtf8( "Gözlük Yapılandırması" ) );

    QVBoxLayout *vbox = new QVBoxLayout( this, 6 );
	 
	 QLabel *pathLabel = new QLabel ( QString::fromUtf8( "Öntanımlı sözlük dosyası" ), this );
	 vbox->addWidget( pathLabel );
	 
    QHBoxLayout *hbox1 = new QHBoxLayout( vbox, 5 );
    sozlukPath = new QLineEdit( this );
    dirButton = new QPushButton(QString::fromUtf8("Gözat"), this);
    dirButton->setAutoDefault( FALSE );
    
    hbox1->addWidget( sozlukPath );
    hbox1->addWidget( dirButton );

    QHBoxLayout *hbox2 = new QHBoxLayout( vbox, 5 );
    applyButton = new QPushButton( "Tamam", this );
    applyButton->setAutoDefault( FALSE );
    cancelButton = new QPushButton( QString::fromUtf8( "İptal" ), this );
    cancelButton->setAutoDefault( FALSE );
    hbox2->addWidget( applyButton );
    hbox2->addWidget( cancelButton );

    connect( applyButton, SIGNAL( clicked() ),
             this, SLOT( slotApply() ) );
    connect( cancelButton, SIGNAL( clicked() ),
             this, SLOT( slotCancel() ) );
             
    connect( dirButton, SIGNAL( clicked() ), this, SLOT( slotDir() ) );

    // get xml file
    QSettings settings;
    settings.setPath(  "Uludag",  "Gozluk" );
    QString dictFile = settings.readEntry(  "sozluk/xml",  "none" );
    if ( dictFile )
        sozlukPath->setText( dictFile );

}

void GozlukSettings::slotDir()
{
	QFileDialog *dosyaAc = new QFileDialog(this,"ac",TRUE);
	dosyaAc->setCaption(QString::fromUtf8("Öntanımlı olacak dosyayı seçin"));
	if (dosyaAc->exec() == QDialog::Accepted)
	{
		sozlukPath->setText(dosyaAc->selectedFile());
	}
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
