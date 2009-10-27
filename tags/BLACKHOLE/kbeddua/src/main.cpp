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

#include <kuniqueapplication.h>
#include <kaboutdata.h>
#include <kcmdlineargs.h>
#include <klocale.h>

static const char description[] = I18N_NOOP("KDE Beddua Application");

static const char version[] = "0.1";

static KCmdLineOptions options[] =
{
	KCmdLineLastOption
};

int main(int argc, char **argv)
{
	KAboutData about("kbeddua", I18N_NOOP("kbeddua"), version, description,
	KAboutData::License_GPL, "(C) 2007 TUBITAK/UEKAE", 0, 0, "bilgi@uludag.org.tr");
	about.addAuthor( "S.Çağlar Onur", 0, "caglar@uludag.org.tr" );

	KCmdLineArgs::init(argc, argv, &about);
	KCmdLineArgs::addCmdLineOptions( options );

	KCmdLineArgs *args = KCmdLineArgs::parsedArgs();

	KUniqueApplication app;

	kbeddua *mainWin = new kbeddua();

	app.setMainWidget( mainWin );
	mainWin->show();

	args->clear();

	return app.exec();
}

