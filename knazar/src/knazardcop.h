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
};

#endif
