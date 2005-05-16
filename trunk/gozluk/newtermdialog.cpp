/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
	Bu pencere nedir?
	yeni bir term eklemek için gerekli pencere...
	
	Mayıs 2005 - Kaya Oğuz - kaya@kuzeykutbu.org

*/

#include <qlayout.h>
#include <qdialog.h>
#include <qpushbutton.h>
#include <qpopupmenu.h>
#include <qcursor.h>
#include "newtermdialog.h"


newTerm::newTerm(QWidget *parent, const char *name):
					QDialog(parent,name)
{
	this->setCaption(QString::fromUtf8("Yeni Kelime Ekleme"));
	
	QVBoxLayout *ana = new QVBoxLayout(this,5);
	
	boxSource = new QVGroupBox(QString::fromUtf8("Anlam Listesi"),this);
	ySource = new QLineEdit(boxSource);
	lSource = new QListBox(boxSource);
	
	boxTrans = new QVGroupBox(QString::fromUtf8("Karşılıklar Listesi"), this);
	yTrans = new QLineEdit(boxTrans);
	lTrans = new QListBox(boxTrans);
	
	boxDef = new QVGroupBox(QString::fromUtf8("Tanımlar Listesi"), this);
	yDef = new QLineEdit(boxDef);
	lDef = new QListBox(boxDef);
	
	ana->addWidget(boxSource);
	ana->addWidget(boxTrans);
	ana->addWidget(boxDef);
	
	QHBoxLayout *buttons = new QHBoxLayout(ana);
	
	kaydet = new QPushButton(QString::fromUtf8("Kaydet"),this);
	buttons->addWidget(kaydet);
	buttons->addStretch(1);
	kaydet->setDefault(false);
	kaydet->setAutoDefault(false); 
	
	iptal = new QPushButton(QString::fromUtf8("İptal"),this);
	iptal->setDefault(false);
	iptal->setAutoDefault(false); // bu iki defaultlar kabus :)
	buttons->addWidget(iptal);
	
	this->resize(250,390);
	
	// stringLists
	
	sList = new QStringList();
	tList = new QStringList();
	dList = new QStringList();
	
	// popups
	
	sSil = new QPopupMenu(this); sSil->insertItem("Sil",this,SLOT( sCikar() ));
	tSil = new QPopupMenu(this); tSil->insertItem("Sil",this,SLOT( tCikar() ));
	dSil = new QPopupMenu(this); dSil->insertItem("Sil",this,SLOT( dCikar() ));
	
	
	// connections
	connect( ySource, SIGNAL( returnPressed() ), this, SLOT( sEkle() ) );
	connect( yTrans , SIGNAL( returnPressed() ), this, SLOT( tEkle() ) );
	connect( yDef   , SIGNAL( returnPressed() ), this, SLOT( dEkle() ) ); 
	
	connect( iptal,  SIGNAL( clicked() ), this, SLOT( reject() ) );
	connect( kaydet, SIGNAL( clicked() ), this, SLOT( accept() ) );
	connect( kaydet, SIGNAL( clicked() ), this, SLOT( listeKaydet() ) );

	connect( lSource, SIGNAL( rightButtonClicked(QListBoxItem*, const QPoint & )), this, SLOT( sPopup() ));
	connect( lTrans,  SIGNAL( rightButtonClicked(QListBoxItem*, const QPoint & )), this, SLOT( tPopup() ));
	connect( lDef,    SIGNAL( rightButtonClicked(QListBoxItem*, const QPoint & )), this, SLOT( dPopup() ));

}

void newTerm::listeKaydet()
{
	// QListBoxlarin icindekileri listelere ekleyelim :D
	for (uint i=0;i<lSource->count();i++)
		sList->append(lSource->text(i));
	
	for (uint i=0;i<lTrans->count();i++)
		tList->append(lTrans->text(i));
	
	for (uint i=0;i<lDef->count();i++)
		dList->append(lDef->text(i));
}

void newTerm::sPopup()
{ sSil->exec(QCursor::pos() ); }

void newTerm::tPopup()
{ tSil->exec(QCursor::pos() ); }

void newTerm::dPopup()
{ dSil->exec(QCursor::pos() ); }

void newTerm::sEkle()
{ 
	if (ySource->text() != "")
		lSource->insertItem( ySource->text() );
	ySource->setText("");
}

void newTerm::tEkle()
{
	if (yTrans->text() != "")
		lTrans->insertItem( yTrans->text() );
	yTrans->setText("");
}

void newTerm::dEkle()
{
	if (yDef->text() != "")
		lDef->insertItem( yDef->text() );
	yDef->setText("");
}

void newTerm::sCikar()
{ lSource->removeItem(lSource->currentItem()); }

void newTerm::tCikar()
{ lTrans->removeItem(lTrans->currentItem()); }

void newTerm::dCikar()
{ lDef->removeItem(lDef->currentItem()); }
