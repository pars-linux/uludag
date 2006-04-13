/*
 * Copyright © 2005  TUBITAK/UEKAE
 * Licensed under the GNU General Public License, version 2.
 * See the file http://www.gnu.org/copyleft/gpl.txt.
 *
 * S.Çağlar Onur <caglar@uludag.org.
 */

#include <fcntl.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <linux/kd.h>
#include <errno.h>

int main(int argc, char *argv[])
{
    int fd = open_a_console(argv[1]);

    if( argc < 2 )
    {
        fprintf( stderr, ( "where is the device???\n"));
        exit( 1 );
    }

    if( fd >= 0 )
    {
        if( ioctl( fd, KDSKBMODE, K_UNICODE ))
        {
            perror( "KDSKBMODE" );
            fprintf( stderr, ( "%s: error setting keyboard mode\n" ), argv[1] );
            exit( 1 );
        }
    }
    else
        fprintf( stderr, "%s : can't open device\n", argv[1] );

    return 0;
}

int open_a_console( const char *file )
{
    int fd;

    fd = open( file, O_RDWR );

    if( fd < 0 && errno == EACCES )
               fd = open( file, O_WRONLY );

    if( fd < 0 && errno == EACCES )
        fd = open( file, O_RDONLY );

    if( fd < 0 )
        return -1;

    if( !is_a_console( fd ))
    {
        close( fd );
        return -1;
    }

    return fd;
}

int is_a_console(int fd)
{
    char arg = 0;
    return ( ioctl( fd, KDGKBTYPE, &arg ) == 0 && (( arg == KB_101 ) || ( arg == KB_84 )));
}
