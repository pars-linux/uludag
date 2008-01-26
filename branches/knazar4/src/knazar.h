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

#ifndef KNAZAR_H
#define KNAZAR_H

#include <KAboutApplicationDialog>
#include <KAction>
#include <KSystemTrayIcon>

class Knazar : public KSystemTrayIcon
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "tr.org.pardus.knazar")

public:
    Knazar(KAboutData *aboutData);

private:
    bool protection_working;
    int number_of_attacks, defated_attacks;
    KAction *actionAbout;
    KAction *actionProtect;
    KAction *actionRelease;
    KAboutApplicationDialog *aboutApplicationDialog;
    QIcon normalIcon;
    QIcon grayIcon;

public slots:
    void protect_from_harmful_looks();
    void release_the_protection();
    bool is_protecting();
    void send_nazar();
};

#endif
