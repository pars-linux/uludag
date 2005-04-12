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
#include <sstream>
#include <getopt.h>

#include "zstring.h"
#include "zsconn.h"
#include "config.h"

using namespace std;

static const string desc = "@(#) Zemberek Turkish spell checker ";


static int checkAndPrint( ZSConn& zemberek, const string str, int offset )
{
    ZString zstr = zemberek.checkString( str, offset );
    switch ( zstr.status() ) {
    case Z_TRUE:
        cout << "*" << endl;
        break;
    case Z_FALSE:
        cout << "# " << zstr.str() << " 0" << endl;
        break;
    case Z_SUGGESTION:
        cout << "& " <<
            zstr.str() << " " <<
            zstr.suggestionCount() << " " <<
            zstr.offset() << ": " <<
            zstr.suggestionString() << endl;
        break;
    default:
    	return -1;
        break;
    }

    return 0;
}

/* Ispell style interactive mode */
static int z_interactive_mode( ZSConn& zemberek )
{
    cout << desc << VERSION << endl;

    while ( true ) {
        char buf[BUFSIZ];
        char *t;

        cin.getline( buf, BUFSIZ );
        t = buf;
        int offset = 0, count = 0, ret = 0;
        bool inWord = true;
        string str( "" );
        while ( *t ) {
            if ( *t == ' ' || *t == '\t' ) {

                if ( !(str.empty()) ) {
                    ret = checkAndPrint( zemberek, str, offset );
                }

                inWord = false;
                str.erase();
                goto CONTINUE_LOOP;
            }

            if ( !inWord ) {
                offset = count;
                inWord = true;
            }

            str += *t;
        CONTINUE_LOOP:
            ++t; ++count;
        }

        // process the last word (if any)
        if ( !(str.empty()) ) {
            ret = checkAndPrint( zemberek, str, offset );
        }

	if ( ret == 0 ) cout << endl;
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
