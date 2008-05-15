/*
  Copyright (c) 2004, 2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <klocale.h>
#include <kconfig.h>
#include <kstandarddirs.h>
#include <kipc.h>

#include <qlabel.h>
#include <qcombobox.h>
#include <qcheckbox.h>
#include <qpixmap.h>
#include <qradiobutton.h>

#include <fixx11h.h>
#include <X11/Xlib.h>

#include "mouse.h"

Mouse::Mouse(QWidget *parent, const char* name)
    : MouseDlg(parent, name)
{
    mouseBox->insertItem(i18n("Right handed"), 0);
    mouseBox->insertItem(i18n("Left handed"), 1);

    connect(mouseBox, SIGNAL(activated(int)), this, SLOT(setHandedness(int)));

    emit(setHandedness(RIGHT_HANDED));
}

void Mouse::setHandedness(int item)
{
    if (item == RIGHT_HANDED) 
        pix_mouse->setPixmap(QPixmap(locate("data", "kaptan/pics/mouse_rh.png")));
    else
        pix_mouse->setPixmap(QPixmap(locate("data", "kaptan/pics/mouse_lh.png")));
    handed = item;
}

void Mouse::apply()
{
    unsigned char map[20];
    int num_buttons = XGetPointerMapping(kapp->getDisplay(), map, 20);

    if(num_buttons == 1)
    {
        map[0] = (unsigned char) 1;
    }
    else if(num_buttons == 2)
    {
        if (handed == RIGHT_HANDED)
        {
            map[0] = (unsigned char) 1;
            map[1] = (unsigned char) 3;
        }
        else
        {
            map[0] = (unsigned char) 3;
            map[1] = (unsigned char) 1;
        }
    }
    else // 3 buttons and more
    {
        if (handed == RIGHT_HANDED)
        {
            map[0] = (unsigned char) 1;
            map[2] = (unsigned char) 3;
        }
        else
        {
            map[0] = (unsigned char) 3;
            map[2] = (unsigned char) 1;
        }
        if(num_buttons >= 5)
        {
            // Apps seem to expect logical buttons 4,5 are the vertical wheel.
            // With mice with more than 3 buttons (not including wheel) the physical
            // buttons mapped to logical 4,5 may not be physical 4,5 , so keep
            // this mapping, only possibly reversing them.
            int pos;
            for(pos = 0; pos < num_buttons; ++pos)
                if(map[pos] == 4 || map[pos] == 5)
                    break;
            if(pos < num_buttons - 1)
            {
                map[pos] = checkReverse->isChecked() ? (unsigned char) 5 : (unsigned char) 4;
                map[pos+1] = checkReverse->isChecked() ? (unsigned char) 4 : (unsigned char) 5;
            }
        }
    }
    int retval;
    while ((retval = XSetPointerMapping(kapp->getDisplay(), map, num_buttons)) == MappingBusy) {};

    KConfig *config = new KConfig("kcminputrc");
    config->setGroup("Mouse");

    if (handed == RIGHT_HANDED)
        config->writeEntry("MouseButtonMapping", QString("RightHanded"));
    else
        config->writeEntry("MouseButtonMapping", QString("LeftHanded"));
    config->writeEntry("ReverseScrollPolarity", checkReverse->isChecked());
    config->sync();
    delete config;

    config = new KConfig("kdeglobals");
    config->setGroup("KDE");
    config->writeEntry("SingleClick", singleClick->isChecked());
    config->sync();
    delete config;

    KIPC::sendMessageAll(KIPC::SettingsChanged, KApplication::SETTINGS_MOUSE);
}

#include "mouse.moc"
