//////////////////////////////////////////////////////////////////////////
// sysinfo.cpp                                                          //
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

#include <config.h>

#include <qfile.h>
#include <qdir.h>
#include <qregexp.h>

#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdio.h>
#include <mntent.h>
#include <sys/vfs.h>
#include <string.h>
#include <sys/utsname.h>
#include <hal/libhal.h>

#include <kapplication.h>
#include <kcmdlineargs.h>
#include <kdebug.h>
#include <kinstance.h>
#include <kglobal.h>
#include <kstandarddirs.h>
#include <klocale.h>
#include <dcopref.h>
#include <kprocess.h>
#include <kmimetype.h>
#include <kiconloader.h>
#include <kdeversion.h>
#include <kuser.h>
#include <kglobalsettings.h>
#include <ktempfile.h>

#include "sysinfo.h"


using namespace KIO;
#define BR "<br>"

static QString formattedUnit( unsigned long long value, int post=1)
{
    if (value > (1000 * 1000))
        if (value > (1000 * 1000 * 1000))
            return i18n("%1 GB").arg(KGlobal::locale()->formatNumber(value / (1000 * 1000 * (post == 0 ? 1000 : 1000.0)), post));
        else
            return i18n("%1 MB").arg(KGlobal::locale()->formatNumber(value / (1000 * (post == 0 ? 1000 : 1000.0)), post));
    else
        return i18n("%1 KB").arg(KGlobal::locale()->formatNumber(value / (post == 0 ? 1000 : 1000.0), post));
}

kio_sysinfoProtocol::kio_sysinfoProtocol( const QCString & pool_socket, const QCString & app_socket )
    : SlaveBase( "kio_sysinfo", pool_socket, app_socket ), m_dcopClient( new DCOPClient() )
{
    if ( !m_dcopClient->isAttached() )
        m_dcopClient->attach();
}

kio_sysinfoProtocol::~kio_sysinfoProtocol()
{
    m_dcopClient->detach();
    delete m_dcopClient;
}

