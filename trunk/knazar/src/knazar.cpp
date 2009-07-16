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


#include "knazar.h"

#include <kglobal.h>
#include <klocale.h>
#include <kiconloader.h>
#include <kmessagebox.h>
#include <kpopupmenu.h>
#include <kaction.h>
#include <dcopclient.h>
#include <kapp.h>
#include <kiconeffect.h>
#include <kwin.h>
#include <kprocess.h>


#include <qimage.h>
#include <qtooltip.h>
#include <qtimer.h>

#include "knazarballoon.h"

knazar::knazar()
    : DCOPObject( "DCOPNazarIface" ), KSystemTray( 0, "knazar" )
{
	// Insert TrayIcon
	trayIcon = KSystemTray::loadIcon( "knazar" );
	setPixmap( trayIcon );

	// Initialize and Register KNazar DCOP Interface so any KDE program can make Nazar easily
	if ( !kapp->dcopClient()->isRegistered() )
	{
		kapp->dcopClient()->registerAs( "knazar" );
		kapp->dcopClient()->setDefaultObject( objId() );
	}


	// Build PopupMenu
	KPopupMenu* menu = contextMenu();

	( new KAction( i18n( "Protect" ), "ledgreen", 0, this, SLOT( protect_from_harmfull_looks() ), this ) )->plug( menu );
	( new KAction( i18n( "Release" ), "ledred", 0, this, SLOT( release_the_protection() ), this ) )->plug( menu );
	menu->insertSeparator();
	( new KAction( i18n( "About" ), "about", 0, this, SLOT( about() ), this ) )->plug( menu );

	// Initialize variables
	protection_working = true;
	number_of_attacks = defated_attacks = 0;
	QToolTip::add( this, i18n( "knazar - No harmful looks allowed!" ));
}

// Slots
void knazar::protect_from_harmfull_looks()
{
	if ( !is_protecting() )
	{
		KMessageBox::information( 0, i18n( "KNazar is protecting your Pardus Linux from harmful looks..." ));

		setPixmap( trayIcon );
		protection_working = true;
		QToolTip::add( this, i18n( "knazar - No armful looks allowed!" ));
	}
}

void knazar::release_the_protection()
{

	if ( is_protecting() )
	{
		KMessageBox::sorry( 0, i18n( "KNazar is not protecting your Pardus Linux from harmful looks..." ));

		// Convert trayIcon to gray
		QImage iconImage = trayIcon.convertToImage();
		KIconEffect::toGray( iconImage, 0.90 );
		QPixmap convertedTrayIcon;
		convertedTrayIcon.convertFromImage( iconImage );

		setPixmap( convertedTrayIcon );
		protection_working = false;
		QToolTip::add( this, i18n( "knazar - You are completely demilitarized..." ));
	}
}

void knazar::send_nazar()
{
	++number_of_attacks;

	if ( is_protecting() )
	{
		++defated_attacks;
		balloon = new KNazarBalloon( i18n( "<qt><nobr><b>Nazar received and eliminated successfuly</b></nobr><br><nobr></nobr></qt>" ), QString::null );
	}
	else
		balloon = new KNazarBalloon( i18n( "<qt><nobr><b>Nazar received and it HARMED!</b></nobr><br><nobr></nobr></qt>" ), QString::null );
	
	balloon->setAnchor( mapToGlobal( pos() ));
	balloon->show();
	
	KWin::setOnAllDesktops( balloon->winId(), true );
	
	QToolTip::add(this, i18n( "knazar - %1 attacks received so far, %2 of them are eliminated and %3 of them harmed us...")
					.arg( number_of_attacks)
					.arg( defated_attacks )
					.arg( number_of_attacks - defated_attacks ));
}

bool knazar::is_protecting()
{
	return protection_working;
}

void knazar::about()
{
	KMessageBox::information( 0, i18n( "KNazar is a useful part of the Pardus Linux" ));
}

#include "knazar.moc"
