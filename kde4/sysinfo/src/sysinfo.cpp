//////////////////////////////////////////////////////////////////////////
// sysinfo.cpp                                                          //
//                                                                      //
// Copyright (C)  2005, 2008  Lukas Tinkl <lukas.tinkl@suse.cz>         //
//                                        <ltinkl@redhat.com>           //
//           (C)  2008  Dirk Mueller <dmueller@suse.de>                 //
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
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA        //
// 02110-1301, USA.                                                     //
//////////////////////////////////////////////////////////////////////////

#include "sysinfo.h"

#ifdef HAVE_HD_H
#include <hd.h>
#endif

#include <QFile>
#include <QDir>
#include <QTextStream>
#include <QtGui/QX11Info>
#include <QDesktopWidget>

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
#include <kdebug.h>
#include <kglobal.h>
#include <kstandarddirs.h>
#include <klocale.h>
#include <kmimetype.h>
#include <kiconloader.h>
#include <kdeversion.h>
#include <kuser.h>
#include <kglobalsettings.h>
#include <kmountpoint.h>

#include <solid/networking.h>
#include <solid/device.h>
#include <solid/storageaccess.h>
#include <solid/storagevolume.h>
#include <solid/block.h>

#define SOLID_MEDIALIST_PREDICATE \
    "[[ StorageVolume.usage == 'FileSystem' OR StorageVolume.usage == 'Encrypted' ]" \
    " OR " \
    "[ IS StorageAccess AND StorageDrive.driveType == 'Floppy' ]]"

#define BR "<br>"

static QString formattedUnit( quint64 value, int post=1 )
{
    if (value >= (1024 * 1024))
        if (value >= (1024 * 1024 * 1024))
            return i18n("%1 GB", KGlobal::locale()->formatNumber(value / (1024 * 1024 * 1024.0),
                        post));
        else
            return i18n("%1 MB", KGlobal::locale()->formatNumber(value / (1024 * 1024.0), post));
    else
        return i18n("%1 KB", KGlobal::locale()->formatNumber(value / 1024.0, post));
}

static QString htmlQuote(const QString& _s)
{
    QString s(_s);
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
}

static QString readFromFile( const QString & filename, const QString & info = QString(),
                             const char * sep = 0, bool returnlast = false )
{
    //kDebug(1242) << "Reading " << info << " from " << filename;

    QFile file( filename );

    if ( !file.exists() || !file.open( QIODevice::ReadOnly ) )
        return QString::null;

    QTextStream stream( &file );
    QString line, result;

    do
    {
        line = stream.readLine();
        if ( !line.isEmpty() )
        {
            if ( !sep )
                result = line;
            else if ( line.startsWith( info ) )
                result = line.section( sep, 1, 1 );

            if (!result.isEmpty() && !returnlast)
                return result;
        }
    } while (!line.isNull());

    return result;
}

static QString netStatus()
{
    switch (Solid::Networking::status())
    {
    case Solid::Networking::Disconnecting:
        return i18n( "Network is <strong>shutting down</strong>" );
    case Solid::Networking::Connecting:
        return i18n( "<strong>Establishing</strong> connection to the network" );
    case Solid::Networking::Connected:
        return i18n( "You are <strong>online</strong>" );
    case Solid::Networking::Unconnected:
        return i18n( "You are <strong>offline</strong>" );
    case Solid::Networking::Unknown:
    default:
        return i18n( "Unknown network status" );
    }
}

kio_sysinfoProtocol::kio_sysinfoProtocol( const QByteArray & pool_socket, const QByteArray & app_socket )
    : SlaveBase( "kio_sysinfo", pool_socket, app_socket )
{
    m_predicate = Solid::Predicate::fromString(SOLID_MEDIALIST_PREDICATE);
}

kio_sysinfoProtocol::~kio_sysinfoProtocol()
{
}

