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


ZString ZSConn::checkString( const string& str, int offset ) const
{
    ZString zstr( str, offset );

    // pislikleri temizle, bunlar ispell'e gönderilen komutlar.
    // şimdilik işimiz yok bunlarla
    // bir de ^ var ama o kullanılıyor bizim için...
    string flags( "*&@+-~#!%`" );
    string::iterator it = flags.begin();
    string::iterator end = flags.end();
    for ( ; it != end; ++it ) {
        if ( str[0] == *it ) {
            zstr.setStatus( Z_UNKNOWN );
            return zstr;
        }
    }


    zstr.setStatus( spellCheck( zstr.str() ) );

    if ( zstr.status() == Z_FALSE ) {
        zstr.setSuggestions( getSuggestions( zstr.str() ) );
        if ( zstr.suggestionCount() != 0 ) {
            zstr.setStatus( Z_SUGGESTION );
        }
    }

    return zstr;
}

enum Z_CHECK_RESULT ZSConn::spellCheck( const string& str ) const
{
    stringstream strstream;
    strstream << str.length()+2 << " * " << str;
    string checkStr = strstream.str();
    if ( send(_conn, checkStr.c_str(), checkStr.length(), 0) == -1) {
        perror("send()");
    }

    switch ( *(recvResult()) ) {
    case '*':
        return Z_TRUE;
        break;
    case '#':
        return Z_FALSE;
        break;
    default:
        return Z_UNKNOWN;
        break;
    }
}

vector<string> ZSConn::getSuggestions(const string& str ) const
{
    stringstream strstream;
    strstream << str.length()+2 << " & " << str;
    string checkStr = strstream.str();
    if ( send( _conn, checkStr.c_str(), checkStr.length(), 0 ) == -1 ) {
        perror( "send()" );
    }

    vector<string> suggestions;
    string result = recvResult();

    if ( result[0] != '&' ) {
        return suggestions;
    }

    string::iterator it = result.begin();
    string::iterator end = result.end();
    bool start = false;
    string tmp;
    for ( ; it != end; ++it ) {
        if ( *it == '(' ) {
            start = true;
            continue;
        }

        if ( !start ) continue;


        if ( *it == ',' ) {
            suggestions.push_back( tmp );
            tmp.erase();
            continue;
        } else if ( *it == ')' ) {
            suggestions.push_back( tmp );
            break;
        }

        tmp += *it;
    }

    return suggestions;
}


char* ZSConn::recvResult() const
{
    int numbytes = 0;
    string buf("");

    int size = 0;
    while (true) {
        char s;
        numbytes = recv (_conn, &s, 1, 0);

        // ' ' boşluk karakteri hiç gelmezse???
        if (s == ' ') {
            char *endptr;
            size = strtol (buf.c_str() , &endptr, 0);
            buf.erase();
            break;
        }

        buf += s;
    }
    static char *ret = new char[size];
    numbytes = recv (_conn, ret, size, 0);
    ret[numbytes]='\0';

    return ret;
}
