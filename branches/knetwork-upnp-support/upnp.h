// Original work belongs to Ivor Hewitt

#include <qobject.h>
#include <qnetwork.h>
#include <qhttp.h>
#include <qdom.h>
#include <qurl.h>

class UPnP;
class Device;
class Service;

class ServiceFactory
{
public:
    static Service *create(const Device* dev, const QDomElement& el);
};

class Device : public QObject
{
Q_OBJECT

public:
    Device( const UPnP *upnp, const QUrl &url );
    virtual ~Device();

    QPtrList<Service> m_services;

    bool command( const QString &service, const QString &command, const QString &url_path, const QString &content, QString &response ) const;

private slots:
    void requestFinished( int, bool );

private:
    const UPnP *m_upnp;

    QUrl m_url;
    unsigned int m_port;

    QHttp http;
};

class Service
{
public:
    Service( const Device *dev, const QString &name, const QString &type, const QString &url ) : m_dev(dev),m_serviceName(name), m_serviceType(type), m_controlURL(url) {}
    virtual ~Service();

    const QString& serviceName() { return m_serviceName;}
    const QString& controlURL() { return m_controlURL;}

    const Device* m_dev;;

protected:
    QString m_serviceName;
    QString m_serviceType;
    QString m_controlURL;

 private:
    friend class ServiceFactory;
};

class UPnPWANService : public Service
{
public:
    UPnPWANService( const Device *dev, const QString &name, const QString &type, const QString &url ) : Service(dev, name, type, url) {}
    ~UPnPWANService();

    bool getExternalIPAddress( QString &ip );

    bool addPortMapping( const QString& remotehost, unsigned int external_port,
                         const QString& protocol, unsigned int internal_port,
                         const QString& localclient,
                         const QString& comment, int duration );

    bool deletePortMapping( const QString& remotehost, int external_port, const QString &protocol );

    bool getStatusInfo( QString &status ) {status="Connected"; return true;}
    bool getNATStatus( QString &status ) {status="Enabled"; return true;}

private:
};

class UPnP
{
public:
    UPnP();
    ~UPnP();

    bool isReady() { return m_ready;}
    UPnPWANService* getNATService();
    void findDevices();

private:
    QPtrList<Device> m_devices;

    bool m_ready;
};