void kio_sysinfoProtocol::get( const KUrl & /*url*/ )
{
 //   mimeType( "application/x-sysinfo" );
    mimeType( "text/html" );

    // CPU info
    infoMessage( i18n( "Looking for CPU information..." ) );
    cpuInfo();

    // header
    QString location = KStandardDirs::locate( "data", "sysinfo/about/my-computer.html" );
    QFile f( location );
    f.open( QIODevice::ReadOnly );
    QTextStream t( &f );
    QString content = t.readAll();
    content = content.arg( i18n( "My Computer" ),
                           htmlQuote("file:" + KStandardDirs::locate( "data", "sysinfo/about/style.css" )),
                           i18n( "My Computer"),
                           i18n( "Folders, Harddisks, Removable Devices, System Information and more..." ));

    QString sysInfo = "<div id=\"column2\">"; // table with 2 cols
    QString dummy;

    // disk info
    infoMessage( i18n( "Looking for disk information..." ) );
    sysInfo += "<h2 id=\"hdds\">" + i18n( "Disk Information" ) + "</h2>";
    sysInfo += diskInfo();

    osInfo();
    sysInfo += "<h2 id=\"sysinfo\">" +i18n( "OS Information" ) + "</h2>";
    sysInfo += "<table>";
    sysInfo += "<tr><td>" + i18n( "OS:" ) + "</td><td>" + htmlQuote(m_info[OS_SYSNAME]) + " " +
               htmlQuote(m_info[OS_RELEASE]) + " " + htmlQuote(m_info[OS_MACHINE]) + "</td></tr>";
    sysInfo += "<tr><td>" + i18n( "Current user:" ) + "</td><td>" + htmlQuote(m_info[OS_USER]) + "@"
               + htmlQuote(m_info[OS_HOSTNAME]) + "</td></tr>";
    sysInfo += "<tr><td>" + i18n( "System:" ) +  "</td><td>" + htmlQuote(m_info[OS_SYSTEM]) + "</td></tr>";
    sysInfo += "<tr><td>" + i18n( "KDE:" ) + "</td><td>" + KDE::versionString() + "</td></tr>";
    sysInfo += "</table>";

    // OpenGL info
    if ( glInfo() )
    {
        sysInfo += "<h2 id=\"display\">" + i18n( "Display Info" ) + "</h2>";
        sysInfo += "<table>";
        sysInfo += "<tr><td>" + i18n( "Vendor:" ) + "</td><td>" + htmlQuote(m_info[GFX_VENDOR]) +  "</td></tr>";
        sysInfo += "<tr><td>" + i18n( "Model:" ) + "</td><td>" + htmlQuote(m_info[GFX_MODEL]) + "</td></tr>";
        if (!m_info[GFX_DRIVER].isNull())
            sysInfo += "<tr><td>" + i18n( "Driver:" ) + "</td><td>" + htmlQuote(m_info[GFX_DRIVER]) + "</td></tr>";
        sysInfo += "</table>";
    }

    sysInfo += "</div><div id=\"column1\">"; // second column

    // OS info
    infoMessage( i18n( "Getting OS information...." ) );

    // common folders
    sysInfo += "<h2 id=\"dirs\">" + i18n( "Common Folders" ) + "</h2>"; sysInfo += "<ul>";
    if ( KStandardDirs::exists( KGlobalSettings::documentPath() + "/" ) )
        sysInfo += QString( "<li><a href=\"file:%1\">" ).arg( htmlQuote(KGlobalSettings::documentPath()) )
                   + i18n( "My Documents" ) + "</a></li>";
    sysInfo += QString( "<li><a href=\"file:%1\">" ).arg( htmlQuote(QDir::homePath()) ) + i18n( "My Home Folder" ) + "</a></li>";
    sysInfo += QString( "<li><a href=\"file:%1\">" ).arg( htmlQuote(QDir::rootPath()) ) + i18n( "Root Folder" ) + "</a></li>";
    sysInfo += "<li><a href=\"remote:/\">" + i18n( "Network Folders" ) + "</a></li>";
    sysInfo += "</ul>";

    // net info
    infoMessage( i18n( "Looking up network status..." ) );
    QString state = netStatus();
    if ( !state.isEmpty() ) // assume no network manager / networkstatus
    {
        sysInfo += "<h2 id=\"net\">" + i18n( "Network Status" ) + "</h2>";
        sysInfo += "<ul>";
        sysInfo += "<li>" + state + "</li>";
        sysInfo += "</ul>";
    }

    // more CPU info
    if ( !m_info[CPU_MODEL].isNull() )
    {
        sysInfo += "<h2 id=\"cpu\">" + i18n( "CPU Information" ) + "</h2>";
        sysInfo += "<table>";
        sysInfo += "<tr><td>" + i18n( "Processor (CPU):" ) + "</td><td>" + htmlQuote(m_info[CPU_MODEL]) + "</td></tr>";
        sysInfo += "<tr><td>" + i18n( "Speed:" ) + "</td><td>" +
                   i18n( "%1 MHz" , KGlobal::locale()->formatNumber( m_info[CPU_SPEED].toFloat(), 2 ) ) + "</td></tr>";
        int core_num = m_info[CPU_CORES].toUInt() + 1;
        if ( core_num > 1 )
            sysInfo += "<tr><td>" + i18n("Cores:") + QString("</td><td>%1</td></tr>").arg(core_num);

        if (!m_info[CPU_TEMP].isEmpty())
        {
            sysInfo += "<tr><td>" + i18n("Temperature:") + QString("</td><td>%1</td></tr>").arg(m_info[CPU_TEMP]);
        }
        sysInfo += "</table>";
    }

    // memory info
    infoMessage( i18n( "Looking for memory information..." ) );
    memoryInfo();
    sysInfo += "<h2 id=\"memory\">" + i18n( "Memory Information" ) + "</h2>";
    sysInfo += "<table>";
    sysInfo += "<tr><td>" + i18n( "Total memory (RAM):" ) + "</td><td>" + m_info[MEM_TOTALRAM] + "</td></tr>";
    sysInfo += "<tr><td>" + i18n( "Free memory:" ) + "</td><td>" + m_info[MEM_FREERAM] + "</td></tr>";
    dummy = i18n( "Used Memory" );
    dummy += "<tr><td>" + i18n( "Total swap:" ) + "</td><td>" + m_info[MEM_TOTALSWAP] + "</td></tr>";
    sysInfo += "<tr><td>" + i18n( "Free swap:" ) + "</td><td>" + m_info[MEM_FREESWAP] + "</td></tr>";
    sysInfo += "</table>";

    sysInfo += "</div>";

    // Send the data
    content = content.arg( sysInfo ); // put the sysinfo text into the main box
    data( content.toUtf8() );
    data( QByteArray() ); // empty array means we're done sending the data
    finished();
}

