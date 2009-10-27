/*
  Copyright (c) 2004, 2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef STYLE_H
#define STYLE_H

#include <qdom.h>

#include "styledlg.h"

class Style:public StyleDlg
{
    Q_OBJECT

public:
    Style(QWidget *parent = 0, const char* name = 0);

public slots:
    void styleSelected(int);
    void testStyle();

protected slots:
    void kickoffSelected();


private:
    QDomDocument dom;
    QString selectedStyle;
    QString getProperty(QDomElement parent, const QString & tag, const QString & attr) const;
};

#endif // STYLE_H
