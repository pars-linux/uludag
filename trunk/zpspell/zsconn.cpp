/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <iostream>
#include <sstream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#include "zsconn.h"

#define HOST "localhost"
#define ZPORT 10444


ZSConn::ZSConn()
{
    struct hostent *he;
    struct sockaddr_in saddr;

    if ( ( he = (struct hostent *)gethostbyname(HOST) ) == NULL ) {
	perror( "gethostbyname()" );
    }

    if ( ( _conn = socket(AF_INET, SOCK_STREAM, 0) ) == -1 ) {
	perror( "socket()" );
    }

    saddr.sin_family = AF_INET;
    saddr.sin_port = htons( (uint16_t)ZPORT );
    saddr.sin_addr = *( (struct in_addr *)he->h_addr );
    memset( &(saddr.sin_zero), '\0', 8 );

    if ( connect(_conn, (struct sockaddr *)&saddr, sizeof(struct sockaddr)) == -1) {
        perror("connect()");
    }
}

ZSConn::~ZSConn()
{
    if ( _conn ) {
        shutdown( _conn, SHUT_RDWR );
        close( _conn );
    }
}

Z_CHECK_RESULT ZSConn::checkString( const string& str ) const
{
    // pislikleri temizle, bunlar ispell'e gönderilen komutlar.
    // şimdilik işimiz yok bunlarla
    string flags( "*&@+-~#!%`^" );
    string::iterator it = flags.begin();
    string::iterator end = flags.end();
    for ( ; it != end; ++it ) {
        if ( str[0] == *it ) {
            return Z_UNKNOWN;
        }
    }

    // new scope for temp. variables
    {
      stringstream strstream;
      strstream << str.length() << " " << str;
      string checkStr = strstream.str();
      if ( send(_conn, checkStr.c_str(), checkStr.length(), 0) == -1) {
        perror("send()");
      }
    }

    string check = recvResult();

    if ( check == "5 DOGRU" ) {
        return Z_TRUE;
    } else if ( check == "6 YANLIS" ) {
        return Z_FALSE;
    }

    return Z_UNKNOWN;
}

char* ZSConn::recvResult() const
{
    // FIXME: dönüş değeri 10 karakterden büyük olursa?
    // ZemberekServer protokolü belirlendikten sonra düzeltilecek.
    char *ret = new char[11];
    int numbytes=recv(_conn, ret, 10, 0);
    ret[numbytes]='\0';

    return ret;
}
