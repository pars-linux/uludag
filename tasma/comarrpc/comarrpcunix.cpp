/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <sys/socket.h>
#include <sys/un.h>

#include "comarrpcunix.h"
#include "comarxml.h"

bool ComarRPCUNIX::Connect( RPCparam& connect_params)
{
    char *sockFile = connect_params[ "sock_file" ];
    if ( !sockFile ) {
        qDebug( "Can not get socket_file" );
        return false;
    }

    struct sockaddr_un name;
    size_t size;

    _sock = socket( PF_LOCAL,  SOCK_STREAM,  0 );
    if ( _sock == -1 ) {
        qDebug( "Cannot open socket: %s", sockFile );
        return false;
    }

    name.sun_family = AF_LOCAL;
    strncpy( name.sun_path,  sockFile,  sizeof ( name.sun_path ) );
    size = ( offsetof ( struct sockaddr_un,  sun_path ) + strlen ( name.sun_path ) + 1 );
    if ( connect( _sock,  ( struct sockaddr * ) &name,  size ) != 0 ) {
        qDebug( "connect() failed." );
        return false;
    }

    return true;
}

bool ComarRPCUNIX::Auth( RPCparam& auth_params )
{
    char *user = auth_params[ "user" ];
    char *pass = auth_params[ "password" ];

    qDebug( "\nUsername: %s\tPassword: %s",
            user, pass );

    return true;
}

int ComarRPCUNIX::Send( RPCparam& send_params )
{
    ComarXML xml;

    if ( !xml.buildXML( send_params ) ) {
        return 0;
    }

    // XML verisini gönder.
    send( _sock,  xml.getXML(),  strlen( xml.getXML() ),  0 );

    // giden bayt sayısını geri döndür.
    // debug....
    return printf( "%s\n", xml.getXML() );
}

RPCparam* ComarRPCUNIX::Recv()
{
    // XML verisini al
    // RPCparam formatına dönüştür
    // RPCparam'ı geri döndür.

    RPCparam* param = new RPCparam();

    param->insert( "deneme", "12345" );

    return param;
}

