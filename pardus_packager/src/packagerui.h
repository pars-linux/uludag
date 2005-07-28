/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#ifndef PACKAGERUI_H
#define PACKAGERUI_H

#include "packagemanager.h"

class KHTMLPart;
class HtmlWriter;

class PackagerUI : public PackageManager
{
  Q_OBJECT

 public:
  PackagerUI(QWidget *parent, const char* name);
  ~PackagerUI();

 private:
  void createUI();

  KHTMLPart *khtmlPart;
  HtmlWriter *htmlWriter;
};

#endif
