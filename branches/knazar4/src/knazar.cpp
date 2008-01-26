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

#include <KLocalizedString>
#include <KMenu>
#include <KMessageBox>
#include <QIcon>

#include "knazar.h"
#include "knazaradaptor.h"

Knazar::Knazar(KAboutData *aboutData)
    : KSystemTrayIcon("knazar")
{
    new KnazarAdaptor(this);
    QDBusConnection dbus = QDBusConnection::sessionBus();
    dbus.registerObject("/KNazar", this);

    aboutApplicationDialog = new KAboutApplicationDialog(aboutData);

    //Initialize actions
    actionAbout = new KAction(KIcon("help-about"), i18n("About KNazar"), this);
    actionProtect = new KAction(KIcon("flag-blue"), i18n("Protect"), this);
    actionRelease = new KAction(KIcon("flag-red"), i18n("Release"), this);

    // Connect actions
    connect(actionAbout, SIGNAL(triggered(bool)), aboutApplicationDialog, SLOT(show()));
    connect(actionProtect, SIGNAL(triggered(bool)), this, SLOT(protect_from_harmful_looks()));
    connect(actionRelease, SIGNAL(triggered(bool)), this, SLOT(release_the_protection()));

    // Add them to menu
    contextMenu()->addAction(actionProtect);
    contextMenu()->addAction(actionRelease);
    contextMenu()->addSeparator();
    contextMenu()->addAction(actionAbout);

    // Initialize variables
    protection_working = true;
    number_of_attacks = defated_attacks = 0;
    setToolTip(i18n("KNazar - No harmful look allowed!" ));
    normalIcon = icon();
    grayIcon.addPixmap(icon().pixmap(22, 22, QIcon::Disabled));
}

// Slots
void Knazar::protect_from_harmful_looks()
{
    if (!is_protecting())
    {
        KMessageBox::information(0, i18n("KNazar is starting to protect your Pardus Linux from harmful looks..."));

        setIcon(normalIcon);
        protection_working = true;
        setToolTip(i18n("KNazar - No harmful look allowed!"));
    }
}

void Knazar::release_the_protection()
{
    if ( is_protecting() )
    {
        KMessageBox::sorry(0, i18n("KNazar is stopping to protect your Pardus Linux from harmful looks..."));

        // Convert trayIcon to gray
        setIcon(grayIcon);

        protection_working = false;
        setToolTip(i18n("KNazar - You are completely demilitarized..."));
    }
}

void Knazar::send_nazar()
{
    ++number_of_attacks;

    if (is_protecting())
    {
        ++defated_attacks;
        showMessage(i18n("Nazar eliminated"), i18n("Nazar Received and eliminated successfuly"));
    }
    else
        showMessage(i18n("Nazar harmed"), i18n("Nazar Received and it HARMED!"), QSystemTrayIcon::Critical);

    setToolTip(i18n("KNazar - %1 attacks received so far, %2 are defated and %3 are received...")
                    .arg(number_of_attacks)
                    .arg(defated_attacks)
                    .arg(number_of_attacks - defated_attacks));
}

bool Knazar::is_protecting()
{
    return protection_working;
}
