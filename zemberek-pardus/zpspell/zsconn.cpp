/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <iostream>
#include <glib.h>

#include "zsconn.h"

ZSConn::ZSConn()
{
    GError *gerror = 0;
    g_type_init();

    connection = dbus_g_bus_get(DBUS_BUS_SYSTEM, &gerror);
    if (!connection)
    {
        g_error_free(gerror);
        perror("dbus_g_bus_get()");
    }
    proxy = dbus_g_proxy_new_for_name(connection,
                                      "net.zemberekserver.server.dbus",
                                      "/net/zemberekserver/server/dbus/ZemberekDbus",
                                      "net.zemberekserver.server.dbus.ZemberekDbusInterface");
}

ZSConn::~ZSConn()
{
    if (proxy)
        g_object_unref(proxy);
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
    gboolean result;
    GError *gerror = 0;

    if (!dbus_g_proxy_call(proxy, "kelimeDenetle", &gerror,
                           G_TYPE_STRING, str.c_str() ,G_TYPE_INVALID,
                           G_TYPE_BOOLEAN, &result, G_TYPE_INVALID))
    {
        g_error_free(gerror);
        return Z_UNKNOWN;
    }

    if (result)
        return Z_TRUE;
    else
        return Z_FALSE;
}

vector<string> ZSConn::getSuggestions(const string& str ) const
{
    char** suggs;
    GError* gerror = 0;
    vector<string> suggestions;

    if (!dbus_g_proxy_call(proxy, "oner", &gerror,
                           G_TYPE_STRING, str.c_str(), G_TYPE_INVALID,
                           G_TYPE_STRV, &suggs, G_TYPE_INVALID))
    {
        g_error_free(gerror);
        perror("getSuggestions()");
    }
    
    int suggs_len = g_strv_length(suggs);
    for (int i = 0; i < suggs_len; ++i)
        suggestions.push_back(string(suggs[i]));

    return suggestions;
}

