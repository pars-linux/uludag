/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#ifndef PACKAGERUI_H
#define PACKAGERUI_H

#include "package_manager.h"

class Packager_UI : public Package_Manager
{
  Q_OBJECT

 public:
  Packager_UI(QWidget *parent, const char* name);
  ~Packager_UI();
};

#endif
