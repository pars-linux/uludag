/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qapplication.h>

#include "gozlukwin.h"

int main ( int argc,  char **argv )
{
    QApplication app ( argc,  argv );

    GozlukWin win;
    win.setFixedSize( 400, 400 );
    win.show();

    QObject::connect( &win, SIGNAL( signalQuit() ),
                      &app, SLOT( quit() ) );

    app.setMainWidget( &win );

    return app.exec();
}


