/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef T_CATEGORY_VIEW_H
#define T_CATEGORY_VIEW_H

#include <qframe.h>

class TCategoryView;
class TIconView;
class QLabel;

class CategoryTitle : public QFrame
{
public:
    CategoryTitle( TCategoryView *view );
	
    void setPixmap( const QPixmap& icon );
    void setText( const QString& text );

private:
    QLabel *_pix;
    QLabel *_caption;
};

class TCategoryView : public QFrame
{
    Q_OBJECT
public:
    TCategoryView( QWidget *parent = 0, const char* name = 0 );
    virtual ~TCategoryView();

    void setCategory( const QString& path, const QString& icon, const QString& caption );

signals:
    void signalModuleSelected( KCModule*, const QString&, const QString& );

private:
    CategoryTitle *_title;
    TIconView *_iconview;
};

#endif // T_CATEGORY_VIEW_H
