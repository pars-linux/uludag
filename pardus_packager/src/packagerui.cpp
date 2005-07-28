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

  QString startHtml = "<html>"
       "<head>"
        "   <script language=\"javascript\">"
    "function linkClicked(link, text1, text2) {"
    " var s = text1;"
    " if (link.state) { link.state = false; s = text2; }"
    "else link.state = true;"
    " while (link.firstChild) "
    "link.removeChild(link.firstChild); link.appendChild(document.createTextNode(s)); "
    "}"
    "function getItem(id)"
    "{"
      "var itm = false;"
      "if(document.getElementById)"
	"itm = document.getElementById(id);"
      "else if(document.all)"
	"itm = document.all[id];"
      "else if(document.layers)"
	"itm = document.layers[id];"
      "return itm;"
    "}"
  "function toggleItem(id)"
  "{"
   " itm = getItem(id);"
    "if(!itm)"
     " return false;"
    "if(itm.style.display == 'none')"
     " itm.style.display = '';"
  "else"
   "   itm.style.display = 'none';"
    "return false;"
  "}"
  "function toggleAll(dowhat)"
  "{"
   " var tags = document.getElementsByTagName('tbody');"
    "if(!tags)"
     " return false;"
    "for(var i = 0; i < tags.length; i++)"
      "{"
	"if(tags[i].className == 'collapse_obj')"
	  "{"
	   " if(dowhat == 'collapse')"
	      "tags[i].style.display = 'none';"
  "else"
	"      tags[i].style.display = '';"
	  "}"
   "}"
  "return false;"
  "}"
  "</script>"
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
