/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qlistbox.h>
#include <qfile.h>
#include <kdebug.h>

#include "tvconfig.h"

TvConfig::TvConfig( QWidget *parent)
    : TvConfigUI(parent)
{
}

TvConfig::~TvConfig()
{
}

void TvConfig::saveOptions()
{
    int card, tuner;
    QFile bttv("/etc/modules.d/bttv");

    card = cardList->currentItem();
    tuner = tunerList->currentItem();

    if (bttv.open(IO_WriteOnly | IO_Truncate))
    {
	QTextStream os(&bttv);

	os << "### This file is automatically generated by tasma." << endl;
	os << "#" << endl;
	os << "# Please do not edit this file directly. All changes" << endl;
	os << "# made in this file will be lost." << endl;
	os << "#" << endl;
	os << endl;
	os << "options bttv card=" << card;

	if (tuner != AUTO_TUNER)
	    os << " " << "tuner=" << tuner - 1; 

	os << endl;

	bttv.close();
	system("/sbin/modules-update");
    }
}

// TODO: read dmesg for error or success 
void TvConfig::removeModule()
{
    QCString cmd = "/sbin/rmmod bttv";
    system(cmd);
}

// TODO: read dmesg for error or success 
void TvConfig::loadModule()
{
    QCString cmd; 
    int card, tuner;

    card = cardList->currentItem();
    tuner = tunerList->currentItem();

    if (tuner != AUTO_TUNER)
	cmd.sprintf("/sbin/modprobe bttv card=%d tuner=%d", card, tuner - 1);
    else
	cmd.sprintf("/sbin/modprobe bttv card=%d", card);

    system(cmd);	
}
