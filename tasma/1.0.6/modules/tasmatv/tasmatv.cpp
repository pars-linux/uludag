/*
  Copyright (c) 2005-2006, TUBITAK/UEKAE

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
#include <qradiobutton.h>
#include <qbuttongroup.h>
#include <qcheckbox.h>
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
				     I18N_NOOP("(c) 2005-2006, TUBITAK - UEKAE" ) );

    TasmaTvAbout->addAuthor( "Faik Uygur",  I18N_NOOP( "Current Maintainer" ),  "faik@pardus.org.tr" );

    connect(mainWidget->tvModel, SIGNAL(selectionChanged()), SLOT(configChanged()));
    connect(mainWidget->tvVendor, SIGNAL(selectionChanged()), SLOT(tvVendorChanged()));
    connect(mainWidget->tunerModel, SIGNAL(selectionChanged()), SLOT(configChanged()));
    connect(mainWidget->tunerVendor, SIGNAL(selectionChanged()), SLOT(tunerVendorChanged()));
    connect(mainWidget->pllGroup, SIGNAL(pressed(int)), SLOT(configChanged()));
    connect(mainWidget->radioCard, SIGNAL(stateChanged(int)), SLOT(configChanged()));
    load();
}

void TasmaTv::load()
{
    int card, pll, radio, tuner = 0;

    QFile bttv("/etc/modules.d/bttv");
    QRegExp re(".*card=([0-9]+)( tuner=([0-9]+))?( pll=([0-9]))?( radio=([0-9]))?");

    if (bttv.open(IO_ReadOnly)) {

	QByteArray ba = bttv.readAll();
	QCString str(ba.data(), ba.size() + 1);

	if (re.search(str) != -1) {
	    card  = re.cap(1).toInt();
	    if (!re.cap(3).isEmpty())
		tuner = re.cap(3).toInt();
	    pll   = re.cap(5).toInt();
	    radio = re.cap(7).toInt();

	    mainWidget->selectCard(card);
	    mainWidget->selectTuner(tuner);
	    mainWidget->pllGroup->setButton(pll);
	    mainWidget->radioCard->setChecked(radio);
	}
	
	bttv.close();
    }
}

void TasmaTv::save()
{
    mainWidget->removeModule();
    mainWidget->saveOptions();
    mainWidget->loadModule();
}

void TasmaTv::defaults()
{
    mainWidget->selectCard(AUTO_CARD);
    mainWidget->selectTuner(AUTO_TUNER);
}

QString TasmaTv::quickHelp() const
{
    return i18n("Tv card configuration module for TASMA.");
}

void TasmaTv::configChanged()
{
    emit changed(true);
}

void TasmaTv::tunerVendorChanged()
{
    mainWidget->tunerVendorChanged();
}

void TasmaTv::tvVendorChanged()
{
    mainWidget->tvVendorChanged();
}
