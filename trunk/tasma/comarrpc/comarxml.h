/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  comarrpc - xmlrpc.h

  ComarRPCdata marshaller :)
*/

#include <qstring.h>

class RPCparam;

enum RPCPrio {
    NORMAL = 0,
    URGENT,
    INTERACTIVE,
    DONTCARE
};

class ComarXML
{
public:
    ComarXML( int eoltime = 7200, RPCPrio priority = NORMAL );
//    ComarXML(const char* xml_data);
    ~ComarXML();

    bool buildXML( const RPCparam& params );
    const char* getXML();

protected:
    void initialize();

    void beginNode( const char* node );
    void addValue( const char* val );
    void endNode( const char* node );

    void finalize();
    
/*
    char *getValue( .... );
*/

private:
    QString *xmlData;
    int _eol; // end of life time (seconds)
    RPCPrio _prio;
};
