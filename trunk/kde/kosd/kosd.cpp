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

#include "kosd.h"

#include <kpluginfactory.h>
#include <kpluginloader.h>

K_PLUGIN_FACTORY(KOSDFactory,
                 registerPlugin<KOSD>();
        )

K_EXPORT_PLUGIN(KOSDFactory("kosd"))


KOSD::KOSD(QObject* parent, const QList<QVariant>& l)
    :KDEDModule(parent)
{
    // Create an OSD instance
    m_osd = new OSD();

    // Appear for 2 seconds and vanish
    m_osd->setTimeout(2);
}


KOSD::~KOSD()
{
    delete m_osd;
}


// Public slot (exposed via DBUS)
void KOSD::showOSD(QString icon, QString label, int percent)
{
    if (percent < 0)
        percent = 0;
    else if (percent > 100)
        percent = 100;

    m_osd->display(icon, label, percent);
}

#include "kosd.moc"
