/*
  Copyright (c) 2004, 2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qfile.h>
#include <qlabel.h>
#include <qcheckbox.h>
#include <qpushbutton.h>
#include <qstringlist.h>
#include <qpixmap.h>
#include <qimage.h>
#include <qmap.h>
#include <qtextstream.h>

#include <dcopref.h>
#include <dcopclient.h>
#include <kcombobox.h>
#include <kstandarddirs.h>
#include <kglobal.h>
#include <kstringhandler.h>
#include <kconfig.h>
#include <kapplication.h>

#include "wallpaper.h"

Wallpaper::Wallpaper( QWidget *parent, const char* name )
    : WallpaperDlg( parent, name )
{
    changePaper = true;
    selectedPaper = "";

    QStringList lst = KGlobal::dirs()->findAllResources("wallpaper", "*.desktop", false /* no recursion */, true /* unique files */ );
    QString line,lname,lang,langCode;

    // FIXME: What about other languages?
    lang = QString(getenv("LC_ALL"));
    if (lang == "tr_TR.UTF-8")
        langCode="Name[tr]";
    else
        langCode="Name";

    for(QStringList::Iterator it = lst.begin(); it != lst.end(); ++it)
    {
        if(!(*it).endsWith(".svgz.desktop"))
        {
                QFile desktopFile(*it);
                QTextStream stream(&desktopFile);
                desktopFile.open(IO_ReadOnly);

                bool foundName = false;
                while(!foundName && (line = stream.readLine()))
                {
                    if (line.startsWith(langCode))
                    {
                        lname = line.section("=",1,1);
                        foundName=true;
                    }
                }
            papers.insert(lname, (*it).remove(".desktop"));
            desktopFile.close();
        }
    }

    QMap<QString, QString>::ConstIterator it = papers.begin();
    for(; it != papers.constEnd(); ++it)
        wallpaperBox->insertItem(it.key());

    connect(testButton, SIGNAL(clicked()), this , SLOT(testWallpaper()));
    connect(wallpaperBox, SIGNAL(activated(int)), this, SLOT(paperSelected(int)));
    connect(changeCheck, SIGNAL(toggled(bool)), this, SLOT(optionChanged(bool)));

    emit paperSelected(0);

    // Backup old walpaper name
    DCOPClient *client = kapp->dcopClient();
    QByteArray replyData;
    QCString replyType;

    client->call("kdesktop", "KBackgroundIface", "currentWallpaper(int)", 6, replyType, replyData);
    QDataStream reply(replyData, IO_ReadOnly);
    reply >> oldWallpaper;
}

void Wallpaper::paperSelected(int item)
{
    QString file = papers[wallpaperBox->text(item)];
    pix_wallpaper->setPixmap(QPixmap(QImage(file)));
    selectedPaper = file;
}

void Wallpaper::testWallpaper()
{
    DCOPRef wall("kdesktop", "KBackgroundIface");
    DCOPReply reply = wall.call("setWallpaper", selectedPaper, 6);
}

void Wallpaper::setWallpaper()
{
    // KDesktop settings...
    // - Wallpaper is scaled
    KConfig *config = new KConfig("kdesktoprc");
    config->setGroup("Desktop0");
    config->writeEntry("WallpaperMode", "Scaled");
    config->writePathEntry("Wallpaper", selectedPaper);

    // Same wallpaper for alls desktops
    config->setGroup("Background Common");
    config->writeEntry("CommonDesktop", true);
    config->sync();
    delete config;

    // call dcop
    DCOPRef wall("kdesktop", "KBackgroundIface");
    DCOPReply reply = wall.call("setWallpaper", selectedPaper, 6);
}

void Wallpaper::optionChanged(bool dontChange)
{
    changePaper = !dontChange;
    wallpaperBox->setEnabled(!dontChange);
    testButton->setEnabled(!dontChange);
}

bool Wallpaper::changeWallpaper()
{
    return changePaper;
}

void Wallpaper::resetWallpaper()
{
    DCOPRef wall("kdesktop", "KBackgroundIface");
    DCOPReply reply = wall.call("setWallpaper", oldWallpaper, 6);
}

#include "wallpaper.moc"
