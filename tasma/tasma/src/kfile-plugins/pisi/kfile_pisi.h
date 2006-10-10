/*
  Copyright (c) 2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef __KFILE_PISI_H__
#define __KFILE_PISI_H__
       
#include <kfilemetainfo.h>
       
class QStringList;
       
class PisiPlugin: public KFilePlugin
{
    Q_OBJECT

public:
    PisiPlugin(QObject *parent, const char *name, const QStringList& args);
    virtual bool readInfo( KFileMetaInfo& info, uint what);
};

#endif // __KFILE_PISI_H__
