/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef QUESTION_H
#define QUESTION_H

#include "questiondlg.h"

class Question : public QuestionDlg
{
public:
    Question ( QWidget *parent = 0, const char* name = 0, QString title = "Pardus Linux" );
};

#endif // QUESTION_H
