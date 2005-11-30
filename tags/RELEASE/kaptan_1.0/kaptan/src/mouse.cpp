/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <kstandarddirs.h>
#include <kconfig.h>
#include <qlabel.h>
#include <qradiobutton.h>
#include <qpixmap.h>

#include "mouse.h"

#include <X11/Xlib.h>


MouseSetup::MouseSetup( QWidget *parent, const char* name )
    : MouseSetupDlg( parent, name )
{
    /* sol/sağ el ile kullanımı seç.
       X'i seçimi kullanması için tetikle...
       kcminputrc dosyasına seçimi yaz... */
    // right-handed default
    setHandedness( RIGHT_HANDED );

    connect( leftHanded, SIGNAL( clicked() ),
             this, SLOT( slotLeftHanded() ) );
    connect( rightHanded, SIGNAL( clicked() ),
             this, SLOT( slotRightHanded() ) );
}

MouseSetup::~MouseSetup()
{

}

void MouseSetup::setHandedness( int val )
{
    rightHanded->setChecked( false );
    leftHanded->setChecked( false );
    if ( val == RIGHT_HANDED ) {
        rightHanded->setChecked( true );
        mousePix->setPixmap(
            QPixmap( locate( "data", "kaptan/pics/mouse_rh.png" ) ) );
        handed = RIGHT_HANDED;
    }
    else {
        leftHanded->setChecked( true );
        mousePix->setPixmap(
            QPixmap( locate( "data", "kaptan/pics/mouse_lh.png" ) ) );
        handed = LEFT_HANDED;
    }

}

void MouseSetup::apply()
{
    unsigned char map[20];
    int num_buttons = XGetPointerMapping( kapp->getDisplay(), map, 20 );
    if ( num_buttons == 1 )
    {
        map[0] = ( unsigned char ) 1;
    }
    else if ( num_buttons == 2 )
    {
        if ( handed == RIGHT_HANDED )
        {
            map[0] = ( unsigned char ) 1;
            map[1] = ( unsigned char ) 3;
        } else {
            map[0] = ( unsigned char ) 3;
            map[1] = ( unsigned char ) 1;
        }
    }
    else // 3 or more buttons
    {
        if ( handed == RIGHT_HANDED )
        {
            map[0] = ( unsigned char ) 1;
            map[2] = ( unsigned char ) 3;
        } else {
            map[0] = ( unsigned char ) 3;
            map[2] = ( unsigned char ) 1;
        }
    }

        int retval;
        while ( ( retval = XSetPointerMapping(
                      kapp->getDisplay(), map, num_buttons ) ) == MappingBusy ) {};
}

void MouseSetup::save()
{
    KConfig *config = new KConfig( "kcminputrc" );
    config->setGroup( "Mouse" );

    if ( handed == RIGHT_HANDED )
        config->writeEntry( "MouseButtonMapping", QString( "RightHanded" ) );
    else
        config->writeEntry( "MouseButtonMapping", QString( "LeftHanded" ) );

    config->sync();
}
