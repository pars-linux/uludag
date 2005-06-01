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

#include <fstream>
#include "iksemelpp.h"
#include "iksemelpp-exception.h"

namespace IPP
{
	namespace Sax
	{
		Sax::Sax( iksTagHook *tag_hook, iksCDataHook *cdata_hook ) 
		{
			this->parser = iks_sax_new( NULL, tag_hook, cdata_hook );

			if (parser == NULL)
				throw SaxException( "Allocation failed..." );
		}

		Sax::~Sax() 
		{
			iks_parser_delete( this->parser );
		}

		void Sax::parse( string data, size_t len, int finish ) 
		{
			int rc = iks_parse( this->parser, data.c_str(), len, finish);
	
			if (rc != IKS_OK)
				switch(rc)
				{
					case IKS_NOMEM:
						throw SaxException( "Not enough memory..." );
						break;
					case IKS_BADXML:
						throw SaxException( "XML document is not well-formed..." );
						break;
					case IKS_HOOK:
						throw SaxException( "Our hooks didn't like something..." );
						break;
					default:
						throw SaxException( "Unknown internal error..." );
				}
		}	
		
		void Sax::parse( size_t len, int finish ) 
		{
			int rc = iks_parse( this->parser, this->buffer.c_str(), len, finish);
	
			if (rc != IKS_OK)
				switch(rc)
				{
					case IKS_NOMEM:
						throw SaxException( "Not enough memory..." );
						break;
					case IKS_BADXML:
						throw SaxException( "XML document is not well-formed..." );
						break;
					case IKS_HOOK:
						throw SaxException( "Our hooks didn't like something..." );
						break;
					default:
						throw SaxException( "Unknown internal error..." );
				}
		}

		void Sax::loadFile( string filename )
		{
			string line;
			ifstream xmlFile;
			xmlFile.open( filename.c_str() );
			if( xmlFile )
				while( getline( xmlFile, line) )
					buffer += line + "\n";
			else
				throw SaxException( "Can't open the file..." );

			xmlFile.close();
		}
		
		unsigned long Sax::bytes() const 
		{
			return iks_nr_bytes( this->parser );
		}

		unsigned long Sax::lines() const 
		{
			return iks_nr_lines( this->parser );
		}

		Sax& Sax::reset() 
		{
			iks_parser_reset( this->parser );

			return *this;
		}
	}
}