void kio_sysinfoProtocol::get( const KURL & /*url*/ )
{
    mimeType( "application/x-sysinfo" );

    // header
    QString location = locate( "data", "sysinfo/about/my-computer.html" );
    QFile f( location );
    f.open( IO_ReadOnly );
    QTextStream t( &f );

    infoMessage(i18n("Looking for hardware information..."));

    QString content = t.read();
    content = content.arg( i18n( "My Computer" ) ); // <title>

    content = content.arg( "file:" + locate( "data", "sysinfo/about/style.css" ) );

    content = content.arg( i18n( "My Computer" ) ); // <h1>
    content = content.arg( i18n( "Folders, Harddisks, Removable Devices, System Information and more..." ) ); // catchphrase

    QString sysInfo = "<div id=\"column\">"; // table with 2 cols
    QString dummy;

    // OS info

    // common folders
    sysInfo += "<h2 id=\"dirs\">" + i18n( "Common Folders" ) + "</h2>";
    sysInfo += "<ul>";
    // We don't have a separate Documents directory in Pardus
    //    sysInfo += QString( "<li><a href=\"file:%1\">" ).arg( KGlobalSettings::documentPath() ) + i18n( "My Documents" ) + "</a></li>";
    sysInfo += QString( "<li><a href=\"file:%1\">" ).arg( QDir::homeDirPath() ) + i18n( "My Home Folder" ) + "</a></li>";
    sysInfo += QString( "<li><a href=\"file:%1\">" ).arg( QDir::rootDirPath() ) + i18n( "Root Folder" ) + "</a></li>";
    sysInfo += "<li><a href=\"remote:/\">" + i18n( "Network Folders" ) + "</a></li>";
    sysInfo += "</ul>";

    // net info
    int state = netInfo();
    if (state > 1) { // assume no network manager / networkstatus
      sysInfo += "<h2 id=\"net\">" + i18n( "Network Status" ) + "</h2>";
      sysInfo += "<ul>";
      sysInfo += "<li>" + netStatus( state ) + "</li>";
      sysInfo += "</ul>";
    }

    // CPU info
    cpuInfo();
    if ( !m_info[CPU_MODEL].isNull() )
    {
        sysInfo += "<h2 id=\"cpu\">" + i18n( "CPU Information" ) + "</h2>";
        sysInfo += "<ul>";
        sysInfo += "<li><span class=\"label\">" + i18n( "Processor (CPU):" ) + "</span>" + m_info[CPU_MODEL] + "</li>";
        sysInfo += "<li><span class=\"label\">" + i18n( "Speed:" ) + "</span> " +
                   i18n( "%1 MHz" ).arg( KGlobal::locale()->formatNumber( m_info[CPU_SPEED].toFloat(), 2 ) ) + "</li>";
        sysInfo += "</ul>";
    }

    // memory info
    memoryInfo();
    sysInfo += "<h2 id=\"memory\">" + i18n( "Memory Information" ) + "</h2>";
    sysInfo += "<table>";
    sysInfo += "<tr><td>" + i18n( "Total memory (RAM):" ) + "</td><td>" + m_info[MEM_TOTALRAM] + "</td></tr>";
    sysInfo += "<tr><td>" + i18n( "Free memory:" ) + "</td><td>" + m_info[MEM_FREERAM] + "</td></tr>";
    dummy = i18n( "Used Memory" );
    dummy = "<tr><td>" + i18n( "Total swap:" ) + "</td><td>" + m_info[MEM_TOTALSWAP] + "</td></tr>";
    dummy = "<tr><td>" + i18n( "Free swap:" ) + "</td><td>" + m_info[MEM_FREESWAP] + "</td></tr>";
    sysInfo += "</table>";

    // hw info
    if (!m_info[TYPE].isNull() || !m_info[MANUFACTURER].isNull() || !m_info[PRODUCT].isNull() 
        || !m_info[BIOSVENDOR].isNull() || !m_info[ BIOSVERSION ].isNull())
    {
        sysInfo += "<h2 id=\"hwinfo\">" +i18n( "Hardware Information" ) + "</h2>";
        sysInfo += "<table>";
        sysInfo += "<tr><td>" + i18n( "Type:" ) + "</td><td>" + m_info[ TYPE ] + "</td></tr>";
        sysInfo += "<tr><td>" + i18n( "Vendor:" ) + "</td><td>" + m_info[ MANUFACTURER ] + "</td></tr>";
        sysInfo += "<tr><td>" + i18n( "Model:" ) + "</td><td>" + m_info[ PRODUCT ] + "</td></tr>";
        sysInfo += "<tr><td>" + i18n( "Bios Vendor:" ) + "</td><td>" + m_info[ BIOSVENDOR ] + "</td></tr>";
        sysInfo += "<tr><td>" + i18n( "Bios Version:" ) + "</td><td>" + m_info[ BIOSVERSION ] + "</td></tr>";
        sysInfo += "</table>";
    }

    sysInfo += "</div><div id=\"column2\">"; // second column

    // disk info
    sysInfo += "<h2 id=\"hdds\">" + i18n( "Disk Information" ) + "</h2>";
    sysInfo += diskInfo();

    // Os info
    osInfo();
    sysInfo += "<h2 id=\"sysinfo\">" +i18n( "OS Information" ) + "</h2>";
    sysInfo += "<table>";
    sysInfo += "<tr><td>" + i18n( "OS:" ) + "</td><td>" + m_info[OS_SYSNAME] + " " + m_info[OS_RELEASE] + " " + m_info[OS_MACHINE] + "</td></tr>";
    sysInfo += "<tr><td>" + i18n( "Current user:" ) + "</td><td>" + m_info[OS_USER] + "@" + m_info[OS_HOSTNAME] + "</td></tr>";
    sysInfo += "<tr><td>" + i18n( "System:" ) +  "</td><td>" + m_info[OS_SYSTEM] + "</td></tr>";
    sysInfo += "<tr><td>" + i18n( "KDE:" ) + "</td><td>" + KDE::versionString() + "</td></tr>";
    sysInfo += "</table>";

    // OpenGL info
    if ( glInfo() )
    {
        sysInfo += "<h2 id=\"display\">" + i18n( "Display Info" ) + "</h2>";
        sysInfo += "<table>";
        sysInfo += "<tr><td>" + i18n( "Vendor:" ) + "</td><td>" + m_info[GFX_VENDOR] +  "</td></tr>";
        sysInfo += "<tr><td>" + i18n( "Model:" ) + "</td><td>" + m_info[GFX_MODEL] + "</td></tr>";
        if (!m_info[GFX_DRIVER].isNull())
            sysInfo += "<tr><td>" + i18n( "Driver:" ) + "</td><td>" + m_info[GFX_DRIVER] + "</td></tr>";
        sysInfo += "</table>";
    }

    sysInfo += "</div>";

    // Send the data
    content = content.arg( sysInfo ); // put the sysinfo text into the main box
    data( QCString( content.utf8() ) );
    data( QByteArray() ); // empty array means we're done sending the data
    finished();
}

