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
#include <kmessagebox.h>
#include <kprocess.h>
#include <qcombobox.h>

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

    networkEnabled = checkComarACL("Net.Link.setConnection");
    if (networkEnabled)
    {
        network = new Network(this);
        addPage(network, i18n("Network Setup"));
        setHelpEnabled(KWizard::page(i++), false);
    }

    packageEnabled = checkComarACL("PackageHandler.setupPackage");
    if (packageEnabled)
    {
        package = new Package(this);
        addPage(package, i18n("Package Manager"));
        setHelpEnabled(KWizard::page(i++), false);
    }

    goodbye = new Goodbye(this);
    addPage( goodbye, i18n("Congratulations"));
    setHelpEnabled(KWizard::page(i), false);

    // migration tool integration
    KProcess *mig = new KProcess();
    *mig << locate("exe", "migration-users");
    connect(mig, SIGNAL(receivedStdout(KProcess *, char *, int)), this, SLOT(migration(KProcess *, char *, int)));
    mig->start(KProcess::DontCare, KProcess::Stdout);

    setFinishEnabled(KWizard::page(i), true);

    locale = new KLocale("kaptan");
    locale->setLanguage(KLocale::defaultLanguage());

    // used for garbage collecting :)
    connect(kapp, SIGNAL(aboutToQuit()), this, SLOT(aboutToQuit()));
}

bool Kaptan::checkComarACL(QString methodName)
{
    int cmd;
    unsigned int id;
    char *ret;

    comarConnection = comar_connect();
    comar_send(comarConnection, 0, COMAR_CHECKACL, methodName.ascii(), NULL);
    comar_wait(comarConnection, -1);
    comar_read(comarConnection, &cmd, &id, &ret);
    comar_disconnect(comarConnection);
    return (cmd != COMAR_DENIED);
}

void Kaptan::aboutToQuit()
{
    delete welcome;
    delete mouse;
    delete style;
    delete wallpaper;
    if (networkEnabled)
        delete network;
    if (packageEnabled)
        delete package;
    delete goodbye;
}

void Kaptan::next()
{
    if (currentPage() == mouse)
        mouse->apply();
    else if (currentPage() == style){
        if (style->testedStyle != style->styleBox->currentItem()){
            style->testStyle();
        }
    }
    else if (currentPage() == wallpaper)
    {
        if (wallpaper->changeWallpaper())
            wallpaper->setWallpaper();
        else
            wallpaper->resetWallpaper();
        if (networkEnabled)
            network->embedManager();
    }
    else if (currentPage() == package)
        package->apply();

    KWizard::next();
}

void Kaptan::migration(KProcess* mig, char* buffer, int buflen)
{
    int migrationUsers;
    sscanf(buffer, "%d", &migrationUsers);
    if (migrationUsers>0)
    {
        if (KMessageBox::questionYesNo(this, tr2i18n("An existing operating system is found on your computer. Do you want to migrate files and settings from there?")) == QMessageBox::Yes)
        {
            KProcess migration;
            migration << locate("exe", "migration");
            migration.start(KProcess::DontCare);
        }
    }
}

#include "kaptan.moc"
