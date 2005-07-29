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

  khtmlPart->setJScriptEnabled(true);

  createUI();
}

PackagerUI::~PackagerUI()
{
  delete khtmlPart;
  delete htmlWriter;
}

void PackagerUI::createUI()
{
  QStringList apps;
  apps << "Foo" << "Bar" << "Baz";
  QString html = htmlWriter->createHtml(apps);
  // HACK for now
  QString path = QString(getenv("PWD"))+QString("/functions.js");
  kdDebug() << "Got " << path << endl;

  QString startHtml = 
    "<html>"
    "<head>"
    "<script language=\"JavaScript\" src=\""+path+"\"></script>"
    "</head>"
    "<body onload=\"toggleAll('collapse')\">";

  khtmlPart->begin();
  khtmlPart->write(startHtml);
  khtmlPart->write(html);
  khtmlPart->write("</body></html>");
  khtmlPart->end();
  khtmlPart->view()->resize(400, 300);
}

#include "packagerui.moc"
