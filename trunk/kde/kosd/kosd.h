/***************************************************************************
 *   Copyright (C) 2008-2009 by Marcel Hasler <mahasler_at_gmail.com>      *
 *   Copyright (C) 2010 by Ozan Çağlayan <ozan_at_pardus.org.tr>           *
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

#ifndef KOSD_H
#define KOSD_H

#include "kosd_osd.h"
#include <kdedmodule.h>


class KOSD: public KDEDModule
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "org.kde.KOSD")
    public:
        KOSD(QObject* parent, const QList<QVariant>&);
        ~KOSD();

    public Q_SLOTS:
        /** D-Bus call to display an OSD notification.
         *  @param icon determines the icon to show in the OSD widget
         *  @param label determines the label to show in the OSD widget
         *  @param percent determines the progress ratio to be showed in the OSD widget
         */
        Q_SCRIPTABLE void showOSD(QString icon, QString label, int percent);

    private:
        OSD *m_osd;     // OSD instance
};

#endif // KOSD_H