void kio_sysinfoProtocol::mimetype( const KURL & /*url*/ )
{
    mimeType( "application/x-sysinfo" );
    finished();
}

static unsigned long int scan_one( const char* buff, const char *key )
{
    char *b = strstr( buff, key );
    if ( !b )
        return 0;
    unsigned long int val = 0;
    if ( sscanf( b + strlen( key ), ": %lu", &val ) != 1 )
        return 0;
    kdDebug() << "scan_one " << key << " " << val << endl;
    return val;
}

static unsigned long int calculateFreeRam()
{
    FILE *fd = fopen( "/proc/meminfo", "rt" );
    if ( !fd )
        return 0;

    QTextIStream is( fd );
    QString MemInfoBuf = is.read();

    unsigned long int MemFree = scan_one( MemInfoBuf.latin1(), "MemFree" );
    unsigned long int Buffers = scan_one( MemInfoBuf.latin1(), "Buffers" );
    unsigned long int Cached  = scan_one( MemInfoBuf.latin1(), "Cached" );
    unsigned long int Slab    = scan_one( MemInfoBuf.latin1(), "Slab" );
    fclose( fd );

    MemFree += Cached + Buffers + Slab;
    if ( MemFree > 50 * 1024 )
        MemFree -= 50 * 1024;
    return MemFree;
}

void kio_sysinfoProtocol::memoryInfo()
{
    struct sysinfo info;
    int retval = sysinfo( &info );

    if ( retval !=-1 )
    {
        const int mem_unit = info.mem_unit;

        m_info[MEM_TOTALRAM] = formattedUnit( info.totalram * mem_unit ,0);
        unsigned long int totalFree = calculateFreeRam() * 1024;
        kdDebug() << "total " << totalFree << " free " << info.freeram << " unit " << mem_unit << endl;
        if ( totalFree > info.freeram * info.mem_unit || true )
            m_info[MEM_FREERAM] = i18n("%1 (+ %2 Caches)").arg(formattedUnit( info.freeram * mem_unit ))
                                  .arg( formattedUnit( totalFree - info.freeram * mem_unit ,0));
        else
            m_info[MEM_FREERAM] = formattedUnit( info.freeram * mem_unit );

        m_info[MEM_TOTALSWAP] = formattedUnit( info.totalswap * mem_unit ,0);
        m_info[MEM_FREESWAP] = formattedUnit( info.freeswap * mem_unit ,0);

        m_info[SYSTEM_UPTIME] = convertSeconds( info.uptime );
    }
}

void kio_sysinfoProtocol::cpuInfo()
{
    QString speed = readFromFile( "/proc/cpuinfo", "cpu MHz", ":" );

    if ( speed.isNull() )    // PPC?
        speed = readFromFile( "/proc/cpuinfo", "clock", ":" );

    if ( speed.endsWith( "MHz", false ) )
        speed = speed.left( speed.length() - 3 );

    m_info[CPU_SPEED] = speed;

    m_info[CPU_MODEL] = readFromFile( "/proc/cpuinfo", "model name", ":" );
    if ( m_info[CPU_MODEL].isNull() ) // PPC?
         m_info[CPU_MODEL] = readFromFile( "/proc/cpuinfo", "cpu", ":" );
}