void kio_sysinfoProtocol::mimetype( const KUrl & /*url*/ )
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
    //kDebug(1242) << "scan_one " << key << " " << val;
    return val;
}

static quint64 calculateFreeRam()
{
    FILE *fd = fopen( "/proc/meminfo", "rt" );
    if ( !fd )
        return 0;

    QTextStream is(fd);
    QString MemInfoBuf = is.readAll();

    quint64 MemFree = scan_one( MemInfoBuf.toLatin1(), "MemFree" );
    quint64 Buffers = scan_one( MemInfoBuf.toLatin1(), "Buffers" );
    quint64 Cached  = scan_one( MemInfoBuf.toLatin1(), "Cached" );
    quint64 Slab    = scan_one( MemInfoBuf.toLatin1(), "Slab" );
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
        quint64 mem_unit = info.mem_unit;

        m_info[MEM_TOTALRAM] = formattedUnit( quint64(info.totalram) * mem_unit );
        quint64 totalFree = calculateFreeRam() * 1024;
        kDebug(1242) << "total " << totalFree << " free " << info.freeram << " unit " << mem_unit;
        if ( totalFree > info.freeram * info.mem_unit || true )
            m_info[MEM_FREERAM] = i18n("%1 (+ %2 Caches)",
                                       formattedUnit( quint64(info.freeram) * mem_unit ),
                                       formattedUnit( totalFree - info.freeram * mem_unit ));
        else
            m_info[MEM_FREERAM] = formattedUnit( quint64(info.freeram) * mem_unit );

        m_info[MEM_TOTALSWAP] = formattedUnit( quint64(info.totalswap) * mem_unit );
        m_info[MEM_FREESWAP] = formattedUnit( quint64(info.freeswap) * mem_unit );

        m_info[SYSTEM_UPTIME] = KIO::convertSeconds( info.uptime );
    }
}

