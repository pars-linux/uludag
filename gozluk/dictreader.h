/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef DICT_READER_H
#define DICT_READER_H

#include <qxml.h>
#include <qobject.h>

class DictReader : public QObject, public QXmlDefaultHandler
{
    Q_OBJECT
public:
    DictReader ( QObject *parent , const char *name = 0 )
	: QObject( parent ) {};
    
    bool startDocument();
    bool startElement (const QString&,
		       const QString&,
		       const QString&,
		       const QXmlAttributes&);
    bool characters (const QString&);
    bool endElement (const QString&,
		     const QString&,
		     const QString&);

signals:
    void signalSource (const QString);
    void signalTranslation (const QString);
    void signalDefinition (const QString);
    void signalEndTerm();

private:
    bool inUdSozluk;
    bool inTerm;
    bool inS; // source
    bool inT; // translation
    bool inD; // definition
};

#endif // DICT_READER_H
