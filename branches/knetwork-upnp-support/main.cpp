#include <iostream>
#include <qapplication.h>
#include <qthread.h>

#include "upnp.h"

using namespace std;

//Simple example usage....

class MainThread : public QThread
{
public:
    virtual void run();
};

void MainThread::run()
{
    /*
     * UPnP controller instance. When this goes, all the services will be destroyed.
     */
    UPnP upnp;

    /*
     * isReady() has the controller got any services
     */
    while (!upnp.isReady())
    {
        cout <<"Not ready" << endl;
        sleep(1);
    }

    /*
     * Helper function to locate a suitable NAT service to use
     */
    UPnPWANService *srv;
    while ( !(srv = upnp.getNATService()) )
    {
        cout << "Waiting" << endl;
        sleep(1);
    }

    if (srv)
    {
        /*
         * Get our IP address
         */
        QString ip;
        if (srv->getExternalIPAddress(ip))
        {
            cout << ip << endl;
        }

/*        if (srv->AddPortMapping( "", 8010,
                                 "TCP", 8010,
                                 "192.168.0.32",
                                 "test tunnel", 0 ))
        {
            cout << "New port mapping created." << endl;
        }

        if (srv->DeletePortMapping( "", 8010, "TCP"))
        {
            cout << "Port mapping deleted." << endl;
            }*/
    }

}

int main(int argc, char **argv)
{
    QApplication a( argc, argv );
    qInitNetworkProtocols();


    MainThread t;
    t.start();


    return a.exec();
}
