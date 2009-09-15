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
#include <KPluginFactory>
// #include <KSimpleConfig>

#include <Q3ListBox>
#include <QRadioButton>
#include <QButtonGroup>
#include <QCheckBox>
#include <QFile>
#include <QLayout>
#include <QVariant>
#include <QAction>
#include <iostream>

#include "tv-manager.h"
#include "tv-manager.moc"

// typedef KGenericFactory<TasmaTv, QWidget>::create(parent, &lst) TasmaTvFactory;
// K_EXPORT_COMPONENT_FACTORY(kcm_tvManager, TasmaTvFactory("tv-manager"))

TasmaTv::TasmaTv(QWidget *parent/*, const QVariantList &lst*/) : QWidget(parent)
   // : KCModule(TasmaTvFactory::componentData(), parent, lst)
{
    std::cout << "tv-manager signaling" << std::endl;
    KGlobal::locale()->setMainCatalog("tasma");  // Changed 2008 to 2009
    mainWidget = new TvConfig(this);
setWindowTitle("TV Manager");
    QVBoxLayout *v = new QVBoxLayout(this);    // Ported
    v->addWidget(mainWidget);

    TasmaTvAbout = new KAboutData("tv-managera", 0, ki18n(  "TASMA Tv Card Configuration Module" ),  "0.1",
				     ki18n("TASMA Tv Card Configuration Module" ),
				     KAboutData::License_GPL,
				     ki18n("(c) 2005-2006, TUBITAK - UEKAE" ) );  // Ported to kde4

    TasmaTvAbout->addAuthor( ki18n("Enes Albay"),  ki18n( "Current Maintainer" ), "albayenes@gmail.com", "");   // Ported to kde4

    connect(mainWidget->cardModList, SIGNAL(currentItemChanged(QListWidgetItem*, QListWidgetItem*)), SLOT(configChanged()));
    connect(mainWidget->cardManList, SIGNAL(currentItemChanged(QListWidgetItem*, QListWidgetItem*)), SLOT(cardManListChanged()));
    connect(mainWidget->tunerModList, SIGNAL(currentItemChanged(QListWidgetItem*, QListWidgetItem*)), SLOT(configChanged()));
    connect(mainWidget->tunerManList, SIGNAL(currentItemChanged(QListWidgetItem*, QListWidgetItem*)), SLOT(tunerManListChanged()));
    connect(mainWidget->pllGroup, SIGNAL(buttonClicked(int)), SLOT(configChanged()));
    connect(mainWidget->radioCard, SIGNAL(stateChanged(int)), SLOT(configChanged()));
    load();
    std::cout << "tv-manager awakened" << std::endl;
}

void TasmaTv::load()
{
    QVariant def;
    bool ok = true;
    KConfig *config = new KConfig("kcmtasmatvrc");
    KConfigGroup *group = new KConfigGroup(config, "System");
    mainWidget->selectCard(group->readEntry("Card", def).toInt(&ok));
    mainWidget->selectTuner(group->readEntry("Tuner", def).toInt(&ok));
    // mainWidget->pllGroup->setButton(group->readEntry("Pll", def).toInt(&ok));
    mainWidget->radioCard->setChecked(group->readEntry("Radio", def).toBool());
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
//    emit changed(true);
}

void TasmaTv::tunerManListChanged()
{
    mainWidget->tunerManListChanged();
}

void TasmaTv::cardManListChanged()
{
    mainWidget->cardManListChanged();
}
