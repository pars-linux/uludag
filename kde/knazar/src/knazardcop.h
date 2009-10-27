/***************************************************************************
 *   Copyright (C) 2005, 2007 by TUBITAK/UEKAE                                   *
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

#ifndef _KNAZARDCOP_H_
#define _KNAZARDCOP_H_

#include <dcopobject.h>

class DCOPNazarIface : virtual public DCOPObject
{
    K_DCOP
k_dcop:
    virtual void protect_from_harmfull_looks() = 0;
    virtual void release_the_protection() = 0;
    virtual void send_nazar() = 0;
    virtual bool is_protecting() = 0;
};

#endif
