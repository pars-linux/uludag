
class QStringList;
class QRegExp;

class Device
{

public:
    Device();
    virtual ~Device();

    /**
     * Configures the interface (dev), with ip (and if provided)
     * broadcast (bc) and netmask (nm).
     */
    int setInterface( const char *dev, const char *ip,
		      const char *bc, const char *nm );

    /**
     * Adds a default route to the routing table
     */
    int setDefaultRoute( const char *ip );

    /**
     * Get IP address for device from kernel
     */
    const char *getIP( const char *dev );

    /**
     * Get Netmask for device from kernel
     */
    const char *getNetmask( const char *dev );

    /**
     * Get broadcast for device from kernel
     */
    const char *getBroadcast( const char *dev );

    /**
     * Read resolv.conf and return the nameserver list
     */
    QStringList getDnsList();

    /**
     * Write nameservers to resolv.conf
     */
    int writeDnsList( const QStringList& dnsList );

    /**
     * Start dhcpcd for device (dev)
     */
    int startDhcpcd( const char *dev );

    /**
     * Send a SIGHUP signal to the dhcpcd process
     */
    int killDhcpcd( const char *dev );

    /**
     * return the regexp object used for IP validation
     */
    const QRegExp getRx() const;

private:
    /**
     * Open a socket for us to communicate with kernel
     */
    int sockets_open();

    QRegExp *rx;
};