QString kio_sysinfoProtocol::diskInfo()
{
    QString result = "<table>";
    if ( fillMediaDevices() )
    {
        for ( QValueList<DiskInfo>::ConstIterator it = m_devices.constBegin(); it != m_devices.constEnd(); ++it )
        {
            DiskInfo di = ( *it );
            QString tooltip = i18n( di.model );
            QString label = di.userLabel.isEmpty() ? di.label : di.userLabel;

            unsigned long long usage,percent,peer;
            usage = di.total - di.avail;
            peer = di.total / 100;

            peer == 0 ? percent = 0 : percent = usage / peer;

            result += QString( "<tr>"
                               "    <td>%1</td>"
                               "    <td width=\"100%\">"
                               "        <table width=\"100%\">"
                               "            <tr>"
                               "                <td>"
                               "                    <a href=\"media:/%2\" title=\"%3\">%4</a> [%5]"
                               "                    " + i18n("Total") + ": <b>%6</b> " + i18n("Available") + ": <b>%7</b>"
                               "                </td>"
                               "            </tr>"
                               "            <tr height=\"10px\">"
                               "                <td class=\"bar\">"
                               "                    <div style=\"width: %8%\">%9&nbsp</div>"
                               "                </td>"
                               "            </tr>"
                               "        </table>"
                               "    </td>"
                               "</tr>"
                               "<tr></tr>" ).
                                arg( icon( di.iconName, 48 ) ).
                                arg( di.name ).
                                arg( tooltip+" "+di.deviceNode ).
                                arg( label ).
                                arg( di.fsType ).
                                arg( formattedUnit( di.total,0 ) ).
                                arg( formattedUnit( di.avail,0 ) ).
                                arg( di.mounted ? percent : 0).
                                arg( di.mounted ? formattedUnit( usage ) : QString::null );
        }
    }
    result += "</table>";
    return result;
}


int kio_sysinfoProtocol::netInfo() const
{
    // query kded.networkstatus.status(QString host)
    DCOPRef nsd( "kded", "networkstatus" );
    nsd.setDCOPClient( m_dcopClient );
    DCOPReply reply = nsd.call( "status" );

    if ( reply.isValid() )
        return reply;

    kdDebug() << k_funcinfo << "Reply is invalid" << endl;

    return 0;
}

#define INFO_XORG "/etc/X11/xorg.conf"
#define INFO_OPENGL "/usr/bin/glxinfo"

bool isOpenGlSupported() {

    FILE *pipe;
    QString line;

    if ((pipe = popen(INFO_OPENGL, "r")) == NULL) {
        pclose(pipe);
        return false;
    }

    QTextStream t(pipe, IO_ReadOnly);
    while (!t.atEnd()) {
        line = t.readLine();
        line = line.stripWhiteSpace();
        if (line.startsWith("direct rendering: "))
            if (line.replace("direct rendering: ","") == "Yes")
                return true;
            else
                return false;
    }
    return false;
}

bool kio_sysinfoProtocol::glInfo()
{
    QFile file;
    QString line;
    int inFold=0;
    bool openGlSupported = isOpenGlSupported();

    file.setName(INFO_XORG);
    if (!file.exists() || !file.open(IO_ReadOnly))
        return false;

    QTextStream stream(&file);
    while (!stream.atEnd()) {
        line = stream.readLine();
        line = line.stripWhiteSpace();
        if (line.startsWith("Section \"Device\"")) inFold = 1;
        if (line.startsWith("EndSection")) inFold = 0;
        if (inFold==1){
            if (line.startsWith("VendorName"))
                m_info[GFX_VENDOR] = line.replace("VendorName ","").replace("\"","");
            if (line.startsWith("BoardName"))
                m_info[GFX_MODEL] = line.replace("BoardName ","").replace("\"","");
            if (line.startsWith("Driver")){
                QString driver = line.replace("Driver ","").replace("\"","");
                if (openGlSupported)
                    m_info[GFX_DRIVER] = i18n("%1 (3D Support)").arg(driver);
                else
                    m_info[GFX_DRIVER] = i18n("%1 (No 3D Support)").arg(driver);
            }
        }
    }
    return true;
}

