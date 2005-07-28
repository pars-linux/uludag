/*
  Copyright 2005 UEAKE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <khtmlview.h>
#include <khtml_part.h>

#include "packager_ui.h"
#include "htmlwriter.h"

Packager_UI::Packager_UI(QWidget* parent, const char* name)
  : Package_Manager(parent,name)
{
  KHTMLPart *khtmlpart =  new KHTMLPart (m_displayFrame);
  HtmlWriter *htmlWriter = new HtmlWriter();

  QString html = htmlWriter->createHtml("Foo");
  html += htmlWriter->createHtml("Foo");

  khtmlpart->begin();
  khtmlpart->write(html);
  khtmlpart->end();
  khtmlpart->view()->resize(400, 300); 
}

Packager_UI::~Packager_UI()
{}

#include "packager_ui.moc"
