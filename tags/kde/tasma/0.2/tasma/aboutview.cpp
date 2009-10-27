/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - aboutview.cpp
  AboutView implementation
*/

#include <qpainter.h>
#include <qpixmap.h>
#include <kpixmap.h>
#include <kpixmapeffect.h>
#include <kstandarddirs.h>
#include <klocale.h>
#include <kglobalsettings.h>

#include "aboutview.h"

AboutView::AboutView( QWidget *parent, const char *name )
    : QWidget( parent, name )
{
    setPaletteBackgroundColor( KGlobalSettings::alternateBackgroundColor() );

    // init pixmaps
    _tasmaLogo = new QPixmap( locate( "data", "tasma/tasma_logo.png" ) );
    _pardusLogo = new KPixmap( locate( "data", "tasma/pardus.png" ) );
    KPixmapEffect::fade( *_pardusLogo, 0.80, Qt::white );
}

void AboutView::paintEvent( QPaintEvent *e )
{
    updateView( geometry() );
}

void AboutView::updateView( const QRect& rect )
{
    QPainter p( this );

    int lw = _tasmaLogo->width();
    int lh = _tasmaLogo->height();

    // A rect for tasma_logo and title
    p.setBrush( KGlobalSettings::baseColor() );
    QPen old_pen = p.pen();
    p.setPen( NoPen );
    p.drawRect( 0, 0, rect.width(), lh + 10 );
    p.setPen( old_pen );
    p.setPen( SolidLine );
    p.drawLine( 0, lh+10, rect.width(), lh+10 );

    // tasma logo
    p.drawPixmap( 5, 0, *_tasmaLogo );

    // title text
    QFont f = font();
    QFont f_title( f );
    f_title.setBold( true );
    f_title.setPointSize( 25 );
    p.setFont( f_title );
    p.drawText( 15 + lw, lh/2 - 5, "Pardus" );
    p.drawText( 15 + lw, lh/2 + 30, i18n( "Configuration Center" ) );

    if ( height() > 350 )
    {
        // pardus logo
        int px = rect.width() - _pardusLogo->width();
        int py = rect.height() - _pardusLogo->height();
        p.drawPixmap( px, py, *_pardusLogo );
    }

    QFont f2( f );
    f2.setBold( true );

    // desc text
    int descX = 30;
    int descY = lh + 50; // 50pix far from title
    p.setFont( f2 );
    p.drawText( descX, descY,
                i18n( "Welcome to TASMA" ) );
    p.setFont( f );
    QString desc1 = i18n( "TASMA is a configuration application for "
                          "Pardus Operating System. You can tweak the "
                          "systems default configuration settings and "
                          "by using the modules presented in TASMA. " );
    QRect r = p.boundingRect( descX, descY+10,
                              rect.width()-descX*2, rect.height()-(descY+50),
                              AlignLeft | AlignTop | WordBreak, desc1 );
    p.drawText( descX, descY+10,
                rect.width()-descX*2, rect.height()-(descY+50),
                AlignLeft | AlignTop | WordBreak, desc1 );

    QString desc2 = i18n( "For a better understanding modules are grouped "
                          "by categories. You can activate a category by "
                          "selecting a category from the left. After activating "
                          "a category its contents will be shown as icons "
                          "in the right panel. You can start a configuration module "
                          "by clicking (or double clicking) its icon." );

    p.drawText( descX, descY+r.height()+20, // 10pix far from desc1
                rect.width()-descX*2, rect.height()-(descY+50),
                AlignLeft | AlignTop | WordBreak, desc2 );

}
