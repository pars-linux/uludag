#include <comarrpc/comarrpcunix.h>

int main()
{
    ComarRPCUNIX rpc;

    RPCparam params;

    params.insert( "sock_file", "/tmp/comar-test" );
    if ( !rpc.Connect( params ) ) {
        printf( "baglanti saglanamadi...\n" );
        return -1;
    }

    params.clear();
    params.insert( "user", "baris" );
    params.insert( "password", "gizli" );
    if ( !rpc.Auth( params ) ) {
        printf( "yetkilendirme basarisiz...\n" );
        return -1;
    }

    params.clear();
    params.insert( "rpctype", "OMCALL" );
    params.insert( "type", "method" );
    params.insert( "name", "none" );
    params.insert( "index", "0" );
    params.insert( "parameters", "yok" );
    if ( !rpc.Send( params ) ) {
        printf( "gönderme basarisiz...\n" );
        return -1;
    }

    return 0;
}

