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

int main( int argc, char *argv[] )
{
	DOM *document, *node, *element;
	
	document = new DOM("Document");
	node = new DOM( document, "Node");
	element = new DOM( node, "Element");
	
	document->insertAttribute("Version","1");
	document->insertAttribute("Version","3");
	document->insertAttribute("Revision","2");	

	element->insertCData("Tasma");
	
	DOM *copy = new DOM( document );
	delete document, node, element;
	
	try
	{
		copy->saveFile( "test.xml" );
	}
	catch(const exception& e)
	{
		cerr << e.what() << endl;
	}

	return 0;
}
