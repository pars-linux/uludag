/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef TASMA_NET_WIDGET_H
#define TASMA_NET_WIDGET_H

#include <kiconview.h>

class QTimer;
class KAboutData;

class Interface : public KIconViewItem
{
public:
    Interface( KIconView *parent, const QString& name, const QPixmap& icon );

};


class TasmaNetWidget : public KIconView
{
    Q_OBJECT

public:
    TasmaNetWidget( QWidget *parent = 0, const char *name = 0 );

protected slots:
    void updateInterfaces();
    void interfaceSelected( QIconViewItem* item );

private:
    KAboutData *_aboutData;
    QTimer *_timer;
};

#endif // TASMA_NET_WIDGET_H
