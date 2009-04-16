/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include "dictreader.h"

bool DictReader::startDocument ()
{
    inS = inT = inD = inTerm = inUdSozluk = false;
    return true;
}

bool DictReader::startElement ( const QString& /* nsUri */,
                                const QString& /* localName */,
                                const QString& qName,
                                const QXmlAttributes& /* attrs */ )
{
    if ( inUdSozluk ) {
        if ( qName == "term" )
            inTerm = true;
        else if ( qName == "s" )
            inS = true;
        else if ( qName == "t" )
            inT = true;
        else if ( qName == "d" )
            inD = true;
    } else {
        if ( qName == QString::fromUtf8( "ud_sözlük" ) )
            inUdSozluk = true;
    }
    return true;
}

bool DictReader::characters ( const QString &ch )
{
    if ( inTerm ) {

        if ( inS )
            emit signalSource ( ch );
        else if ( inT )
            emit signalTranslation( ch );
        else if ( inD )
            emit signalDefinition( ch );
    }
    return true;
}

bool DictReader::endElement ( const QString& /* nsUri */,
                              const QString& /* localName */,
                              const QString& qName )
{
    if ( qName == "term" ) {
        emit signalEndTerm();
        inTerm = false;
    }
    else if ( qName == "s" )
        inS = false;
    else if ( qName == "t" )
        inT = false;
    else if ( qName == "d" )
        inD = false;
    else if ( qName == QString::fromUtf8( "ud_sözlük" ) )
        inUdSozluk = false;

    return true;
}
