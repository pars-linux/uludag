/***************************************************************************
 *   Copyright (C) 2005 - 2008 by TUBITAK/UEKAE                            *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/
#include <KAboutApplicationDialog>
#include <KAboutData>
#include <KAction>
#include <KCmdLineArgs>
#include <KMenu>
#include <KSystemTrayIcon>
#include <KUniqueApplication>

int main (int argc, char *argv[])
{
    KAboutData aboutData(
        "knazar", 0,
        ki18n("knazar"), KNAZAR_VERSION,
        ki18n("KDE Nazar Application"),
        KAboutData::License_GPL_V2,
        ki18n("Copyright (c) 2005 - 2008 TUBITAK/UEKAE"),
        ki18n("KNazar is a usefull part of the Pardus Linux"),
        "http://www.pardus.org.tr",
        "bilgi@pardus.org.tr");
    aboutData.addAuthor(ki18n("S. Çağlar Onur"), ki18n("Author"), "caglar@pardus.org.tr");
    aboutData.addAuthor(ki18n("Uğur Çetin"), ki18n("KDE4 porter"), "jnmbk@users.sourceforge.net");
    KCmdLineArgs::init(argc, argv, &aboutData);

    if (!KUniqueApplication::start())
        return 0;
    KUniqueApplication app;

    //TODO: move following codes to knazar.cpp
    KSystemTrayIcon icon("knazar");
    KAction aboutAction("about", &icon);
    aboutAction.setText(i18n("About KNazar"));
    KAboutApplicationDialog aboutApplicationDialog(&aboutData);
    aboutAction.connect(&aboutAction, SIGNAL(triggered(bool)), &aboutApplicationDialog, SLOT(show()));
    icon.contextMenu()->addAction(&aboutAction);
    icon.show();

    return app.exec();
}
