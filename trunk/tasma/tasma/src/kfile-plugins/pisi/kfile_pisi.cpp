/*
  Copyright (c) 2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <kgenericfactory.h>
#include <kstringhandler.h>
#include <klocale.h>

#include <qfile.h>
#include <qstringlist.h>
#include <qdatetime.h>

extern "C" {
#include <iksemel.h>
#include "zip.h"
}

#include "kfile_pisi.h"

typedef KGenericFactory<PisiPlugin> PisiFactory;

K_EXPORT_COMPONENT_FACTORY(kfile_pisi, PisiFactory("kfile_pisi"))

PisiPlugin::PisiPlugin(QObject *parent, const char *name, const QStringList &args) : KFilePlugin(parent, name, args)
{
    KGlobal::locale()->insertCatalogue("tasma");

    KFileMimeTypeInfo* info = addMimeTypeInfo( "application/x-pisi" );

    KFileMimeTypeInfo::GroupInfo* group = 0L;
    group = addGroupInfo(info, "Package", i18n("PiSi Package Info"));

    KFileMimeTypeInfo::ItemInfo* item;

    item = addItemInfo(group, "Name", i18n("Name"), QVariant::String);
    setHint(item, KFileMimeTypeInfo::Name);
    item = addItemInfo(group, "Description", i18n("Description"), QVariant::String);
    item = addItemInfo(group, "Size", i18n("Size"), QVariant::Int);
    setHint(item, KFileMimeTypeInfo::Size);
    setUnit(item, KFileMimeTypeInfo::KiloBytes);
}

bool PisiPlugin::readInfo(KFileMetaInfo& info, uint)
{
    KFileMetaInfoGroup group = appendGroup(info, "Package");
    int err;

    zip *pisi = zip_open(info.path().data(), &err);

    if (err)
      return false;

    iks *x = zip_load_xml(pisi, "metadata.xml", &err);

    if (err)
      {
        zip_close(pisi);
        return false;
      }

    appendItem(group, "Name", iks_cdata(iks_child(iks_find(iks_find(x, "Package"), "Name"))));
    appendItem(group, "Size", QString(iks_cdata(iks_child(iks_find(iks_find(x, "Package"), "InstalledSize")))).toInt()/1024);

    QString lang,description;

    lang = KGlobal::locale()->language();

    description = QString::fromLocal8Bit(iks_cdata(iks_child(iks_find_with_attrib(iks_find(x, "Package"), "Summary", "xml:lang", lang))));

    if (description.isEmpty())
      description = iks_cdata(iks_child(iks_find(iks_find(x, "Package"), "Summary")));

    appendItem(group, "Description", KStringHandler::rsqueeze(description,80));

    zip_close(pisi);
    iks_delete(x);

    return true;
}

#include "kfile_pisi.moc"
