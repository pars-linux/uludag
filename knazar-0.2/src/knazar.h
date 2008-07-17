/***************************************************************************
 *   Copyright (C) 2005, 2007 by TUBITAK/UEKAE                                   *
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

#ifndef _KNAZAR_H_
#define _KNAZAR_H_

#include <ksystemtray.h>
#include <qpixmap.h>
#include "knazardcop.h"

class KNazarBalloon;

class knazar : public KSystemTray, virtual public DCOPNazarIface
{
	Q_OBJECT
public:
	knazar();
public slots:
	void protect_from_harmfull_looks();
	void release_the_protection();
	bool is_protecting();
	void send_nazar();
	void about();
private:
	QPixmap trayIcon;
	bool protection_working;
	int number_of_attacks, defated_attacks;
	KNazarBalloon * balloon;
};

#endif
