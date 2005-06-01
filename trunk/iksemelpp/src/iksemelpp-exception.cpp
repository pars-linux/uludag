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

#include "iksemelpp-exception.h"

namespace IPP
{

	exception::exception(const string& message)
	: message(message)
	{}

	exception::~exception() throw()
	{}

	const char* exception::what() const throw()
	{
		return this->message.c_str();
	}

	void exception::Raise() const
	{
		throw *this;
	}
	
	exception * exception::Clone() const
	{
		return new exception(*this);
	}	

	namespace DOM
	{
		DOMException::DOMException( const std::string& message )
		: exception( message )
		{}

		DOMException::~DOMException() throw()
		{}

		void DOMException::Raise() const
		{
			throw *this;
		}

		exception* DOMException::Clone() const
		{
			return new DOMException( *this );
		}
	}
	
	namespace Sax
	{
		SaxException::SaxException( const std::string& message )
		: exception( message )
		{}

		SaxException::~SaxException() throw()
		{}

		void SaxException::Raise() const
		{
			throw *this;
		}

		exception* SaxException::Clone() const
		{
			return new SaxException( *this );
		}
	}
}
