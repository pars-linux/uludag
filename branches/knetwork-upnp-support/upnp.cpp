//
// Trivial UPnP controller
// 

#include <qsocketdevice.h>
#include <qurl.h>
#include <qdom.h>

#include <iostream>

#include "upnp.h"


#define REQUEST_TIMEOUT 5

using namespace std;


Service *ServiceFactory::Create( const Device* dev, const QDomElement &el )
{
    QString serviceType;
    QString serviceName;
    QString controlURL;

    for( QDomNode n = el.firstChild(); !n.isNull(); n = n.nextSibling() )
    {
        if ( n.isElement() ) {
            QDomElement e = n.toElement();
            if (e.tagName()=="serviceType")
            {
                serviceType = e.text();

                QString s = e.text().section(':',3,3);
                serviceName = s.stripWhiteSpace();
            }
            else if (e.tagName() == "controlURL")
                controlURL = e.text();
        }
    }

cout << serviceName << ":" << controlURL << endl;

    if (serviceName == "WANIPConnection" ||
        serviceName == "WANPPPConnection" )
    {
cout << "Found wan service" << endl;

        UPnPWANService* srv = new UPnPWANService( dev, serviceName, serviceType, controlURL  );
        return (Service*)srv;
    }
    return 0;
}

/*
 *
 *
 */
Device::Device( const UPnP *upnp, const QUrl &url ) : QObject(), m_upnp(upnp), m_url(url)
{
    connect( &http, SIGNAL( requestFinished( int, bool ) ),
             this, SLOT( requestFinished( int, bool )) );

cout << "Requesting device info from:" << m_url.host() << m_url.path() << endl;

    http.setHost(m_url.host(), m_url.port());
    http.get(m_url.path());
}

Device::~Device()
{
}

/*
QDomNode GetNode( QDomNode node, const QString& path )
{
    QStringList l = QStringList.split(".",path);

    for ( QStringList::Iterator it = fonts.begin(); it != fonts.end(); ++it ) {
        cout << *it << ":";
    }
}
*/

void Device::requestFinished ( int id, bool error )
{
cout << "requestFinished." << endl;

    int size = http.bytesAvailable();
    if (size)
    {
        char buffer[size];
        int len = http.readBlock(buffer,size);
        buffer[len] = 0;

//cout << "Content: " << buffer << endl;

        QDomDocument doc;
        doc.setContent(QString(buffer));

/*      QDomNode dev = GetNode(doc, "root.device");
        m_name = GetElement(dev, "friendlyname").text();
        m_manuf = GetElement(dev, "manufacturer").text();*/

        //Flatten the services and store them.
        QDomNodeList nl = doc.elementsByTagName("service");
        for (unsigned int i=0; i< nl.count(); ++i)
        {
            QDomNode n = nl.item(i);
            QDomElement e = n.toElement();

            Service *srv = ServiceFactory::Create(this, e);
            if (srv)
            {
                m_services.append(srv);
            }
        }
    }
}

/*
 * blocking http request.
 */
bool Device::Command( const QString &service, const QString &command, const QString &url_path, const QString &content, QString &response ) const
{
    QHttp cmd_http;
    cmd_http.setHost(m_url.host(), m_url.port());

    QHttpRequestHeader head("POST", url_path);
    head.setValue("CONTENT-TYPE", "text/xml ; charset=\"utf-8\"");
    head.setValue("HOST",QString("%1:%2").arg(m_url.host()).arg(m_url.port()));
    head.setValue("SOAPACTION", QString("\"%1#%2\"").arg(service).arg(command) );
    head.setValue("Content-Length", QString("%1").arg(content.length()));

    QByteArray qb(content.length());
    memcpy(qb.data(), content.ascii(), content.length());

    cout << "Service: '" << service << "'Command: '" << command << "' url: '" << url_path << "' host " << m_url.host() << endl;

    cmd_http.request( head, qb );

    for (int i=0; i < REQUEST_TIMEOUT; i++)
    {
        cout << "command wait" << endl;

        if (cmd_http.bytesAvailable())
            break;
        sleep(1);
    }

    {
        int size;
        size = cmd_http.bytesAvailable();

        char buffer[size];
        int len = cmd_http.readBlock(buffer,size);
        buffer[len] = 0;

        response = buffer;

        return true;
    }
    return false;
}

