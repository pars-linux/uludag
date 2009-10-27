/*  This file is part of the KDE project
    Copyright (C) 2002 Alexander Neundorf <neundorf@kde.org>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details.

    You should have received a copy of the GNU Library General Public License
    along with this library; see the file COPYING.LIB.  If not, write to
    the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA 02110-1301, USA.
*/

#include "ksysinfopart.h"
#include <qstring.h>

#include <qtimer.h>
#include <kinstance.h>
#include <kglobal.h>
#include <kdebug.h>
#include <klocale.h>
#include <kstandarddirs.h>
#include <kaboutdata.h>
#include <kdeversion.h>
#include <kpopupmenu.h>
#include <khtmlview.h>
#include <khtml_events.h>
#include <qcursor.h>
#include <kio/netaccess.h>
#include <kfileitem.h>

extern "C"
{
    KDE_EXPORT void* init_libksysinfopart()
    {
        return new KSysinfoPartFactory;
    }
}

KInstance* KSysinfoPartFactory::s_instance = 0L;
KAboutData* KSysinfoPartFactory::s_about = 0L;

KSysinfoPartFactory::KSysinfoPartFactory( QObject* parent, const char* name )
: KParts::Factory( parent, name )
{}

KSysinfoPartFactory::~KSysinfoPartFactory()
{
    delete s_instance;
    s_instance = 0L;
    delete s_about;
}

KParts::Part* KSysinfoPartFactory::createPartObject( QWidget * parentWidget, const char* /*widgetName*/, QObject *,
                                                     const char* name, const char* /*className*/,const QStringList & )
{
    KSysinfoPart* part = new KSysinfoPart( parentWidget, name );
    return part;
}

KInstance* KSysinfoPartFactory::instance()
{
    if( !s_instance )
    {
        s_about = new KAboutData( "ksysinfopart",
                                  I18N_NOOP( "KSysinfo" ), KDE_VERSION_STRING );
        s_instance = new KInstance( s_about );
    }
    return s_instance;
}


KSysinfoPart::KSysinfoPart( QWidget * parent, const char * name )
: KHTMLPart( parent, name )
{
    KInstance * instance = new KInstance( "ksysinfopart" );
    setInstance( instance );
    rescanTimer=new QTimer(this);

    connect(rescanTimer, SIGNAL(timeout()),
                         SLOT(rescan()));

    rescanTimer->start( 20000, true );

    connectDCOPSignal( "kded", "networkstatus", "statusChange(QString,int)", "rescan()", false );
    installEventFilter( this );
}

void KSysinfoPart::slotResult( KIO::Job *job )
{
    KIO::StatJob *sjob = dynamic_cast<KIO::StatJob*>( job );
    if (!job)
        return;

    KFileItem item(sjob->statResult(), sjob->url());
    KFileItemList list;
    list.append(&item);
    emit browserExtension()->popupMenu( 0, QCursor::pos(), list );
}

void KSysinfoPart::customEvent( QCustomEvent *event )
{
    if ( KParts::Event::test( event, "khtml/Events/MousePressEvent" ) )
    {
        khtml::MousePressEvent *ev = static_cast<khtml::MousePressEvent *>( event );
        KURL url(ev->url().string());
        if (url.protocol() == "media" && ev->qmouseEvent()->button() == QMouseEvent::RightButton ) 
        {
            KIO::UDSEntry entry;
            KIO::Job *job = KIO::stat( url, false );

            connect( job, SIGNAL( result( KIO::Job * ) ),
                          SLOT( slotResult( KIO::Job * ) ) );
            return;
        }
    }
    KHTMLPart::customEvent(event);
}

void KSysinfoPart::rescan()
{
    openURL( "sysinfo:/" );
    rescanTimer->stop();
    rescanTimer->start( 20000, true );
}

void KSysinfoPart::FilesAdded( const KURL & dir )
{
    if (dir.protocol() == "media")
    {
        rescanTimer->stop();
        rescanTimer->start( 10, true );
    }
}

void KSysinfoPart::FilesRemoved( const KURL::List & urls )
{
    for ( KURL::List::ConstIterator it = urls.begin() ; it != urls.end() ; ++it )
        FilesAdded( *it );
}

void KSysinfoPart::FilesChanged( const KURL::List & urls )
{
    // not same signal, but same implementation
    FilesRemoved( urls );
}

#include "ksysinfopart.moc"

