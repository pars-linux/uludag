/*
  Copyright (c) 2005-2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <KAboutData>
#include <KDialog>
#include <KGenericFactory>
// #include <KSimpleConfig>

#include <Q3ListBox>
#include <QRadioButton>
#include <QButtonGroup>
#include <QCheckBox>
#include <QFile>
#include <QLayout>

#include "tv-manager.h"
#include "tv-manager.moc"

typedef KGenericFactory<TasmaTv, QWidget> TasmaTvFactory;
//typedef KGenericFactory<TasmaTv, QWidget> TasmaTvFactory;
K_EXPORT_COMPONENT_FACTORY(kcm_tasmatv, TasmaTvFactory("tasmatv"))
//K_EXPORT_COMPONENT_FACTORY(kcm_tasmatv, TasmaTvFactory("tasmatv"))

TasmaTv::TasmaTv(QWidget *parent,const QStringList &)
    : KCModule(TasmaTvFactory::componentData(), parent)
{
    KGlobal::locale()->setMainCatalog("tasma");  // Changed 2008 to 2009
    mainWidget = new TvConfig(this);

    QVBoxLayout *v = new QVBoxLayout(this);    // Ported
    v->addWidget(mainWidget);

    TasmaTvAbout = new KAboutData("tasmatv", 0, ki18n(  "TASMA Tv Card Configuration Module" ),  "0.1",
				     ki18n("TASMA Tv Card Configuration Module" ),
				     KAboutData::License_GPL,
				     ki18n("(c) 2005-2006, TUBITAK - UEKAE" ) );  // Ported to kde4

    TasmaTvAbout->addAuthor( ki18n("Enes Albay"),  ki18n( "Current Maintainer" ), "albayenes@gmail.com", "");   // Ported to kde4

    /*connect(mainWidget->tvModel, SIGNAL(selectionChanged()), SLOT(configChanged()));
    connect(mainWidget->tvVendor, SIGNAL(selectionChanged()), SLOT(tvVendorChanged()));
    connect(mainWidget->tunerModel, SIGNAL(selectionChanged()), SLOT(configChanged()));
    connect(mainWidget->tunerVendor, SIGNAL(selectionChanged()), SLOT(tunerVendorChanged()));
    connect(mainWidget->pllGroup, SIGNAL(pressed(int)), SLOT(configChanged()));
    connect(mainWidget->radioCard, SIGNAL(stateChanged(int)), SLOT(configChanged()));
    load();*/
}

/*void TasmaTv::load()
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
}*/
