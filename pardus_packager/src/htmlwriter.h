/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#ifndef HTMLWRITER_H
#define HTMLWRITER_H

class QStringList;
class QString;

class HtmlWriter
{
 public:
  HtmlWriter();
  ~HtmlWriter();

  QString createHtml(const QStringList& programList);
};

#endif
