/***************************************************************************
 *   Copyright (C) 2007 by TUBITAK/UEKAE                                   *
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

#ifndef _KBEDDUA_H_
#define _KBEDDUA_H_

#include <ksystemtray.h>
#include <qpixmap.h>

#include "kbedduadcop.h"

class KProcess;

class kbeddua : public KSystemTray, virtual public DCOPBedduaIface
{
	Q_OBJECT
public:
	kbeddua();

public slots:
	bool is_protecting();
	void crash_firefox();
	void crash_kopete();
	void about();

private:
	QPixmap trayIcon;
	KProcess *proc;

	bool protection_working;
	int number_of_attacks, defated_attacks;
};

#endif
