/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef COMAR_RPC_HTTP_H
#define COMAR_RPC_HTTP_H

#include <comarrpc/comarrpc.h>

class QHttp;

class ComarRPCHTTP : public ComarRPC
{
public:
    ComarRPCHTTP() {}
    virtual ~ComarRPCHTTP() {}

    bool Connect( RPCparam& connect_params);

    /* no authorization for now */
    bool Auth( RPCparam& auth_params );

    int Send( RPCparam& send_params );

    RPCparam* Recv();

private:
    QHttp *_http;
};



#endif // COMAR_RPC_HTTP_H
