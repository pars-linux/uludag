/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - main.h
  TasmaApp, inherited from KUniqueApplication.
*/

#ifndef MAIN_H
#define MAIN_H

#include <kuniqueapplication.h>

class TasmaMainWin;

class TasmaApp : public KUniqueApplication
{
 Q_OBJECT

   public:
  TasmaApp();
  virtual ~TasmaApp();

 private:
  TasmaMainWin *tasmawin;
};

#endif // MAIN_H
