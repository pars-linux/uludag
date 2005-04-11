/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  ISpell-like, command line ZemberekServer client.
*/

#include <iostream>
#include <getopt.h>

#include "zstring.h"
#include "zsconn.h"
#include "config.h"

using namespace std;

static const string desc = "@(#) Zemberek Turkish spell checker ";

/* Ispell style interactive mode */
int z_interactive_mode( ZSConn& zemberek )
{
    cout << desc << VERSION << endl;

    string str;
    while ( true ) {
        str = "";
        cin >> str;

        if ( str.empty() )
            return 0;

        // offset bilgisini de alarak birden fazla string gönderebilmeliyiz...
        ZString zstr = zemberek.checkString( str, 0 );
        switch ( zstr.status() ) {
        case Z_TRUE:
            cout << "*" << endl << endl;
            break;
        case Z_FALSE:
            cout << "# " << zstr.str() << " 0" << endl << endl;
            break;
        case Z_SUGGESTION:
            cout << "& " <<
                zstr.str() << " " <<
                zstr.suggestionCount() << " " <<
                zstr.offset() << ": " <<
                zstr.suggestionString() << endl << endl;
            break;
        default:
            break;
        }

    }

    return 0;
}


int main( int argc, char** argv )
{
    bool aflag = false;
    int o;
    while ( ( o = getopt( argc, argv, "a" )) != -1 ) {
        switch ( o ) {
        case 'a':
            aflag = true;
            break;
        default:
            cerr << "Bilinmeyen parametre: " << optopt << endl;
        }
    }

    ZSConn zemberek;

    // start interactive mode and finalize.
    if ( aflag ) {
        return z_interactive_mode( zemberek );
    }

/*
    for ( int i = 1; i < argc; ++i ) {
        string str( argv[i] );
        cout << str;

        switch ( zemberek.checkString( str ) ) {
        case Z_TRUE:
            cout << ": DOGRU" << endl;
            break;
        case Z_FALSE:
            cout << ": YANLIS" << endl;
            break;
        default:
            break;
        }

    }
*/

    return 0;
}
