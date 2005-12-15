/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef __TASMATV_H__
#define __TASMATV_H__

#include <kcmodule.h>
#include "tvconfig.h"

#define AUTO_CARD 0
#define AUTO_TUNER 0

class KAboutData;
class TvConfigUI;

class TasmaTv : public KCModule
{
    Q_OBJECT
public:
    TasmaTv( QWidget *parent = 0, const char* name = 0, const QStringList &lst = QStringList());
    ~TasmaTv() {}

    virtual void load();
    virtual void save();
    virtual void defaults();
    virtual QString quickHelp() const;

public slots:
    void configChanged();

private:
    TvConfig *mainWidget;
    KAboutData *TasmaTvAbout;
};

#endif // __TASMATV_H__
