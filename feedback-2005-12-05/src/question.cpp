/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include "question.h"

#include <kstandarddirs.h>

#include <qlabel.h>
#include <qpixmap.h>

Question::Question( QWidget *parent, const char* name )
	: QuestionDlg( parent, name )
{
	questionPixmap->setPixmap(QPixmap( locate( "data", "feedback/pics/feedback.png" ) ) );
}