/*
 *
 *
 */
Service::~Service()
{}

UPnPWANService::~UPnPWANService()
{}

bool UPnPWANService::GetExternalIPAddress( QString &ip )
{
    bool ret=false;
cout << "GetExternal" << endl;

/*request*/
    QDomDocument doc;
    QDomElement e = doc.createElementNS("http://schemas.xmlsoap.org/soap/envelope/","s:Envelope");
    doc.appendChild(e);
    QDomElement b = doc.createElement("s:Body");
    e.appendChild(b);
    QDomElement a = doc.createElementNS(m_serviceType, "u:GetExternalIPAddress");
    b.appendChild(a);
    QString request(doc.toString());

    QString response;
    ret = m_dev->Command( m_serviceType, "GetExternalIPAddress", m_controlURL, request, response );

    cout << "Ret: " << ret << "Resp: " << response << endl;
/*response*/
    QDomDocument rdoc;
    rdoc.setContent(response);
    {
        QDomNodeList nl = rdoc.elementsByTagName("NewExternalIPAddress");

        QDomElement e = nl.item(0).toElement();
        ip = e.text();
    }
    return ret;
}

bool UPnPWANService::AddPortMapping( const QString& remotehost, unsigned int external_port,
                     const QString& protocol, unsigned int internal_port,
                     const QString& localclient,
                     const QString& comment, int duration )
{
    bool ret=false;

    QDomDocument doc;

    QDomElement e = doc.createElement("Envelope");
    doc.appendChild(e);
    QDomElement b = doc.createElement("Body");
    e.appendChild(b);
    QDomElement a = doc.createElement("AddPortMapping");
    b.appendChild(a);

    QDomElement node_remotehost   = doc.createElement("NewRemoteHost");
    node_remotehost.appendChild(doc.createTextNode(remotehost));
    a.appendChild(node_remotehost);

    QDomElement node_externalport = doc.createElement("NewExternalPort");
    node_externalport.appendChild(doc.createTextNode(QString("%1").arg(external_port)));
    a.appendChild(node_externalport);

    QDomElement node_protocol     = doc.createElement("NewProtocol");
    node_protocol.appendChild(doc.createTextNode(protocol));
    a.appendChild(node_protocol);

    QDomElement node_internalport = doc.createElement("NewInternalPort");
    node_internalport.appendChild(doc.createTextNode(QString("%1").arg(internal_port)));
    a.appendChild(node_internalport);

    QDomElement node_internalclient = doc.createElement("NewInternalClient");
    node_internalclient.appendChild(doc.createTextNode(localclient));
    a.appendChild(node_internalclient);

    QDomElement node_enabled      = doc.createElement("NewEnabled");
    node_enabled.appendChild(doc.createTextNode("1"));
    a.appendChild(node_enabled);

    QDomElement node_description  = doc.createElement("NewPortMappingDescription");
    node_description.appendChild(doc.createTextNode(comment));
    a.appendChild(node_description);

    QDomElement node_duration     = doc.createElement("NewLeaseDuration");
    node_duration.appendChild(doc.createTextNode(QString("%1").arg(duration)));
    a.appendChild(node_duration);

    QString request(doc.toString());

    QString response;
    ret = m_dev->Command(m_serviceType, "AddPortMapping", m_controlURL, request, response);

cout << response << endl;

    return ret;
}

