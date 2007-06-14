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

#ifndef IKSEMELPP_H
#define IKSEMELPP_H

#include <string>
#include "iksemel.h"

#ifdef HAVE_GC
#include <gc_cpp.h>
#endif

namespace IPP
{
	using std::string;

	namespace Stack
	{
#ifdef HAVE_GC
		class Stack: public gc
#else
		class Stack
#endif
		{
			public:
				Stack( size_t, size_t );
				~Stack();

				void * allocStack( Stack *, size_t );
				void * strdupStack( Stack *, const string , size_t );
			private:
				ikstack *stack;
		};
	};

	namespace DOM
	{
#ifdef HAVE_GC
		class DOM: public gc
#else
		class DOM
#endif
		{
			public:
				// Creating a Tree
				DOM();
				DOM( DOM *);
				DOM( const string );
				DOM( DOM *, const string );
						
				~DOM();
				
				// Modify Tree
				DOM* insertNode( DOM * );
				DOM* insertCData( const string );
				DOM* insertAttribute( const string, const string );
			
				// Accessing a Tree
				
				DOM* moveNext();
				DOM* movePrev();
				DOM* moveParent();
				DOM* moveChild();
				DOM* moveAttribute();
				DOM* moveRoot();
				DOM* moveNextTag();
				DOM* movePrevTag();
				DOM* moveFirstTag();
		
				const enum ikstype getType() const;

				const string getName() const;
				const string getCData() const;
				const size_t getSizeCData() const;
			
				const bool hasChildren() const;
				const bool hasAttributes() const;

				DOM* findNode( const string ) const;
				string findCData( const string ) const;
				string findAttribute( const string ) const;
				DOM* findWithAttribute( const string, const string, const string ) const;

				void loadFile( const string );
				void saveFile( const string ) const;

				const bool asBool() const;
				iks *asData();
				void setData( iks * );
			private:
				iks *document;
		};
	};

	namespace Sax
	{
		using namespace std;
#ifdef HAVE_GC
		class Sax: public gc 
#else
		class Sax
#endif
		{
			public:
				Sax( iksTagHook *, iksCDataHook * );
				~Sax();

				void parse( string, size_t, int );
				void parse( size_t, int );
				void loadFile( string );
				unsigned long bytes() const;
				unsigned long lines() const;
				Sax& reset();
			private:
				iksparser *parser;
				string buffer;
		};
	};
};

#endif