QString kio_sysinfoProtocol::netStatus( int code ) const
{
    if ( code == 1 || code == 2 )
        return i18n( "Network is <strong>unreachable</strong>" );
    else if ( code == 3 || code == 4 || code == 6 )
        return i18n( "You are <strong>offline</strong>" );
    else if ( code == 5 )
        return i18n( "Network is <strong>shutting down</strong>" );
    else if ( code == 7 )
        return i18n( "<strong>Establishing</strong> connection to the network" );
    else if ( code == 8 )
        return i18n( "You are <strong>online</strong>" );

    return i18n( "Unknown network status" );
}

QString kio_sysinfoProtocol::readFromFile( const QString & filename, const QString & info, const char * sep ) const
{
    QFile file( filename );

    if ( !file.exists() || !file.open( IO_ReadOnly ) )
        return QString::null;

    QTextStream stream( &file );
    QString line;

    while ( !stream.atEnd() )
    {
        line = stream.readLine();
        if ( !line.isEmpty() )
        {
            if ( !sep )
                return line;
            if ( line.startsWith( info ) )
            {
                return line.section( sep, 1, 1 );
            }
        }
    }

    return QString::null;
}

QString kio_sysinfoProtocol::icon( const QString & name, int size ) const
{
    QString path = KGlobal::iconLoader()->iconPath( name, -size );
    return QString( "<img src=\"file:%1\" width=\"%2\" height=\"%3\" valign=\"center\"/>" ).arg( path ).arg( size ).arg( size );
}

QString kio_sysinfoProtocol::iconForDevice( const QString & name ) const
{
    DCOPRef nsd( "kded", "mediamanager" );
    nsd.setDCOPClient( m_dcopClient );
    QStringList result = nsd.call( "properties", name );

    if ( result.isEmpty() )
        return QString::null;

    KMimeType::Ptr mime = KMimeType::mimeType( result[10] );
    return mime->icon( QString::null, false );
}

void kio_sysinfoProtocol::osInfo()
{
    struct utsname uts;
    uname( &uts );
    m_info[ OS_SYSNAME ] = uts.sysname;
    m_info[ OS_RELEASE ] = uts.release;
    m_info[ OS_VERSION ] = uts.version;
    m_info[ OS_MACHINE ] = uts.machine;
    m_info[ OS_HOSTNAME ] = uts.nodename;

    m_info[ OS_USER ] = KUser().loginName();

    m_info[ OS_SYSTEM ] = readFromFile( "/etc/pardus-release" );
}

static const KCmdLineOptions options[] =
{
        { "+protocol", "Protocol name", 0 },
        { "+pool", "Socket name", 0 },
        { "+app", "Socket name",  0 },
        KCmdLineLastOption
};

extern "C"
{
    int kdemain(int argc, char **argv)
    {
      // we need KApp to check the display capabilities
      putenv(strdup("SESSION_MANAGER="));
      KCmdLineArgs::init(argc, argv, "kio_sysinfo", 0, 0, 0, 0);
      KCmdLineArgs::addCmdLineOptions( options );
      KApplication app( false, true );

        kdDebug(7101) << "*** Starting kio_sysinfo " << endl;

        if (argc != 4) {
            kdDebug(7101) << "Usage: kio_sysinfo  protocol domain-socket1 domain-socket2" << endl;
            exit(-1);
        }

	KCmdLineArgs *args = KCmdLineArgs::parsedArgs();

        kio_sysinfoProtocol slave( args->arg(1), args->arg(2));
        slave.dispatchLoop();

        kdDebug(7101) << "*** kio_sysinfo Done" << endl;
        return 0;
    }
}

