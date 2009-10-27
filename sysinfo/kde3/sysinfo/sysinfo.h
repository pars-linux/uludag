//////////////////////////////////////////////////////////////////////////
// sysinfo.h                                                            //
//                                                                      //
// Copyright (C)  2005  Lukas Tinkl <lukas.tinkl@suse.cz>               //
//                                                                      //
// This program is free software; you can redistribute it and/or        //
// modify it under the terms of the GNU General Public License          //
// as published by the Free Software Foundation; either version 2       //
// of the License, or (at your option) any later version.               //
//                                                                      //
// This program is distributed in the hope that it will be useful,      //
// but WITHOUT ANY WARRANTY; without even the implied warranty of       //
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        //
// GNU General Public License for more details.                         //
//                                                                      //
// You should have received a copy of the GNU General Public License    //
// along with this program; if not, write to the Free Software          //
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA            //
// 02111-1307, USA.                                                     //
//////////////////////////////////////////////////////////////////////////

#ifndef _sysinfo_H_
#define _sysinfo_H_

#include <qstring.h>
#include <qcstring.h>
#include <qmap.h>
#include <qstringlist.h>

#include <kurl.h>
#include <kio/global.h>
#include <kio/slavebase.h>
#include <dcopclient.h>

class QCString;

struct DiskInfo
{
    // taken from media:/
    QString id;
    QString name;
    QString label;
    QString userLabel;
    bool mountable;
    QString deviceNode;
    QString mountPoint;
    QString fsType;
    bool mounted;
    QString baseURL;
    QString mimeType;
    QString iconName;

    // own stuff
    unsigned long long total, avail; // space on device
    QString model;              // physical device model (name)
};


/**
 * System information IO slave.
 *
 * Produces an HTML page with system information overview
 */
class kio_sysinfoProtocol : public KIO::SlaveBase
{
public:
    kio_sysinfoProtocol( const QCString &pool_socket, const QCString &app_socket );
    virtual ~kio_sysinfoProtocol();
    virtual void mimetype( const KURL& url );
    virtual void get( const KURL& url );

    /**
     * Info field
     */
    enum
    {
        MEM_TOTALRAM = 0,
        MEM_FREERAM,
        MEM_USAGE,
        MEM_TOTALSWAP,
        MEM_FREESWAP,
        CPU_MODEL,
        CPU_NOFCORE,            // number of cores
        CPU_SPEED,              // in MHz
        OS_SYSNAME,             // man 2 uname
        OS_RELEASE,
        OS_VERSION,
        OS_MACHINE,
        OS_USER,                // username
        OS_SYSTEM,              // Pardus version
        OS_HOSTNAME,
        GFX_VENDOR,              // Display stuff
        GFX_MODEL,
        GFX_DRIVER,
        SYSINFO_LAST,
        PRODUCT,
        MANUFACTURER,
        TYPE,
        BIOSVENDOR,
        BIOSVERSION
    };

private:
    /**
     * Read sysinfo from (proc) filesystem. The data is assumed to be separated by newlines, with key:value pairs
     *
     * @param filename file to read from
     * @param info requested field (if empty, return the first line from the file)
     * @param sep separator
     */
    QString readFromFile( const QString & filename, const QString & info = QString::null, const char * sep = 0, const bool getlast = false ) const;

    /**
     * Gather basic memory info
     */
    unsigned long int memoryInfo();

    /**
     * Gather CPU info
     */
    void cpuInfo();

    /**
     * @return a formatted table with disk partitions
     */
    QString diskInfo();

    /**
     * Query the online status
     * @return Unknown = 0, NoNetworks = 1, Unreachable, OfflineDisconnected,  OfflineFailed, ShuttingDown, Offline, Establishing, Online
     */
    int netInfo() const;

    /**
     * @return a verbose string containing the network status
     * @see netInfo()
     */
    QString netStatus( int code ) const;

    /**
     * Get info about kernel and OS version (uname)
     */
    void osInfo();

    /**
     * Gather basic OpenGL info
     */
    bool glInfo();

    /**
     * Helper function to locate a KDE icon
     * @return img tag with full path to the icon
     */
    QString icon( const QString & name, int size = KIcon::SizeSmall, bool justPath = false ) const;

    /**
     * For device @p name like "hdb2", @return name of the corresponding icon, e.g. hdd_mount
     */
    QString iconForDevice( const QString & name ) const;

    /**
     * Fill the list of devices (m_devices) with data from the media KIO protocol
     * @return true on success
     */
    bool fillMediaDevices();

    /**
     * Map holding the individual info attributes
     */
    QMap<int, QString> m_info;

    QString startStock( const QString title );
    QString addToStock( const QString _icon, const QString text, const QString details = "", const QString link = "" );
    QString addProgress( const QString _icon, const unsigned long long size );
    QString finishStock();

    DCOPClient * m_dcopClient;
    QValueList<DiskInfo> m_devices;
};

#endif
