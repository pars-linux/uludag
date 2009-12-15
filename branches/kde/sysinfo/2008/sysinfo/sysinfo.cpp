//////////////////////////////////////////////////////////////////////////
// sysinfo.cpp                                                          //
//                                                                      //
// Copyright (C)  2005  Lukas Tinkl <lukas.tinkl@suse.cz>               //
// Copyright (C)  2007-2008  Pardus Developers <info@pardus.org.tr>     //
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

static QString formattedUnit( unsigned long long value, int post=1 )
{
    if (value > (1024 * 1024))
        if (value > (1024 * 1024 * 1024))
            return i18n("%1 GB").arg(KGlobal::locale()->formatNumber(value / (1024 * 1024 * (post == 0 ? 1024 : 1024.0)), post));
        else
            return i18n("%1 MB").arg(KGlobal::locale()->formatNumber(value / (1024 * (post == 0 ? 1024 : 1024.0)), post));
    else
        return i18n("%1 KB").arg(KGlobal::locale()->formatNumber(value / (post == 0 ? 1024 : 1024.0), post));
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

QString kio_sysinfoProtocol::startStock( const QString title )
{
    QString templator = QString ("<table class=\"stock\">"
                                 "<tr>"
                                 "     <th colspan=3><h2>%1</h2></th>"
                                 "</tr>").arg(title);
    return templator;
}

QString kio_sysinfoProtocol::addToStock( const QString _icon, const QString text, const QString details, const QString link )
{
    QString iconpath = icon(_icon, 22, true);
    QString templator;
    QString temp = "";

    if ( link != "" )
        temp = QString(" onClick=\"location.href='%1'\" ").arg(link);

    templator += QString ("<tr class=\"info\" %1>").arg(temp);
    templator += QString ("<td><img src=\"%1\"></td><td>%2").arg(iconpath).arg(text);

    if ( details != "" )
        templator += QString("<span class=\"detail\">[ %1 ]</span>").arg(details);

    templator += "</td><td></td></tr>";
    return templator;
}

QString kio_sysinfoProtocol::addProgress( const QString _icon, const unsigned long long size )
{
    QString iconpath = icon(_icon, 22, true);
    QString progress = "file:" + locate( "data", "sysinfo/themes/2008/images/progress.png" );
    QString templator;

    templator += QString ("<tr class=\"progress\">");
    templator += QString ("<td><img src=\"%1\"></td>").arg(iconpath);
    templator += QString ("<td><img src=\"%1\" width=\"%2%\"></td><td></td></tr>").
                         arg(progress).arg(size);
    return templator;
}

QString kio_sysinfoProtocol::finishStock()
{
    return QString ("</table>");
}

static QString formatStr( QString st ) 
{
    if ( st == "" )
        return i18n("Not Available");
    return st;
}

void kio_sysinfoProtocol::get( const KURL & /*url*/ )
{
    mimeType( "application/x-sysinfo" );

    // header
    QString location = locate( "data", "sysinfo/themes/2008/index.html" );
    QFile f( location );
    f.open( IO_ReadOnly );
    QTextStream t( &f );

    infoMessage( i18n( "Looking for hardware information..." ) );

    QString content = t.read();
    content = content.arg( i18n( "My Computer" ) ); // <title>
    content = content.arg( "file:" + locate( "data", "sysinfo/themes/2008/stil.css" ) );
    content = content.arg( i18n( "Folders, Harddisks, Removable Devices, System Information and more..." ) ); // catchphrase

    QString dynamicInfo, staticInfo;
    QString dummy;

    // Dynamic Info

    // common folders
    dynamicInfo += startStock( i18n( "Common Folders" ) );
    dynamicInfo += addToStock( "folder_home", i18n( "My Home Folder" ), QDir::homeDirPath(), "file:" + QDir::homeDirPath() );
    dynamicInfo += addToStock( "folder_red", i18n( "Root Folder" ), QDir::rootDirPath(), "file:" + QDir::rootDirPath() );
    dynamicInfo += addToStock( "network", i18n( "Network Folders" ), "remote:/" , "remote:/" );
    dynamicInfo += finishStock();

    // net info
    int state = netInfo();
    if (state >= 1) { // assume no network manager / networkstatus
        dynamicInfo += startStock( i18n( "Network" ) );
        dynamicInfo += addToStock( "network", netStatus( state ));
        dynamicInfo += finishStock();
    }

    // memory info
    unsigned long int percent = memoryInfo();

    dynamicInfo += startStock( i18n( "Memory" ) );
    dynamicInfo += addToStock( "memory", i18n( "%1 free of %2" ).arg( m_info[MEM_FREERAM] ).arg( m_info[MEM_TOTALRAM] ), m_info[MEM_USAGE]);
    dynamicInfo += addProgress( "memory", percent);
    dynamicInfo += finishStock();

    content = content.arg( dynamicInfo ); // put the dynamicInfo text into the dynamic left box

    // Disk Info

    content = content.arg( i18n( "Disks" ) );
    content = content.arg(diskInfo()); // put the discInfo text into the disk right box

    // Static Info

    // Os info
    osInfo();
    staticInfo += startStock( i18n( "Operating System" ) );
    staticInfo += addToStock( "system", m_info[OS_SYSNAME] + " <b>" + m_info[OS_RELEASE] + "</b>", m_info[OS_USER] + "@" + m_info[OS_HOSTNAME] );
    staticInfo += addToStock( "system", i18n( "Kde <b>%1</b> on <b>%2</b>" ).arg(KDE::versionString()).arg( m_info[OS_SYSTEM] ));
    staticInfo += finishStock();

    // update content..
    content = content.arg( staticInfo );
    staticInfo = "";

    // CPU info
    cpuInfo();
    if ( !m_info[CPU_MODEL].isNull() )
    {
        staticInfo += startStock( i18n( "Processor" ) );
        staticInfo += addToStock( "kcmprocessor", m_info[CPU_MODEL]);
        staticInfo += addToStock( "kcmprocessor", i18n( "%1 MHz" ).arg( 
                    KGlobal::locale()->formatNumber( m_info[CPU_SPEED].toFloat(), 2 )), m_info[CPU_NOFCORE] + i18n( " core" ));
        staticInfo += finishStock();
    }

    // update content..
    content = content.arg( staticInfo );
    staticInfo = "";

    // OpenGL info
    if ( glInfo() )
    {
        staticInfo += startStock( i18n( "Display" ) );
        staticInfo += addToStock( "krdc", formatStr(m_info[GFX_MODEL]), formatStr(m_info[GFX_VENDOR]) );
        if (!m_info[GFX_DRIVER].isNull())
            staticInfo += addToStock( "x", i18n( "Driver: " ) + m_info[GFX_DRIVER] );
        staticInfo += finishStock();
    }

    // update content
    content = content.arg( staticInfo );
    staticInfo = "";

    /*
    // hw info
    if (!m_info[TYPE].isNull() || !m_info[MANUFACTURER].isNull() || !m_info[PRODUCT].isNull()
        || !m_info[BIOSVENDOR].isNull() || !m_info[ BIOSVERSION ].isNull())
    {
        staticInfo += "<h2 id=\"hwinfo\">" +i18n( "Hardware Information" ) + "</h2>";
        staticInfo += "<table style=\"background-image:url('" + icon( "laptop", 48, true) + "');\">";
        staticInfo += "<tr><td>" + i18n( "Type:" ) + "</td><td>" + m_info[ TYPE ] + "</td></tr>";
        staticInfo += "<tr><td>" + i18n( "Vendor:" ) + "</td><td>" + m_info[ MANUFACTURER ] + "</td></tr>";
        staticInfo += "<tr><td>" + i18n( "Model:" ) + "</td><td>" + m_info[ PRODUCT ] + "</td></tr>";
        staticInfo += "<tr><td>" + i18n( "Bios Vendor:" ) + "</td><td>" + m_info[ BIOSVENDOR ] + "</td></tr>";
        staticInfo += "<tr><td>" + i18n( "Bios Version:" ) + "</td><td>" + m_info[ BIOSVERSION ] + "</td></tr>";
        staticInfo += "</table>";
    }
    */

    // Send the data
    data( QCString( content.utf8() ) );
    data( QByteArray() ); // empty array means we're done sending the data
    finished();
}

void kio_sysinfoProtocol::mimetype( const KURL & /*url*/ )
{
    mimeType( "application/x-sysinfo" );
    finished();
}

unsigned long int kio_sysinfoProtocol::memoryInfo()
{
    struct sysinfo info;
    int retval = sysinfo( &info );

    if ( retval !=-1 )
    {
        const int mem_unit = info.mem_unit;
        unsigned long int usage,percent,peer;
        usage = ( info.totalram - info.freeram ) * mem_unit;
        peer = (info.totalram * mem_unit) / 100;
        peer == 0 ? percent = 0 : percent = usage / peer;

        m_info[MEM_TOTALRAM] = formattedUnit( info.totalram * mem_unit );
        m_info[MEM_FREERAM] = formattedUnit( info.freeram * mem_unit );
        m_info[MEM_USAGE] = formattedUnit( usage );
        m_info[MEM_TOTALSWAP] = formattedUnit( info.totalswap * mem_unit );
        m_info[MEM_FREESWAP] = formattedUnit( info.freeswap * mem_unit );

        return percent;
    }

    return 0;
}

void kio_sysinfoProtocol::cpuInfo()
{
    QString speed = readFromFile( "/proc/cpuinfo", "cpu MHz", ":" );

    if ( speed.isNull() )    // PPC?
        speed = readFromFile( "/proc/cpuinfo", "clock", ":" );

    if ( speed.endsWith( "MHz", false ) )
        speed = speed.left( speed.length() - 3 );

    m_info[CPU_SPEED] = speed;

    QString numberOfCores = readFromFile( "/proc/cpuinfo", "processor", ":", true);
    numberOfCores = QString::number(numberOfCores.toInt() + 1);
    m_info[CPU_NOFCORE] = numberOfCores;
    m_info[CPU_MODEL] = readFromFile( "/proc/cpuinfo", "model name", ":" );
    if ( m_info[CPU_MODEL].isNull() ) // PPC?
         m_info[CPU_MODEL] = readFromFile( "/proc/cpuinfo", "cpu", ":" );
}


QString kio_sysinfoProtocol::diskInfo()
{
    QString result;
    if ( fillMediaDevices() )
    {
        for ( QValueList<DiskInfo>::ConstIterator it = m_devices.constBegin(); it != m_devices.constEnd(); ++it )
        {
            DiskInfo di = ( *it );
            unsigned long long usage,percent,peer;
            QString label = di.userLabel.isEmpty() ? di.label : di.userLabel;
            QString mountState = di.mounted ? i18n( "Mounted on %1" ).arg(di.mountPoint) : i18n( "Not mounted" );
            QString tooltip = i18n( di.model );
            usage = di.total - di.avail;
            peer = di.total / 100;
            peer == 0 ? percent = 0 : percent = usage / peer;
            QString sizeStatus = i18n( "%1 free of %2" ).arg( formattedUnit( di.avail,0 ) ).arg( formattedUnit( di.total,0 ) );

            result +=   QString("<tr class=\"media\">"
                                "   <td>"
                                "   <a href=\"media:/%1\" title=\"%2\">"
                                "       <img src=\"%3\" width=\"48\" height=\"48\" />"
                                "   </a></td>").
                                arg( di.name ).
                                arg( tooltip+" "+di.deviceNode ).
                                arg( icon( di.iconName, 48, true) );

            result +=   QString("   <td>"
                                "       <span class=\"detail\">[ %1 ]<br><span style=\"float:right\">[ %2 ]</span></span>"
                                "       <a href=\"media:/%3\" title=\"%4\">"
                                "       %5<br><span class=\"mediaDf\">%6</span><br></a>"
                                "       <img class=\"diskusage\" src=\"file:%7\" width=\"%8%\">"
                                "   </td>"
                                "   <td></td>"
                                "</tr>").
                                arg( mountState ).
                                arg( di.fsType ).
                                arg( di.name ).
                                arg( tooltip+" "+di.deviceNode ).
                                arg( label ).
                                arg( sizeStatus ).
                                arg( locate( "data", "sysinfo/themes/2008/images/progress.png" ) ).
                                arg( percent );
        }
    }
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
#include <GL/glx.h>

bool isOpenGlSupported() {

    int scr = 0;               // print for screen 0
    Display *dpy;              // Active X display
    GLXContext ctx;            // GLX context
    XVisualInfo *visinfo;      // Visual info
    char *displayname = NULL;  // Server to connect
    Bool allowDirect = true;   // Direct rendering only
    Bool isEnabled = false;

    // GLX attributes
    int attribSingle[] = {
        GLX_RGBA,
        GLX_RED_SIZE,   1,
        GLX_GREEN_SIZE, 1,
        GLX_BLUE_SIZE,  1,
        None
    };
    int attribDouble[] = {
        GLX_RGBA,
        GLX_RED_SIZE, 1,
        GLX_GREEN_SIZE, 1,
        GLX_BLUE_SIZE, 1,
        GLX_DOUBLEBUFFER,
        None
    };

    // Open the display with screen#:scr to fiddle with
    dpy = XOpenDisplay (displayname);

    if (!dpy)
        return false;

    visinfo = glXChooseVisual(dpy, scr, attribSingle);
    if (!visinfo) 
    {
        visinfo = glXChooseVisual(dpy, scr, attribDouble);
        if (!visinfo) 
        {
            XCloseDisplay (dpy);
            return false;
        }
    }

    ctx = glXCreateContext( dpy, visinfo, NULL, allowDirect );
    if (!ctx) 
    {
       fprintf(stderr, "Error: glXCreateContext failed\n");
       XFree(visinfo);
       XCloseDisplay (dpy);
       return false;
    }

    if(glXIsDirect(dpy, ctx))
        isEnabled = true;

    glXDestroyContext (dpy,ctx);
    XFree(visinfo);
    XCloseDisplay (dpy);

    return isEnabled;
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

QString kio_sysinfoProtocol::readFromFile( const QString & filename, const QString & info, const char * sep, const bool getlast ) const
{
    QFile file( filename );

    if ( !file.exists() || !file.open( IO_ReadOnly ) )
        return QString::null;

    QTextStream stream( &file );
    QString line;
    QString temp;

    while ( !stream.atEnd() )
    {
        line = stream.readLine();
        if ( !line.isEmpty() )
        {
            if ( !sep )
                return line;
            if ( line.startsWith( info ) )
            {
                temp = line.section( sep, 1, 1 );
                if ( !getlast )
                    return temp;
            }
        }
    }
    return temp;
}

QString kio_sysinfoProtocol::icon( const QString & name, int size, bool justPath ) const
{
    QString path = KGlobal::iconLoader()->iconPath( name, -size );
    if ( justPath == true )
        return QString( "file:%1" ).arg( path );
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

        if (argc != 4) 
        {
            kdDebug(7101) << "Usage: kio_sysinfo protocol domain-socket1 domain-socket2" << endl;
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
        kdDebug(1219) << "Failed to initialize HAL!" << endl;

    DBusError error;
    dbus_error_init(&error);
    DBusConnection *dbus_connection = dbus_bus_get(DBUS_BUS_SYSTEM, &error);

    if (dbus_error_is_set(&error)) 
    {
        dbus_error_free(&error);
        libhal_ctx_free(m_halContext);
        m_halContext = 0;
    }

    if (m_halContext)
    {
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

            di.model = libhal_device_get_property_string( m_halContext, di.id.latin1( ), "block.storage_device", &error );
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