bool kio_sysinfoProtocol::fillMediaDevices()
{
    DCOPRef nsd( "kded", "mediamanager" );
    nsd.setDCOPClient( m_dcopClient );
    QStringList devices = nsd.call( "fullList" );
    if ( devices.isEmpty() )
        return false;

    kdDebug() << devices << endl;

    m_devices.clear();

    LibHalContext  *m_halContext = libhal_ctx_new();
    if (!m_halContext)
      {
	kdDebug(1219) << "Failed to initialize HAL!" << endl;
      }

    DBusError error;
    dbus_error_init(&error);
    DBusConnection *dbus_connection = dbus_bus_get(DBUS_BUS_SYSTEM, &error);

    if (dbus_error_is_set(&error)) {
      dbus_error_free(&error);
      libhal_ctx_free(m_halContext);
      m_halContext = 0;
    }

    if (m_halContext) {
      libhal_ctx_set_dbus_connection(m_halContext, dbus_connection);
      dbus_error_init(&error);
      if (!libhal_ctx_init(m_halContext, &error))
	{
	  printf("error %s %s\n", error.name, error.message);
	  if (dbus_error_is_set(&error))
	    dbus_error_free(&error);
	  libhal_ctx_free(m_halContext);
	  m_halContext = 0;
	}
    }

    for ( QStringList::ConstIterator it = devices.constBegin(); it != devices.constEnd(); ++it )
    {
        DiskInfo di;

        di.id = ( *it );
        di.name = *++it;
        di.label = *++it;
        di.userLabel = ( *++it );
        di.mountable = ( *++it == "true" ); // bool
        di.deviceNode = ( *++it );
        di.mountPoint = ( *++it );
        di.fsType = ( *++it );
        di.mounted = ( *++it == "true" ); // bool
        di.baseURL = ( *++it );
        di.mimeType = ( *++it );
        di.iconName = ( *++it );

        if ( di.iconName.isEmpty() ) // no user icon, query the MIME type
        {
            KMimeType::Ptr mime = KMimeType::mimeType( di.mimeType );
            di.iconName = mime->icon( QString::null, false );
        }

        di.total = di.avail = 0;

        // calc the free/total space
        struct statfs sfs;
        if ( di.mounted && statfs( QFile::encodeName( di.mountPoint ), &sfs ) == 0 )
        {
            di.total = ( unsigned long long ) sfs.f_blocks * sfs.f_bsize;
            di.avail = ( unsigned long long )( getuid() ? sfs.f_bavail : sfs.f_bfree ) * sfs.f_bsize;
        } else if (m_halContext && di.id.startsWith("/org/freedesktop/Hal/" ) )
        {
            dbus_error_init(&error);
            di.total = libhal_device_get_property_uint64(m_halContext, di.id.latin1(), "volume.size", &error);
            if (dbus_error_is_set(&error))
                di.total = 0;
            }

            di.model = libhal_device_get_property_string(  m_halContext, di.id.latin1(  ), "block.storage_device", &error );
            di.model = libhal_device_get_property_string( m_halContext, di.model.latin1( ), "storage.model", &error );

            ++it; // skip separator

            m_devices.append( di );
    }

    m_info[PRODUCT ] = libhal_device_get_property_string(  m_halContext, "/org/freedesktop/Hal/devices/computer", "smbios.system.product", &error );
    m_info[MANUFACTURER ] = libhal_device_get_property_string(  m_halContext, "/org/freedesktop/Hal/devices/computer", "smbios.system.manufacturer", &error );
    m_info[TYPE] = libhal_device_get_property_string( m_halContext, "/org/freedesktop/Hal/devices/computer", "smbios.chassis.type", &error );
    m_info[BIOSVENDOR] = libhal_device_get_property_string( m_halContext, "/org/freedesktop/Hal/devices/computer", "smbios.bios.vendor", &error );
    m_info[BIOSVERSION] = libhal_device_get_property_string( m_halContext, "/org/freedesktop/Hal/devices/computer", "smbios.bios.version", &error );

    libhal_ctx_free(m_halContext);

    return true;
}
