/***************************************************************************
 *   Copyright (C) 2005 by TUBITAK/UEKAE                                   *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#include <iostream>
#include "iksemelpp.h"

using namespace std;
using namespace IPP::Sax;

int pr_tag( void *udata, char *name, char **atts, int type ) 
{
	switch( type )
	{
		case IKS_OPEN:
			cout << "TAG <" << name << ">" << endl;
			break;
		case IKS_CLOSE:
			cout << "TAG </" << name << ">" << endl;
			break;
		case IKS_SINGLE:
			cout << "TAG <" << name << "/>" << endl;
			break;
	}

	if( atts ) 
	{
		int i = 0;
		while( atts[i] ) 
		{
			cout << "  ATTRIB " << atts[i] << "='" << atts[i+1] << "'" << endl;
			i += 2;
		}
	}

	return IKS_OK;
}

int pr_cdata( void *udata, char *data, size_t len ) 
{
	cout << "CDATA [";
	for( int i = 0; i < len; i++ )
		cout << data[i];
	cout << "]" << endl;
	
	return IKS_OK;
}

int main( int argc, char *argv[] ) 
{
	Sax *Parser = new Sax( pr_tag, pr_cdata );

	try 
	{
		Parser->loadFile( argv[1] );
		Parser->parse( 0, 1 );
	}
	catch( const exception &e )
	{
		cerr << e.what() << endl;
		exit(1);
	}

	cout << "Bytes parsed: " << Parser->bytes() << endl;
	cout << "Lines parsed: " << Parser->lines() << endl;

	delete Parser;

	return 0;
}
