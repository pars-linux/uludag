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

namespace IPP
{
	namespace Stack
	{
		Stack::Stack( size_t meta_chunk, size_t data_chunk) 
		{
			this->stack = iks_stack_new( meta_chunk, data_chunk );
		}

		Stack::~Stack()
		{
			iks_stack_delete( this->stack );
		}

		void * Stack::allocStack( Stack *stack, size_t size )
		{
			return iks_stack_alloc( stack->stack, size);
		}

		void * Stack::strdupStack( Stack *stack, const string src, size_t len )
		{
			return iks_stack_strdup( stack->stack, src.c_str(), len );
		}
	}
}
