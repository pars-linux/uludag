/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <klocale.h>

#include <qmessagebox.h>

#include "hardwareinfo.h"

HardwareInfo::HardwareInfo( QWidget *parent, const char* name )
    : HardwareInfoDlg( parent, name )
{
	permit = false;

	file.setName("index.html");

	if(!file.open(IO_WriteOnly))
	{
		QMessageBox::warning( this, i18n("Cannot write file"), i18n("Error %1 %2")
						.arg(file.errorString())
						.arg(file.name()));
	}	
	connect(&http, SIGNAL(done(bool)), this, SLOT(done(bool)));
    connect(&http, SIGNAL(stateChanged(int)), this, SLOT(stateChanged(int)));

	httpConnect( "tux.uludag.org.tr", "/index.php", &file );

}

HardwareInfo::~HardwareInfo()
{
}

void HardwareInfo::httpConnect( QString url, QString path, QFile *file)
{
	if( permit )
	{
	    QHttpRequestHeader header( "POST", path );
    	header.setValue( "Host", url );
	    header.setContentType( "text/html" );

		http.setHost ( url );
		http.request( header, QCString("?pardus=m"), file );
	}
}

void HardwareInfo::done( bool error )
{
	if ( error )
		QMessageBox::warning( this, i18n("HTTP Get"), i18n("Error %1").arg(http.errorString()));

//	QString result(http.readAll());
//  QMessageBox::information( this, i18n("Sent To Server"), result);

	file.close();
}

void HardwareInfo::stateChanged( int state )
{
	if ( state == QHttp::Connecting )
		QMessageBox::information( this, i18n("HTTP Connecting"), i18n("Connecting..."));
	
	if ( state == QHttp::Sending )
		QMessageBox::information( this, i18n("HTTP Connecting"), i18n("Sending Request..."));
	
	if ( state == QHttp::Reading )
		QMessageBox::information( this, i18n("HTTP Connecting"), i18n("Reading Data..."));

	if ( state == QHttp::Closing )
		QMessageBox::information( this, i18n("HTTP Connecting"), i18n("Closing..."));

	if ( state == QHttp::Unconnected )
		QMessageBox::information( this, i18n("HTTP Connecting"), i18n("Unconnected..."));
}
