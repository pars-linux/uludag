/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  comarrpc - comarrpc.h
  RPCparam: dictionary based parameters for RPC functions.
  ComarRPC: an abstract base class for real RPC classes
*/

#ifndef COMAR_RPC_H
#define COMAR_RPC_H

#include <qasciidict.h>

/* 
   Every RPC class needs different parameters for regular functions
   (functions defined in ComarRPC). So we'll use a dictionary
   based parameter list which will suit for all.

   Library user will build the list before passing it to a function.
   For an example please see the test program(s) in test/ subdirectory.
*/

class RPCparam : public QAsciiDict<char>
{
public:
    RPCparam() 
	: QAsciiDict<char>()
    { 
	/* mutual for us!
	   setAutoDelete( true ); */
    }

    virtual ~RPCparam() {}
};

typedef QAsciiDictIterator<char> RPCparamIterator;

/*
#define rpcCommand(c)  new QString(c)
#define rpcValue(v)  new QString(v)
*/


class ComarRPC
{
public:
    ComarRPC() {}
    virtual ~ComarRPC() {}

    virtual bool Connect( RPCparam& connect_params ) = 0;
    virtual bool Auth( RPCparam& auth_params ) = 0;
    virtual int Send( RPCparam& send_params ) = 0;
    virtual RPCparam* Recv() = 0;
};

#endif // COMAR_RPC_H
