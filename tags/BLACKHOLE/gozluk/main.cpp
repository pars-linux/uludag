/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*

	Gözlük için main.cpp
	
	Kaya Oğuz <kaya@kuzeykutbu.org>

*/

#include <qapplication.h>

#include "anapencere.h"


int main(int argc, char **argv)
{
	QApplication uyg(argc, argv);
	anaPencere k;
	k.show();
	
	uyg.setMainWidget(&k);
	return uyg.exec();
}
