/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include "comarrpc.h"
#include "comarxml.h"

#define RPC_VERSION "1.0"

ComarXML::ComarXML( int eoltime, RPCPrio priority )
    : _eol( eoltime ), _prio( priority )
{
    xmlData = new QString();
}

bool ComarXML::buildXML( const RPCparam& params )
{
    initialize();

    // parametreleri ayıkla, geçerliliklerini kontrol et.
    // XML verisini oluştur.
    // OMCALL için test ediyoruz sadece... parametrelerin durumlarına göre
    // (rpctype'a göre?) geçerlilik kontrolü burada yapılacak.
    RPCparamIterator it(  params );
    for (  ; it.current(); ++it ) {
        if (  QString(  "rpctype" ) == it.currentKey() ) {
            beginNode(  "RPCType" );
            addValue(  it.current() );
            endNode(  "RPCType" );
        }
        else if (  QString(  "type" ) == it.currentKey() ) {
            beginNode(  "type" );
            addValue(  it.current() );
            endNode(  "type" );
        }
        else if (  QString(  "name" ) == it.currentKey() ) {
            beginNode(  "name" );
            addValue(  it.current() );
            endNode(  "name" );
        }
        else if (  QString(  "index" ) == it.currentKey() ) {
            beginNode(  "index" );
            addValue(  it.current() );
            endNode(  "index" );
        }
        else if (  QString(  "parameters" ) == it.currentKey() ) {
            beginNode(  "parameters" );
            addValue(  it.current() );
            endNode(  "parameters" );
        }
    }

    finalize();
    return true;
}

const char* ComarXML::getXML()
{
    /*
    QByteArray *data = new QByteArray();
    data->setRawData( xmlData->ascii(), xmlData->length() );
    */
    return xmlData->ascii();
}


void ComarXML::initialize()
{
    xmlData->append( "<COMARRPCData><RPCVersion>"RPC_VERSION"</RPCVersion>" );

    int eol = _eol + ( unsigned int )time(NULL);
    srand( eol );
    int r = rand();

    char *ttsid = new char[255];
    sprintf( ttsid, "tasma-%d-%d", eol, r );

    xmlData->append( "<RPCTTSID>" + QString( ttsid ) + "</RPCTTSID>" );
    delete [] ttsid;

    char *e = new char[20];
    sprintf( e, "%d", eol );
    xmlData->append( "<RPCEOLTime>" + QString( e ) + "</RPCEOLTime>" );
    delete [] e;

    QString prio;
    switch ( _prio )
    {
    case NORMAL:
        prio = "NORMAL";
        break;
    case URGENT:
        prio = "URGENT";
        break;
    case INTERACTIVE:
        prio = "INTERACTIVE";
        break;
    case DONTCARE:
        prio = "DONTCARE";
        break;
    default:
        prio = "NORMAL";
    }
    xmlData->append( "<RPCPriority>" + prio + "</RPCPriority>" );

    xmlData->append( "<RPCData>" );
}

void ComarXML::beginNode( const char* node )
{
    xmlData->append( "<" );
    xmlData->append( node );
    xmlData->append( ">" );
}

void ComarXML::addValue( const char* val )
{
    xmlData->append( val );
}

void ComarXML::endNode( const char* node )
{
    xmlData->append( "</" );
    xmlData->append( node );
    xmlData->append( ">" );
}

ComarXML::~ComarXML()
{
    delete xmlData;
}

void ComarXML::finalize()
{
    xmlData->append( "</RPCData></COMARRPCData>" );
}

