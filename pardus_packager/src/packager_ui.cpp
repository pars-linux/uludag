/*
  Copyright 2005 UEAKE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <khtmlview.h>
#include <khtml_part.h>

#include "packager_ui.h"

Packager_UI::Packager_UI(QWidget* parent, const char* name)
  : Package_Manager(parent,name)
{
  KHTMLPart *khtmlpart =  new KHTMLPart (m_displayFrame);
  khtmlpart->begin();
  khtmlpart->write("<a href=\"#test\"><b>Buraya incik boncuk</a>");
  khtmlpart->end();
  khtmlpart->view()->resize(400, 50); 
}

Packager_UI::~Packager_UI()
{}

#include "packager_ui.moc"