bool UPnPWANService::DeletePortMapping( const QString& remotehost, int external_port, const QString &protocol )
{
    bool ret=false;

    QDomDocument doc;

    QDomElement e = doc.createElement("Envelope");
    doc.appendChild(e);
    QDomElement b = doc.createElement("Body");
    e.appendChild(b);
    QDomElement a = doc.createElement("DeletePortMapping");
    b.appendChild(a);

    QDomElement node_remotehost   = doc.createElement("NewRemoteHost");
    node_remotehost.appendChild(doc.createTextNode(remotehost));
    a.appendChild(node_remotehost);

    QDomElement node_externalport = doc.createElement("NewExternalPort");
    node_externalport.appendChild(doc.createTextNode(QString("%1").arg(external_port)));
    a.appendChild(node_externalport);

    QDomElement node_protocol     = doc.createElement("NewProtocol");
    node_protocol.appendChild(doc.createTextNode(protocol));
    a.appendChild(node_protocol);

    QString request(doc.toString());

    QString response;
    ret = m_dev->Command(m_serviceType, "DeletePortMapping", m_controlURL, request, response);

cout << response << endl;

    return ret;
}


/*
 * Helper function to locate and cache an available NAT
 * service.
 */
UPnPWANService* UPnP::getNATService()
{
    cout << "getNATService" << endl;
    static UPnPWANService *theService;

    if (theService)
        return theService;

    if (isReady())
    {
        Device *dev;
        for ( dev = m_devices.first(); dev; dev = m_devices.next() )
        {
            Service *srv;
            for (srv=dev->m_services.first(); srv; srv=dev->m_services.next())
            {
                /*
                 * Is this a router?
                 */
                cout << "getNATService" << srv->serviceName() << endl;

                if (srv->serviceName() != "WANIPConnection" &&
                    srv->serviceName() != "WANPPPConnection")
                {
                    cout << "no type match" << endl;
                    continue;
                }

                UPnPWANService *wsrv = (UPnPWANService *)srv;

                QString ret;
                /* is it connected */
                if (!wsrv->GetStatusInfo(ret) || ret != "Connected")
                {
                    cout << "not connected" << endl;
                    continue;
                }
                /* is NAT enabled */
                if (!wsrv->GetNATStatus(ret) || ret != "Enabled")
                {
                    cout << "not enabled" << endl;
                    continue;
                }
                /* does it have an ip address */
                if (!wsrv->GetExternalIPAddress(ret) || ret=="")
                {
                    cout << "no ip" << endl;
                    continue;
                }

                /* if its got all that then use it */
                theService=wsrv;
                return wsrv;
            }
        }
    }
    return 0;
}


/* helper to parse the raw response header */
class Header : public QHttpHeader
{
public:
    Header(const QString & string) : QHttpHeader(string){};
    int majorVersion() const { return 1;}
    int minorVersion() const { return 1;}
};

/*
 *
 */
UPnP::UPnP() : m_ready(false)
{
    findDevices();
}

UPnP::~UPnP()
{
}

void UPnP::findDevices()
{
//TODO Change to keep open and listen to notifications.
    QSocketDevice qs(QSocketDevice::Datagram);
    qs.setBlocking(false);

// Use udp broadcast to find devices.
// give devices 5 seconds to respond
    QString req("M-SEARCH * HTTP/1.1\r\nMX: 5\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nST: upnp:rootdevice\r\n\r\n");
    qs.writeBlock(req.ascii(), req.length(), QHostAddress(0xeffffffa), 1900 );

    char buffer[2048];
    for (int delay=0; delay<5; delay++)
    {
        if (qs.waitForMore(1000))
        {
            long len = qs.readBlock(buffer, 2048);
            if (len>0)
            {
                buffer[len]=0;

                QString resp(buffer);
                int pos = resp.find("200 OK");

                Header head(resp.mid(pos+8));

                QString loc = head.value("LOCATION");
cout << loc << endl;

                QUrl url(loc);
cout << "Notification url: " << url.host() << " port " << url.port() << " path " << url.path() << endl;

                if (url.isValid())
                {
                    Device *dev = new Device( this, url );
                    m_devices.append(dev);
// move to more suitable location.
                    m_ready=true;
                }
            }
        }
    }
}





