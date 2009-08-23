/*
    Copyright (c) 2009      by Marcin Kurczych          <tharkang@gmail.com>

    *************************************************************************
    *                                                                       *
    * This program is free software; you can redistribute it and/or modify  *
    * it under the terms of the GNU General Public License as published by  *
    * the Free Software Foundation; either version 2 of the License, or     *
    * (at your option) any later version.                                   *
    *                                                                       *
    *************************************************************************
*/
#include <iostream>

#include "mainwindow.h"
#include "streamstab.h"
#include "groupmanager.h"
#include "groupstab.h"
#include "trayicon.h"
#include "groupsconfig.h"
#include "rulesconfig.h"
#include "../bindings/sourcemanager.h"
#include "../bindings/sinkmanager.h"
#include "../bindings/sinputmanager.h"

MainWindow::MainWindow(QtPulseAudio::Context *context, QMainWindow *parent):QMainWindow(parent)
{
    setupUi(this);
    this->context = context;
    tabWidget = new QTabWidget(this);
    setCentralWidget(tabWidget);
    QObject::connect(this->context, SIGNAL(ready()), this, SLOT(contextReady()));
    QObject::connect(actionSettings, SIGNAL(triggered(bool)), this, SLOT(showSettings(bool)));
    createTray();
}

void MainWindow::createTray()
{
    trayIcon = new PandaTrayIcon(this);
    trayIcon->show();
}

void MainWindow::contextReady()
{
    pa_operation *o;
    
    o = context->subscribe((pa_subscription_mask_t) ( PA_SUBSCRIPTION_MASK_SINK |
				PA_SUBSCRIPTION_MASK_SOURCE |
				PA_SUBSCRIPTION_MASK_SINK_INPUT |
				PA_SUBSCRIPTION_MASK_CLIENT ) );
    if (!o) {
	std::cout << "pa_context_subscribe() failed" << std::endl;
	return;
    }
    pa_operation_unref(o);
    sinksTab = new StreamsTab(context->sinks(), this);
    sourcesTab = new StreamsTab(static_cast<QtPulseAudio::StreamManager *>(context->sources()), this);
    
    groupManager = new GroupManager(context->sinkInputs(), this);
    groupsTab = new GroupsTab(groupManager, this);
    
    tabWidget->addTab(sinksTab, QString("Output"));
    tabWidget->addTab(sourcesTab, QString("Input"));
    tabWidget->addTab(groupsTab, QString("Applications"));
    trayIcon->createActions();
}

void MainWindow::toggleVisibility()
{
    if(isVisible())
	hide();
    else
	show();
}

void MainWindow::showSettings(bool val)
{
    std::cout << "Show settings" << std::endl;
    KPageDialog *kpd = new KPageDialog(this);
    KPageWidgetItem *groupsItem = new KPageWidgetItem(new GroupsConfigWidget);
    groupsItem->setHeader("Groups");
    groupsItem->setName("Groups");
    groupsItem->setIcon(KIcon("document-folder-open"));;
    kpd->addPage(groupsItem);
    KPageWidgetItem *rulesItem = new KPageWidgetItem(new RulesConfigWidget);
    rulesItem->setHeader("Rules");
    rulesItem->setName("Rules");
    rulesItem->setIcon(KIcon("code-class"));
    kpd->addPage(rulesItem);
    kpd->setButtons( KDialog::Ok | KDialog::Cancel | KDialog::Apply );
    QObject::connect(kpd, SIGNAL(currentPageChanged(KPageWidgetItem*,KPageWidgetItem*)),
		     this, SLOT(settingsPageChanged(KPageWidgetItem*,KPageWidgetItem*)));
    kpd->show();
    settingsDialog = kpd;
}


void MainWindow::settingsPageChanged(KPageWidgetItem *current, KPageWidgetItem *prev)
{
    if(prev)
    {
	QObject::disconnect(settingsDialog, SIGNAL(applyClicked()), prev->widget(), SLOT(save()));
	QObject::disconnect(settingsDialog, SIGNAL(okClicked()), prev->widget(), SLOT(save()));
    }
    QObject::connect(settingsDialog, SIGNAL(applyClicked()), current->widget(), SLOT(save()));
    QObject::connect(settingsDialog, SIGNAL(okClicked()), current->widget(), SLOT(save()));
}