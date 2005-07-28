/*
  Copyright 2005 UEAKE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <klocale.h>
#include <khtmlview.h>
#include <khtml_part.h>

#include "packagerui.h"
#include "htmlwriter.h"

PackagerUI::PackagerUI(QWidget* parent, const char* name)
  : PackageManager(parent,name)
{
  setCaption(i18n("Package Manager"));

  khtmlPart =  new KHTMLPart (m_displayFrame);
  htmlWriter = new HtmlWriter();

  QString html = htmlWriter->createHtml("Foo");
  html += htmlWriter->createHtml("Foo");

  khtmlPart->begin();
  khtmlPart->write(html);
  khtmlPart->end();
  khtmlPart->view()->resize(400, 300); 
}

PackagerUI::~PackagerUI()
{
  delete khtmlPart;
  delete htmlWriter;
}

#include "packagerui.moc"
