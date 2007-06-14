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

#include "iksemelpp.h"
#include "iksemelpp-exception.h"

namespace IPP
{
	namespace DOM
	{

		DOM::DOM()
		{
			this->document = iks_new( "" );
		}

		DOM::DOM( DOM *node )
		{
			this->document = iks_copy( node->document );
		}

		DOM::DOM( const string name )
		{
			this->document = iks_new( name.c_str() );
		}

		DOM::DOM( DOM *node, const string name )
		{
			this->document = iks_new( name.c_str() );
			node->insertNode( this );
		}

		DOM::~DOM() 
		{
			iks_delete( this->document );
		}

		DOM* DOM::insertNode( DOM *node )
		{
			DOM *n = new DOM();
			
			n->document = iks_insert_node( this->document, node->document );
			return n;
		}

		DOM* DOM::insertCData( const string name ) 
		{
			DOM *n = new DOM();

			n->document = iks_insert_cdata( this->document, name.c_str(), name.length() );
			return n->moveParent();
		}

		DOM* DOM::insertAttribute( const string name, const string value ) 
		{
			DOM *n = new DOM();

			n->document = iks_insert_attrib( this->document, name.c_str(), value.c_str() );
			return n->moveParent();
		}

		DOM* DOM::moveNext() 
		{
			DOM *n = new DOM();

			n->document = iks_next( this->document );
			return n;
		}

		DOM* DOM::movePrev() 
		{
			DOM *n = new DOM();

			n->document = iks_prev( this->document );
			return n;
		}

		DOM* DOM::moveParent() 
		{
			DOM *n = new DOM();

			n->document = iks_parent( this->document );
			return n;
		}

		DOM* DOM::moveChild() 
		{
			DOM *n = new DOM();
	
			n->document = iks_child( this->document );
			return n;
		}

		DOM* DOM::moveAttribute() 
		{
			DOM *n = new DOM();

			n->document = iks_attrib( this->document );
			return n;
		}

		DOM* DOM::moveRoot() 
		{
			DOM *n = new DOM();
	
			n->document = iks_root( this->document );
			return n;
		}

		DOM* DOM::moveNextTag() 
		{
			DOM *n = new DOM();
		
			n->document = iks_next_tag( this->document );
			return n;
		}

		DOM* DOM::movePrevTag() 
		{
			DOM *n = new DOM();

			n->document = iks_prev_tag( this->document );
			return n;
		}
	
		DOM* DOM::moveFirstTag() 
		{
			DOM *n = new DOM();
	
			n->document = iks_first_tag( this->document );
			return n;
		}

		const enum ikstype DOM::getType() const 
		{
			return iks_type( this->document );
		}

		const string DOM::getName() const 
		{
			return iks_name( this->document );
		}
	
		const string DOM::getCData() const 
		{
			return iks_cdata( this->document );
		}

		const size_t DOM::getSizeCData() const 
		{
			return iks_cdata_size( this->document );
		}

		const bool DOM::hasChildren() const 
		{
			return iks_has_children( this->document );
		}

		const bool DOM::hasAttributes() const 
		{
			return iks_has_attribs( this->document );
		}

		DOM* DOM::findNode( const string name ) const 
		{
			DOM *n = new DOM();
	
			n->document = iks_find( this->document, name.c_str() );
			return n;
		}

		string DOM::findCData( const string name ) const 
		{
			return iks_find_cdata( this->document, name.c_str() );
		}

		string DOM::findAttribute( const string name ) const 
		{
			return iks_find_attrib( this->document, name.c_str() );
		}

		DOM* DOM::findWithAttribute( const string tagname, const string attrname, const string value ) const
		{
			DOM *n = new DOM();
		
			n->document = iks_find_with_attrib( this->document, tagname.c_str(), attrname.c_str(), value.c_str() );
			return n;
		}

		void DOM::loadFile( const string name ) 
		{
			int rc = iks_load( name.c_str(), &(this->document) );

			if( rc != IKS_OK )
				switch( rc )
				{
					case IKS_FILE_NOFILE:
						throw DOMException( "File doesn't exists..." );
						break;
					case IKS_FILE_NOACCESS:
						throw DOMException( "Permission denied..." );
						break;
					case IKS_FILE_RWERR:
						throw DOMException( "I/O error occured..." );
						break;
				}
		}

		void DOM::saveFile( const string name ) const 
		{
			int rc = iks_save( name.c_str(), this->document );

			if( rc != IKS_OK )
				switch( rc )
				{
					case IKS_FILE_NOACCESS:
						throw DOMException( "Permission denied..." );
						break;
					case IKS_FILE_RWERR:
						throw DOMException( "I/O error occured..." );
						break;
				}
		}

		const bool DOM::asBool() const 
		{
			return this->document;
		}

		iks* DOM::asData() 
		{
			return this->document;
		}

		void DOM::setData( iks *i ) 
		{
			this->document = i;
		}
	}
}
