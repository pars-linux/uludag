/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef HARDWAREINFO_H
#define HARDWAREINFO_H

#include <qhttp.h>
#include <qfile.h>

#include "hardwareinfodlg.h"

class HardwareInfo : public HardwareInfoDlg
{
	Q_OBJECT
public:
	HardwareInfo( QWidget *parent = 0, const char* name = 0 );
	~HardwareInfo();

	bool permit;
private:
	QHttp http;
	QFile file;
	void HardwareInfo::httpConnect( QString url, QString path, QFile *file);

protected slots:
	void done( bool error );
	void stateChanged ( int state );
};

#endif // HARDWAREINFO_H
