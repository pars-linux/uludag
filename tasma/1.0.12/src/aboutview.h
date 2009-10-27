/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - aboutview.h
  AboutView, first screen
*/

#ifndef ABOUT_VIEW_H
#define ABOUT_VIEW_H

#include <qwidget.h>

class QPixmap;
class KPixmap;
class QRect;

class AboutView : public QWidget
{

 public:
  AboutView( QWidget *parent = 0, const char *name = 0 );

 protected:
  void paintEvent( QPaintEvent *e );

 private:
  void updateView( const QRect& rect );
  QPixmap *_tasmaLogo;
  KPixmap *_pardusLogo;
};

#endif //ABOUT_VIEW
