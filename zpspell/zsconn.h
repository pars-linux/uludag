/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  ZemberekServer Connection.
*/

#ifndef ZSCONN_H
#define ZSCONN_H

#include <string>

using namespace std;

enum Z_CHECK_RESULT {
    Z_TRUE = 0,
    Z_FALSE,
    Z_UNKNOWN
};

class ZSConn
{
public:
    ZSConn();
    ~ZSConn();

    Z_CHECK_RESULT checkString( const string& str ) const;

private:
    int _conn;
    char* recvResult() const;
};

#endif