void kio_sysinfoProtocol::cpuInfo()
{
    QString speed = readFromFile( "/proc/cpuinfo", "cpu MHz", ":" );

    if ( speed.isNull() )    // PPC?
        speed = readFromFile( "/proc/cpuinfo", "clock", ":" );

    if ( speed.endsWith( "MHz", Qt::CaseInsensitive ) )
        speed = speed.left( speed.length() - 3 );

    m_info[CPU_SPEED] = speed;
    m_info[CPU_CORES] = readFromFile( "/proc/cpuinfo", "processor", ":", true );

    const char* const names[] = { "THM0", "THRM", "THM" };
    for ( unsigned i = 0; i < sizeof(names)/sizeof(*names); ++i )
    {
        m_info[CPU_TEMP] = readFromFile(QString("/proc/acpi/thermal_zone/%1/temperature").arg(names[i]), "temperature", ":");
        m_info[CPU_TEMP] = m_info[CPU_TEMP].trimmed();
        m_info[CPU_TEMP].replace(" C",QString::fromUtf8("°C"));
        if (!m_info[CPU_TEMP].isEmpty())
            break;
    }

    m_info[CPU_MODEL] = readFromFile( "/proc/cpuinfo", "model name", ":" );
    if ( m_info[CPU_MODEL].isNull() ) // PPC?
         m_info[CPU_MODEL] = readFromFile( "/proc/cpuinfo", "cpu", ":" );
}

QString kio_sysinfoProtocol::diskInfo()
{
    QString result = "<table><tr><th>" + i18n( "Device" ) + "</th><th>" + i18n( "Filesystem" ) + "</th><th>" +
                     i18n( "Total space" ) + "</th><th>" + i18n( "Available space" ) + "</th></tr>";

    if ( fillMediaDevices() )
    {
        for ( QList<DiskInfo>::ConstIterator it = m_devices.constBegin(); it != m_devices.constEnd(); ++it )
        {
            QString tooltip = i18n("Press the right mouse button for more options like Mount or Eject");

            DiskInfo di = ( *it );
            unsigned int percent = 0;
            quint64 usage = di.total - di.avail;
            if (di.total)
                percent = usage / ( di.total / 100);

            QString media;
            if (di.mounted)
                media = "file://" + di.mountPoint;

            result += QString( "<tr><td>%1 <a href=\"%2\" title=\"%7\">%3</a></td><td>%4</td><td>%5</td><td>%6</td></tr>\n" ).
                      arg( icon( di.iconName ) ).arg( htmlQuote(media) ).arg( htmlQuote(di.label) ).arg( di.fsType ).
                      arg( di.total ? formattedUnit( di.total) : QString::null).
                      arg( di.mounted ? formattedUnit( di.avail ) : QString::null).
                      arg( htmlQuote( tooltip ) );
            if (di.mounted)
            {
                QColor c;
                c.setHsv(100-percent, 180, 230);
                QString dp = formattedUnit(usage).replace(" ", "&nbsp;");
                QString dpl, dpr;
                if (percent >= 50)
                    dpl = dp;
                else
                    dpr = dp;
                result += QString("<tr><td colspan=\"4\" class=\"bar\" width=\"100%\">"
                                  "<div><span class=\"filled\" style=\"text-align: right; width: %1%; height: 1em; background-color: %4\">"
                                  "%2</span><span style=\"color: #000; text-align: left\">%3</span></div></td></tr>\n")
                          .arg(percent).arg(dpl).arg(dpr).arg(c.name());
            }
        }
    }

    result += "</table>";

    return result;
}

#define HAVE_GLXCHOOSEVISUAL
#ifdef HAVE_GLXCHOOSEVISUAL
#include <GL/glx.h>
#endif

