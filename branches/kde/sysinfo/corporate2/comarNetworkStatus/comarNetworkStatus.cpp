#include "comarNetworkStatus.h"

#include <kapp.h>
#include <dcopclient.h>

#include "networkstatusiface_stub.h"

#define KDED_NETWORK_NAME "COMARNetworkStatus"

extern "C"
KDE_EXPORT KDEDModule *create_comarnetworkstatus( const QCString& obj )
{
    return new comarNetworkStatus::comarNetworkStatus( obj );
}

comarNetworkStatus::comarNetworkStatus( const QCString &obj ): KDEDModule( obj ), m_serviceStub( 0 )
{
    m_serviceStub = new NetworkStatusIface_stub( "kded", "networkstatus" );
    NetworkStatus::Properties nsp;
    nsp.name = KDED_NETWORK_NAME;
    nsp.service = kapp->dcopClient()->appId();
    nsp.status = NetworkStatus::NoNetworks;
    m_serviceStub->registerNetwork( nsp );
}

comarNetworkStatus::~comarNetworkStatus()
{
    m_serviceStub->unregisterNetwork( KDED_NETWORK_NAME );
    delete m_serviceStub;
}
