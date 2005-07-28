/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <qstring.h>
#include <qstringlist.h>
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

  for(QStringList::ConstIterator it = packageList.begin(); it != packageList.end(); ++it)
    {
      kdDebug() << "It " << *it << endl;
      result += QString("\n<font size=-2><a href=\"#%1\">\n"
			"<table>\n<tr>\n"
			"<td><b>Name :</b> %2 <b>Group :</b> %3</td>\n"
			"</tr>\n<tr>\n"
			"<td><b>Version :</b> %4  <b>Install Date :</b> %5</td>\n"
			"</tr>\n"
			"<tr>\n"
			"<td><b>Size :</b> %6 bytes  <b>License :</b> %7</td>\n"
			"</tr>\n"
			"<tr>\n"
			"<td> <b>Summary :</b> %8</td>\n"
			"</tr>\n"
			"</table>\n"
			"</a></font><hr>\n").
	arg("foo").arg("Foo").arg("Bar").arg("0.0.1").arg("00.00.00").arg("1234").arg("GPL").arg("Summary");
    }

  return result;
}
