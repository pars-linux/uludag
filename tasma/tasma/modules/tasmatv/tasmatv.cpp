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
#include <ksimpleconfig.h>

#include <qlistbox.h>
#include <qradiobutton.h>
#include <qbuttongroup.h>
#include <qcheckbox.h>
#include <qfile.h>
#include <qlayout.h>

#include "tasmatv.h"
#include "tasmatv.moc"

typedef KGenericFactory<TasmaTv, QWidget > TasmaTvFactory;
K_EXPORT_COMPONENT_FACTORY(kcm_tasmatv, TasmaTvFactory("tasmatv"))

TasmaTv::TasmaTv( QWidget* parent, const char *name, const QStringList &)
: KCModule(TasmaTvFactory::instance(), parent, name)
{
    KGlobal::locale()->insertCatalogue("tasma");
    mainWidget = new TvConfig(this);

    QVBoxLayout *v = new QVBoxLayout(this, 0, KDialog::spacingHint());
    v->addWidget(mainWidget);

    TasmaTvAbout = new KAboutData (  "tasmatv",  I18N_NOOP(  "TASMA Tv Card Configuration Module" ),  "0.1",
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
    KConfig *config = new KConfig("kcmtasmatvrc", true);
    config->setGroup("System");
    mainWidget->selectCard(config->readNumEntry("Card"));
    mainWidget->selectTuner(config->readNumEntry("Tuner"));
    mainWidget->pllGroup->setButton(config->readNumEntry("Pll"));
    mainWidget->radioCard->setChecked(config->readBoolEntry("Radio"));
    delete config;
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
