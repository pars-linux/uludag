/*
  Copyright (c) 2004,2005 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qlabel.h>
#include <qpixmap.h>
#include <qtextbrowser.h>
#include <kstandarddirs.h>
#include <kprocess.h>

#include "goodbye.h"

Goodbye::Goodbye( QWidget *parent, const char* name )
    : GoodbyeDlg( parent, name )
{
    pix_goodbye->setPixmap( QPixmap( locate( "data", "kaptan/pics/kaptan_goodbye.png" ) ) );
    
    connect(finishLabel,SIGNAL(linkClicked(const QString&)),this,SLOT(startTasma()));
}

void Goodbye::startTasma()
{
  KProcess proc;
  proc << locate("exe", "tasma");
  proc.start(KProcess::DontCare);
}

#include "goodbye.moc"
