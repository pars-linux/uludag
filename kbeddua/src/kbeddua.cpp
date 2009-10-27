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

#include "kbeddua.h"

#include <kglobal.h>
#include <klocale.h>
#include <kiconloader.h>
#include <kmessagebox.h>
#include <kpopupmenu.h>
#include <kaction.h>
#include <dcopclient.h>
#include <kapp.h>
#include <kprocess.h>

#include <qimage.h>
#include <qtooltip.h>

kbeddua::kbeddua()
    : DCOPObject( "DCOPNazarIface" ), KSystemTray( 0, "kbeddua" )
{
	// Insert TrayIcon
	trayIcon = KSystemTray::loadIcon( "kbeddua" );
	setPixmap( trayIcon );

	// Initialize and Register KNazar DCOP Interface so any KDE program can make Nazar easily
	if ( !kapp->dcopClient()->isRegistered() )
	{
		kapp->dcopClient()->registerAs( "kbeddua" );
		kapp->dcopClient()->setDefaultObject( objId() );
	}

	// Build PopupMenu
	KPopupMenu* menu = contextMenu();

	( new KAction( i18n( "I wish your firefox will crash!" ), "kbeddua", 0, this, SLOT( crash_firefox() ), this ) )->plug( menu );
	( new KAction( i18n( "I wish your kopete will crash!" ), "kbeddua", 0, this, SLOT( crash_kopete() ), this ) )->plug( menu );
	menu->insertSeparator();
	( new KAction( i18n( "About" ), "about", 0, this, SLOT( about() ), this ) )->plug( menu );

	// Initialize variables
	protection_working = true;
	number_of_attacks = defated_attacks = 0;
	QToolTip::add( this, i18n( "kbeddua - No Harmfull look allowed!" ));
}

// Slots
void kbeddua::crash_firefox()
{
	++number_of_attacks;

	if ( is_protecting() )
	{
		++defated_attacks;
		KMessageBox::information( 0, i18n( "Damn! KNazar is protecting this computer!" ));
	}
	else
	{
		proc = new KProcess( this );
		*proc << "/usr/bin/killall";
		*proc << "firefox-bin";
		proc->start();
	}
	QToolTip::add(this, i18n( "kbeddua - %1 attacks received so far, %2 are defated and %3 are received...")
					.arg( number_of_attacks)
					.arg( defated_attacks )
					.arg( number_of_attacks - defated_attacks ));
}

void kbeddua::crash_kopete()
{
	QToolTip::add(this, i18n( "kbeddua - %1 attacks received so far, %2 are defated and %3 are received...")
					.arg( number_of_attacks)
					.arg( defated_attacks )
					.arg( number_of_attacks - defated_attacks ));
}

bool kbeddua::is_protecting()
{
	DCOPClient *client = kapp->dcopClient();
	QByteArray replyData;
	QCString replyType;

	client->call("knazar", "DCOPNazarIface", "is_protecting()", 0, replyType, replyData);
	QDataStream reply(replyData, IO_ReadOnly);
	reply >> protection_working;
	return protection_working;
}

void kbeddua::about()
{
	KMessageBox::information( 0, i18n( "Attacks your computer with obsecured methods but be aware KNazar will protect you!" ));
}

#include "kbeddua.moc"