//-------------------------------------
bool hasDirectRendering ( QString &renderer ) {
    renderer = QString::null;

    Display *dpy = QX11Info::display();
    if (!dpy) return false;

#ifdef HAVE_GLXCHOOSEVISUAL
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

    XVisualInfo* visinfo = glXChooseVisual (
        dpy, QApplication::desktop()->primaryScreen(), attribSingle
    );
    if (visinfo)
    {
        GLXContext ctx = glXCreateContext ( dpy, visinfo, NULL, True );
        if (glXIsDirect(dpy, ctx))
        {
            glXDestroyContext (dpy,ctx);
            return true;
        }

        XSetWindowAttributes attr;
        unsigned long mask;
        Window root;
        XVisualInfo *visinfo;
        int width = 100, height = 100;
        int scrnum = QApplication::desktop()->primaryScreen();

        root = RootWindow(dpy, scrnum);

        visinfo = glXChooseVisual(dpy, scrnum, attribSingle);
        if (!visinfo)
        {
            visinfo = glXChooseVisual(dpy, scrnum, attribDouble);
            if (!visinfo)
            {
                fprintf(stderr, "Error: could not find RGB GLX visual\n");
                return false;
            }
        }

        attr.background_pixel = 0;
        attr.border_pixel = 0;
        attr.colormap = XCreateColormap(dpy, root, visinfo->visual, AllocNone);
        attr.event_mask = StructureNotifyMask | ExposureMask;
        mask = CWBackPixel | CWBorderPixel | CWColormap | CWEventMask;

        Window win = XCreateWindow(dpy, root, 0, 0, width, height,
                                   0, visinfo->depth, InputOutput,
                                   visinfo->visual, mask, &attr);

        if ( glXMakeCurrent(dpy, win, ctx))
            renderer = (const char *) glGetString(GL_RENDERER);
        XDestroyWindow(dpy, win);

        glXDestroyContext (dpy,ctx);
        return false;
    }
    else
    {
        return false;
    }
#else
#error no GL?
    return false;
#endif
}


bool kio_sysinfoProtocol::glInfo()
{
#ifdef HAVE_HD_H
    static hd_data_t hd_data;
    static bool inited_hd = false;
    if ( !inited_hd )
    {
        memset(&hd_data, 0, sizeof(hd_data));
        inited_hd = true;
    }

    if (!hd_list(&hd_data, hw_display, 1, NULL))
        return false;

    hd_t* hd = hd_get_device_by_idx(&hd_data, hd_display_adapter(&hd_data));

    if (!hd)
        return false;

    driver_info_t *di = hd->driver_info;
    QString renderer;
    bool dri = hasDirectRendering( renderer );
    QString driver;

    for(di = di; di; di = di->next)
    {
        QString loadline;
        if (di->any.type == di_x11)
            driver = di->x11.server;
        else if (di->any.type == di_module && di->module.names)
            driver = di->module.names->str;
        loadline = QString("(II) LoadModule: \"%1\"").arg( driver );

        QFile file( "/var/log/Xorg.0.log" );
        if ( !file.exists() || !file.open( QIODevice::ReadOnly ) )
        {
            di = 0;
            break;
        }

        QTextStream stream( &file );
        QString line;
        bool found_line = false;

        while ( !stream.atEnd() )
        {
            line = stream.readLine();
            if (line == loadline)
            {
                found_line = true;
                break;
            }
        }

        kDebug(1242) << "found_line " << found_line;
        if (found_line)
            break;
        else
            driver = QString::null;
    }

    m_info[GFX_VENDOR] = hd->vendor.name;
    m_info[GFX_MODEL] = hd->device.name;
    if (!driver.isNull())
    {
        if (dri)
            m_info[GFX_DRIVER] = i18n("%1 (3D Support)", driver);
        else
        {
            if ( renderer.contains( "Mesa GLX Indirect" ) )
                m_info[GFX_DRIVER] = i18n("%1 (No 3D Support)", driver);
            else
                m_info[GFX_DRIVER] = driver;
        }
    }
    else
        m_info[GFX_DRIVER] = i18n( "Unknown" );

    return true;
#else
    FILE *fd = popen( "glxinfo", "r" );
    if ( !fd )
        return false;

    QTextStream is( fd );

    while ( !is.atEnd() )
    {
        QString line = is.readLine();
        if ( line.startsWith( "OpenGL vendor string:" ) )
            m_info[GFX_VENDOR] = line.section(':', 1, 1);
        else if ( line.startsWith( "OpenGL renderer string:" ) )
            m_info[GFX_MODEL] = line.section(':', 1, 1);
        else if ( line.startsWith( "OpenGL version string:" ) )
            m_info[GFX_DRIVER] = line.section(':', 1, 1);
    }

    pclose( fd );
    return true;
#endif

    return false;
}

