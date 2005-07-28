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
      result += QString("\n<a href=\"#%1\">\n"
			"<table>\n<tr>\n"
			"<td>Name : %2 Group: %3</td>\n"
			"</tr>\n<tr>\n"
			"<td>Version: %4  Install Date: %5</td>\n"
			"</tr>\n"
			"<tr>\n"
			"<td>Size: %6 bytes  License: %7</td>\n"
			"</tr>\n"
			"<tr>\n"
			"<td> Summary: %8</td>\n"
			"</tr>\n"
			"</table>\n"
			"</a><hr>\n").
	arg("foo").arg("Foo").arg("Bar").arg("0.0.1").arg("00.00.00").arg("1234").arg("GPL").arg("Summary");
    }

  return result;
}
