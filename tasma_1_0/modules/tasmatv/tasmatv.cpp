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
#include <kgenericfactory.h>
#include <qlistbox.h>
#include <qfile.h>
#include <qregexp.h>
#include <qlayout.h>

#include "tasmatv.h"
#include "tasmatv.moc"

typedef KGenericFactory<TasmaTv, QWidget > TasmaTvFactory;
K_EXPORT_COMPONENT_FACTORY(kcm_tasmatv, TasmaTvFactory("kcmtasmatv"))

  TasmaTv::TasmaTv( QWidget* parent, const char *name, const QStringList &)
  : KCModule(TasmaTvFactory::instance(), parent, name)
{
    mainWidget = new TvConfig(this);
    
    QVBoxLayout *v = new QVBoxLayout(this, 0, KDialog::spacingHint());
    v->addWidget(mainWidget);

    TasmaTvAbout = new KAboutData (  I18N_NOOP("tasmatv"),  I18N_NOOP(  "TASMA Tv Card Configuration Module" ),  "0.1",
				     I18N_NOOP("TASMA Tv Card Configuration Module" ),  
				     KAboutData::License_GPL,
				     I18N_NOOP("(c) 2005, TUBITAK - UEKAE" ) );

    TasmaTvAbout->addAuthor( "Faik Uygur",  I18N_NOOP( "Current Maintainer" ),  "faikuygur@kuheylan.org" );

    connect(mainWidget->cardList, SIGNAL(selectionChanged()), SLOT(configChanged()));
    connect(mainWidget->tunerList, SIGNAL(selectionChanged()), SLOT(configChanged()));
    load();
}

void TasmaTv::load()
{
    int card, tuner;

    QFile bttv("/etc/modules.d/bttv");
    QRegExp re(".*card=([0-9]+)( tuner=([0-9]+))?");

    if (bttv.open(IO_ReadOnly))
    {
	QByteArray ba = bttv.readAll();
	QCString str(ba.data(), ba.size() + 1);

	if (re.search(str) != -1)
	{
	    card = re.cap(1).toInt();
	    tuner = re.cap(3).toInt() + 1;
	    mainWidget->cardList->setCurrentItem(card);
	    mainWidget->tunerList->setCurrentItem(tuner);
	}
	
	bttv.close();
    }
}

void TasmaTv::save()
{
    mainWidget->removeModule();
    mainWidget->loadModule();
    mainWidget->saveOptions();
}

void TasmaTv::defaults()
{
    mainWidget->cardList->setCurrentItem(AUTO_CARD);
    mainWidget->tunerList->setCurrentItem(AUTO_TUNER);
}

QString TasmaTv::quickHelp() const
{
    return i18n("Tv card configuration module for TASMA.");
}

void TasmaTv::configChanged()
{
    emit changed(true);
}
