/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/


#include <kaboutdata.h>
#include <klineedit.h>
#include <qlabel.h>
#include <qlayout.h>
#include <comarrpc/comarrpcunix.h>

#include "comartestdlg.h"
#include "comartest.h"
#include "comartest.moc"

extern "C"
{
    KCModule *create_comartest( QWidget *parent, const char* name )
    {
        return new ComarTest( parent, name );
    }
};

ComarTest::ComarTest( QWidget* parent, const char *name )
    : KCmodule( parent, name )
{
    // FIXME: ui'den widget'ı oluştur...

    setButtons();
    load();
}

void ComarTest::load()
{
    ComarRPCUNIX rpc;

    RPCparam params;

    // bu veriler gui'den alinacak...
    params.insert( "sock_file", "/tmp/comar-test" );
    rpc.Connect( params );

    params.clear();
    params.insert( "user", "baris" );
    params.insert( "password", "gizli" );
    rpc.Auth( params );

    params.clear();
    params.insert( "rpctype", "OMCALL" );
    params.insert( "type", "method" );
    params.insert( "name", "none" );
    params.insert( "index", "0" );
    params.insert( "parameters", "yok" );
    rpc.Send( params );
}

void ComarTest::save()
{
}

void ComarTest::defaults()
{
}

QString ComarTest::quickHelp() const
{
    return i18n( "Comar Test gui" );
}

void ComarTest::configChanged()
{
    emit changed( true );
}
