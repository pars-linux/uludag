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
#include <kactioncollection.h>
#include <kicon.h>
#include "mainwindow.h"
#include "groupmanager.h"
#include "trayicon.h"
#include "group.h"
#include "slideraction.h"


PandaTrayIcon::PandaTrayIcon(MainWindow* parent): KSystemTrayIcon("audio-headset", parent)
{
    mainWindow = parent;
    QObject::connect(this, SIGNAL(activated(QSystemTrayIcon::ActivationReason)), 
		     this, SLOT(trayIconActivated(QSystemTrayIcon::ActivationReason)));
}

void PandaTrayIcon::trayActivated(QSystemTrayIcon::ActivationReason reason)
{
    mainWindow->toggleVisibility();
}


void PandaTrayIcon::createActions()
{
    foreach(QString g, mainWindow->groupManager->groupNames())
    {
	std::cerr << "Creating action" << std::endl;
	Group *group = mainWindow->groupManager->group(g);
	SliderAction *sliderAction = new SliderAction(this);
	sliderAction->setWidgetIcon(KIcon(group->iconName()));
	sliderAction->setWidgetToolTip(group->name());
	sliderAction->setValue(group->volume());
	QObject::connect(sliderAction, SIGNAL(valueChanged(int)),
			 group, SLOT(setVolume(int)));
	QObject::connect(group, SIGNAL(volumeChanged(int)),
			 sliderAction, SLOT(setValue(int)));
	this->contextMenu()->addAction(sliderAction);
    }
}