QString kio_sysinfoProtocol::icon( const QString & name, int size ) const
{
    QString path = KIconLoader::global()->iconPath( name, -size );
    return QString( "<img src=\"file:%1\" width=\"%2\" height=\"%3\" valign=\"bottom\"/>" )
        .arg( htmlQuote(path) ).arg( size ).arg( size );
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

#ifdef WITH_FEDORA
    m_info[ OS_SYSTEM ] = readFromFile( "/etc/fedora-release" );
#else
    m_info[ OS_SYSTEM ] = readFromFile( "/etc/SuSE-release" );
#endif
    m_info[ OS_SYSTEM ].replace("X86-64", "x86_64");
}

extern "C" int KDE_EXPORT kdemain(int argc, char **argv)
{
    KComponentData componentData( "kio_sysinfo" );
    ( void ) KGlobal::locale();

    kDebug(1242) << "*** Starting kio_sysinfo ";

    if (argc != 4) {
        kDebug(1242) << "Usage: kio_sysinfo  protocol domain-socket1 domain-socket2";
        exit(-1);
    }

    kio_sysinfoProtocol slave(argv[2], argv[3]);
    slave.dispatchLoop();

    kDebug(1242) << "*** kio_sysinfo Done";
    return 0;
}

bool kio_sysinfoProtocol::fillMediaDevices()
{
    QStringList devices;

    const QList<Solid::Device> &deviceList = Solid::Device::listFromQuery(m_predicate);

    if (deviceList.isEmpty())
    {
        kDebug(1242) << "DEVICE LIST IS EMPTY!";
        return false;
    }

    m_devices.clear();

    foreach(const Solid::Device &device, deviceList)
    {
        if (!device.isValid())
            continue;

        const Solid::StorageAccess *access = device.as<Solid::StorageAccess>();
        const Solid::StorageVolume *volume = device.as<Solid::StorageVolume>();
        const Solid::Block *block = device.as<Solid::Block>();

        DiskInfo di;

        di.id = device.udi();
        if (access)
            di.mountPoint = access->filePath();

        if (volume)
            di.label = volume->label();
        if (di.label.isEmpty())
            di.label = di.mountPoint;
        di.mountable = access != 0;
        if (block)
            di.deviceNode = block->device();
        if (volume)
            di.fsType = volume->fsType();
        di.mounted = access && access->isAccessible();
        di.iconName = device.icon();

        di.total = di.avail = 0;

        if (volume)
            di.total = volume->size();

        // calc the free/total space
        struct statfs sfs;
        if ( di.mounted && statfs( QFile::encodeName( di.mountPoint ), &sfs ) == 0 )
        {
            di.total = ( unsigned long long )sfs.f_blocks * sfs.f_bsize;
            di.avail = ( unsigned long long )( getuid() ? sfs.f_bavail : sfs.f_bfree ) * sfs.f_bsize;
        }

        m_devices.append( di );
    }

    // this is ugly workaround, should be in HAL but there is no LVM support
    QRegExp rxlvm("^/dev/mapper/\\S*-\\S*");

    const KMountPoint::List mountPoints = KMountPoint::currentMountPoints(KMountPoint::NeedRealDeviceName);

    foreach( KMountPoint::Ptr mountPoint, mountPoints)
    {
        if ( rxlvm.exactMatch( mountPoint->realDeviceName() ) )
        {
            DiskInfo di;

            di.mountPoint = mountPoint->mountPoint();
            di.label = di.mountPoint;
            di.mountable = di.mounted = true;
            di.deviceNode = mountPoint->realDeviceName();
            di.fsType = mountPoint->mountType();
            di.iconName = QString::fromLatin1( "drive-harddisk" );

            di.total = di.avail = 0;

            // calc the free/total space
            struct statfs sfs;
            if ( di.mounted && statfs( QFile::encodeName( di.mountPoint ), &sfs ) == 0 )
            {
                di.total = ( unsigned long long )sfs.f_blocks * sfs.f_bsize;
                di.avail = ( unsigned long long )( getuid() ? sfs.f_bavail : sfs.f_bfree ) * sfs.f_bsize;
            }

            m_devices.append( di );
        }
    }


    return true;
}
