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

#ifndef EXCEPTION_H
#define EXCEPTION_H

#include <exception>
#include <string>

namespace IPP
{
	using std::string;

	class exception: public std::exception
	{
		public:
			explicit exception( const string &message );
			virtual ~exception() throw();

			virtual const char* what() const throw();
			virtual void Raise() const;
			virtual exception* Clone() const;
		private:
			string message;
	};

	namespace DOM
	{
		class DOMException: public exception
		{
			public:
				explicit DOMException( const std::string &message );
				virtual ~DOMException() throw();

				virtual void Raise() const;
				virtual exception* Clone() const;
		};
	};
	
	namespace Sax
	{
		class SaxException: public exception
		{
			public:
				explicit SaxException( const std::string &message );
				virtual ~SaxException() throw();

				virtual void Raise() const;
				virtual exception* Clone() const;
		};
	};
};

#endif
