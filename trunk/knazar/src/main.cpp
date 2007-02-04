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

#include <kuniqueapplication.h>
#include <kaboutdata.h>
#include <kcmdlineargs.h>
#include <klocale.h>

static const char description[] = I18N_NOOP("KDE Nazar Application");

static const char version[] = "0.2";

static KCmdLineOptions options[] =
{
	KCmdLineLastOption
};

int main(int argc, char **argv)
{
	KAboutData about("knazar", I18N_NOOP("knazar"), version, description,
	KAboutData::License_GPL, "(C) 2005, 2007 TUBITAK/UEKAE", 0, 0, "bilgi@pardus.org.tr");
	about.addAuthor( "S.Çağlar Onur", 0, "caglar@pardus.org.tr" );

	KCmdLineArgs::init(argc, argv, &about);
	KCmdLineArgs::addCmdLineOptions( options );

	KCmdLineArgs *args = KCmdLineArgs::parsedArgs();

	KUniqueApplication app;

	knazar *mainWin = new knazar();

	app.setMainWidget( mainWin );
	mainWin->show();

	args->clear();

	return app.exec();
}

