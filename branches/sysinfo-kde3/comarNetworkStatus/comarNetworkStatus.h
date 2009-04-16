#ifndef _COMARNETWORKSTATUS_H_
#define _COMARNETWORKSTATUS_H_

#include <kdedmodule.h>

#include <networkstatuscommon.h>
class NetworkStatusIface_stub;

class comarNetworkStatus : public KDEDModule
{
    Q_OBJECT
    K_DCOP

    public:
        comarNetworkStatus(const QCString&);
        ~comarNetworkStatus();

    private:
        NetworkStatusIface_stub * m_serviceStub;
};

#endif
