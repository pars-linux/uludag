/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef TASMA_NET_H
#define TASMA_NET_H

#include <kcmodule.h>

class KAboutData;
class TasmaNetWidget;

class TasmaNet : public KCModule
{
    Q_OBJECT

public:
    TasmaNet( QWidget *parent = 0, const char* name = 0 );
    ~TasmaNet() {}

    virtual void load();
    virtual void save();
    virtual void defaults();
    virtual QString quickHelp() const;
    virtual const KAboutData *aboutData () const { return TasmaNetAbout; }

public slots:
    void configChanged();

private:
    TasmaNetWidget *mainWidget;
    KAboutData *TasmaNetAbout;

};

#endif // TASMA_NET_H
