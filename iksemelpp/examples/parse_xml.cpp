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
#include <string>
#include "iksemelpp.h"

using namespace std;
using namespace IPP::DOM;

class iksML
{
	public:
		iksML() { this->node = new DOM(); };
		bool loadXML( string filename );
		void printMeta();
	private:
		DOM *node;
};

bool iksML::loadXML( string filename )
{
	try
	{
		node->loadFile( filename );
	}
	catch(const exception &e)
	{
		cerr << e.what()<< endl;
	}
}

void iksML::printMeta()
{
	DOM *current_node;

	current_node = node->findNode( "Global" );
	current_node = current_node->findNode( "Meta" );

	for( current_node = current_node->moveFirstTag(); current_node->asBool(); current_node = current_node->moveNextTag() )
	{
		if( current_node->getName() == "Author" )
			for( DOM *t = current_node->moveFirstTag(); t->asBool(); t = t->moveNextTag() )
				cout << t->getName() + ": " + t->moveChild()->getName() << endl;
		else
			cout << current_node->getName() + ": " + current_node->moveChild()->getName() << endl;
	}
	delete current_node;
}

int main( int argc, char *argv[] )
{
	iksML * iksemel = new iksML();

	iksemel->loadXML( argv[1] );
	iksemel->printMeta();

	delete iksemel;

	return 0;
}
