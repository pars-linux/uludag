/*
  Copyright (c) 2004,2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <kconfig.h>
#include <kstandarddirs.h>
#include <kprocess.h>
#include <qcheckbox.h>
#include <qlabel.h>
#include <qpixmap.h>
#include <qspinbox.h>

#include "package.h"

Package::Package(QWidget *parent, const char* name)
    : PackageDlg(parent, name)
{
    pix_package->setPixmap(QPixmap(locate("data","kaptan/pics/pisi.png")));

    connect(showTray, SIGNAL(toggled( bool)), this, SLOT(traySelected(bool)));
    connect(checkUpdate, SIGNAL(toggled(bool)), this, SLOT(updateSelected(bool)));
}

void Package::traySelected(bool state)
{
    checkUpdate->setEnabled(state);
    updateInterval->setEnabled(showTray->isChecked() && checkUpdate->isChecked());
}

void Package::updateSelected(bool state)
{
    updateInterval->setEnabled(state);
}

void Package::apply()
{
    KConfig *config = new KConfig("package-managerrc");
    config->setGroup("General");
    config->writeEntry("SystemTray", showTray->isChecked());
    config->writeEntry("UpdateCheck", checkUpdate->isChecked());
    config->writeEntry("UpdateCheckInterval", updateInterval->value() * 60);
    config->sync();
    delete config;

    // start package-manager immediately
    if(showTray->isChecked())
    {
        KProcess proc;
        proc << locate("exe", "package-manager");
        proc.start(KProcess::DontCare);
    }
}

#include "package.moc"
