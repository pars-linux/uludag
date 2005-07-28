/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <qstring.h>
#include <qstringlist.h>
#include <klocale.h>
#include <kdebug.h>

#include "htmlwriter.h"

HtmlWriter::HtmlWriter()
{
}

HtmlWriter::~HtmlWriter()
{
}

QString HtmlWriter::createHtml(const QStringList& packageList)
{
  if(packageList.isEmpty())
    return QString::null;

  QString result;
  int i=1;

  for(QStringList::ConstIterator it = packageList.begin(); it != packageList.end(); ++it)
    {
      result += QString("\n<font size=-2>\n"
			"<table width=100%>\n<tr>\n"
			"<td><b>"+i18n("Name")+" :</b> %1 <b>"+i18n("Group")+" :</b> %2</td>\n"
			"</tr>\n<tr>\n"
			"<td><b>"+i18n("Version")+" :</b> %3  <b>"+i18n("Install Date")+" :</b> %4</td>\n"
			"</tr>\n"
			"<tr>\n"
			"<td><b>"+i18n("Size")+" :</b> %5 "+ i18n("bytes")+"  <b>"+i18n("License")+" :</b> %6</td>\n"
			"</tr>\n"
			"<tbody>"
			"<tr><td style=\"background-color: #CCC\" align=\"right\"><a href=\"#\" onclick=\"linkClicked(this,'"+i18n("Less Information")+"','"+i18n("More Information")+"'); toggleItem('table"+QString::number(i)+"');\">"+i18n("More Information")+"</a></td></tr>"
			"</tbody>"
			"<tbody class=\"collapse_obj\" id=\"table"+QString::number(i)+"\">"
			"<tr><td><b>"+i18n("Summary")+" :</b> %7</td></tr></tbody>\n"
			"</table>\n"
			"</font><hr>\n").
	arg("Foo").arg("Bar").arg("0.0.1").arg("00.00.00").arg("1234").arg("GPL").arg("Summary");
      ++i;
    }

  return result;
}
