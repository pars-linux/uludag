/*
  Copyright (c) 2004, 2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <kapplication.h>
#include <kstandarddirs.h>
#include <klocale.h>
#include <kconfig.h>
#include <kpushbutton.h>

#include "welcome.h"
#include "mouse.h"
#include "style.h"
#include "wallpaper.h"
#include "network.h"
#include "package.h"
#include "goodbye.h"

#include "kaptan.h"

Kaptan::Kaptan(QWidget *parent, const char *name)
    : KWizard(parent, name, true)
{
    int i = 0;
    setCaption(kapp->caption());

    /* Kaptan runs only at FirstRun */
    KConfig *config = kapp->config();
    config->setGroup("General");
    config->writeEntry("RunOnStart", false);
    config->sync();

    welcome = new Welcome(this);
    addPage(welcome, i18n("Welcome"));
    setHelpEnabled(KWizard::page(i++), false);

    mouse = new Mouse(this);
    addPage(mouse, i18n("Mouse Setup"));
    setHelpEnabled(KWizard::page(i++), false);

    style = new Style(this);
    addPage(style, i18n("Style Setup"));
    setHelpEnabled(KWizard::page(i++), false);

    wallpaper = new Wallpaper(this);
    addPage(wallpaper, i18n("Wallpaper Setup"));
    setHelpEnabled(KWizard::page(i++), false);

    network = new Network(this);
    addPage(network, i18n("Network Setup"));
    setHelpEnabled(KWizard::page(i++), false);

    package = new Package(this);
    addPage(package, i18n("Package Manager"));
    setHelpEnabled(KWizard::page(i++), false);

    goodbye = new Goodbye(this);
    addPage( goodbye, i18n("Congratulations"));
    setHelpEnabled(KWizard::page(i), false);

    setFinishEnabled(KWizard::page(i), true);

    locale = new KLocale("kaptan");
    locale->setLanguage(KLocale::defaultLanguage());

    // used for garbage collecting :)
    connect(kapp, SIGNAL(aboutToQuit()), this, SLOT(aboutToQuit()));
}

void Kaptan::aboutToQuit()
{
    delete welcome;
    delete mouse;
    delete style;
    delete wallpaper;
    delete network;
    delete package;
    delete goodbye;
}

void Kaptan::next()
{
    if (currentPage() == mouse)
        mouse->apply();
    else if (currentPage() == style)
        style->testStyle();
    else if (currentPage() == wallpaper)
    {
        if (wallpaper->changeWallpaper())
            wallpaper->setWallpaper();
        else
            wallpaper->resetWallpaper();
        network->embedManager();
    }
    else if (currentPage() == package)
        package->apply();

    KWizard::next();
}

#include "kaptan.moc"
