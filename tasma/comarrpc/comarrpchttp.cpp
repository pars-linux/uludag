/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qhttp.h>

#include "comarrpchttp.h"
#include "comarxml.h"


bool ComarRPCHTTP::Connect( RPCparam& connect_params)
{
    // parametreleri ayıkla, host ve port bilgisini al.
    char *host = connect_params[ "host" ];
    char *port = connect_params[ "port" ];

    // bağlan.
    _http = new QHttp( QString( host ),
                       QString( port ).toUInt() );
    qDebug ( "Connected to host %s, port %s",
             host, port );

    // bağlantı sağlandı ise "true" döndür.
    return true;
}

bool ComarRPCHTTP::Auth( RPCparam& auth_params )
{
    char *user = auth_params[ "user" ];
    char *pass = auth_params[ "password" ];

    qDebug( "\nUsername: %s\tPassword: %s",
            user, pass );

    return true;
}


int ComarRPCHTTP::Send( RPCparam& send_params )
{
    ComarXML xml;

    if ( !xml.buildXML( send_params ) ) {
        return 0;
    }

    // bu calismaz...
    _http->post( "/", *( xml.getXML() ) );
    return printf( "sending data succeeded...\n" );
}

RPCparam* ComarRPCHTTP::Recv()
{
    // XML verisini al
    // RPCparam formatına dönüştür
    // RPCparam'ı geri döndür.

    RPCparam* param = new RPCparam();

    param->insert( "deneme", "12345" );

    return param;
}

