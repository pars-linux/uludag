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
#include <qstringlist.h>
#include <qvbuttongroup.h>
#include "editdialog.h"
#include "cikar.xpm"
#include "ekle.xpm"


editTerm::editTerm(QWidget *parent, const char *name, TransDef *entry)
					: QDialog(parent,name)
{
	this->setCaption(QString::fromUtf8("Kelime Düzenleme"));
	
	QVBoxLayout *ana = new QVBoxLayout(this,5);
	
	satir = new QLineEdit(this);
	ana->addWidget(satir);
	
	boxSource = new QHGroupBox(QString::fromUtf8("Anlam Listesi"),this);
	QVButtonGroup *sourceButtons = new QVButtonGroup(boxSource);
	sourceButtons->setFrameStyle(QFrame::NoFrame);
	sourceButtons->setInsideMargin(0);
	sourceButtons->setInsideSpacing(1);
	bsEkle = new QPushButton(QPixmap(ekle_xpm),QString::fromUtf8("Ekle"),sourceButtons);
	bsCikar = new QPushButton(QPixmap(cikar_xpm),QString::fromUtf8("Çıkar"),sourceButtons);
	bsEkle->setAutoDefault(false);
	bsCikar->setAutoDefault(false);
	lSource = new QListBox(boxSource);
	
	QStringList a = entry->getSources();
	for (QStringList::Iterator it=a.begin(); it!=a.end(); ++it)
		lSource->insertItem(*it);
	
		
	boxTrans = new QHGroupBox(QString::fromUtf8("Karşılıklar Listesi"), this);
	QVButtonGroup *transButtons = new QVButtonGroup(boxTrans);
	transButtons->setFrameStyle(QFrame::NoFrame);
	transButtons->setInsideMargin(0);
	transButtons->setInsideSpacing(1);
	btEkle = new QPushButton(QPixmap(ekle_xpm),QString::fromUtf8("Ekle"),transButtons);
	btCikar = new QPushButton(QPixmap(cikar_xpm),QString::fromUtf8("Çıkar"),transButtons);
	btEkle->setAutoDefault(false);
	btCikar->setAutoDefault(false);
	lTrans = new QListBox(boxTrans);
	
	a = entry->getTranslations();
	for (QStringList::Iterator it=a.begin(); it!=a.end(); ++it)
		lTrans->insertItem(*it);
	
	boxDef = new QHGroupBox(QString::fromUtf8("Tanımlar Listesi"), this);
	
	QVButtonGroup *defButtons = new QVButtonGroup(boxDef);
	defButtons->setFrameStyle(QFrame::NoFrame);
	defButtons->setInsideMargin(0);
	defButtons->setInsideSpacing(1);
	bdEkle = new QPushButton(QPixmap(ekle_xpm),QString::fromUtf8("Ekle"),defButtons);
	bdCikar = new QPushButton(QPixmap(cikar_xpm),QString::fromUtf8("Çıkar"),defButtons);
	bdEkle->setAutoDefault(false);
	bdCikar->setAutoDefault(false);
	lDef = new QListBox(boxDef);
	
	if (entry->getDefinition() != NULL)
		lDef->insertItem(entry->getDefinition()); 
	
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
	
	this->resize(300,370);
	
	// stringLists
	
	sList = new QStringList();
	tList = new QStringList();
	dList = new QStringList();
	
	// connections
	
	connect( bsEkle, SIGNAL( clicked() ), this, SLOT( sEkle() ) );
	connect( bsCikar,SIGNAL( clicked() ), this, SLOT( sCikar()) );
	connect( btEkle, SIGNAL( clicked() ), this, SLOT( tEkle() ) );
	connect( btCikar,SIGNAL( clicked() ), this, SLOT( tCikar()) );
	connect( bdEkle, SIGNAL( clicked() ), this, SLOT( dEkle() ) );
	connect( bdCikar,SIGNAL( clicked() ), this, SLOT( dCikar()) ); 
	
	connect( iptal,  SIGNAL( clicked() ), this, SLOT( reject() ) );
	connect( kaydet, SIGNAL( clicked() ), this, SLOT( accept() ) );
	connect( kaydet, SIGNAL( clicked() ), this, SLOT( listeKaydet() ) );
}

void editTerm::listeKaydet()
{
	// QListBoxlarin icindekileri listelere ekleyelim :D
	for (uint i=0;i<lSource->count();i++)
		sList->append(lSource->text(i));
	
	for (uint i=0;i<lTrans->count();i++)
		tList->append(lTrans->text(i));
	
	for (uint i=0;i<lDef->count();i++)
		dList->append(lDef->text(i)); 
}


void editTerm::sEkle()
{ 
	if (satir->text() != "")
		lSource->insertItem( satir->text() );
	satir->setText("");
}

void editTerm::tEkle()
{
	if (satir->text() != "")
		lTrans->insertItem( satir->text() );
	satir->setText("");
}

void editTerm::dEkle()
{
	if (satir->text() != "")
		lDef->insertItem( satir->text() );
	satir->setText("");
}

void editTerm::sCikar()
{ lSource->removeItem(lSource->currentItem()); }

void editTerm::tCikar()
{ lTrans->removeItem(lTrans->currentItem()); }

void editTerm::dCikar()
{ lDef->removeItem(lDef->currentItem()); }
