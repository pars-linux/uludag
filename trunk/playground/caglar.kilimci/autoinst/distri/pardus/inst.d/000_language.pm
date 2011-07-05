use base "basetest";
use strict;
use bmwqemu;

sub run()
{
    # sleep 2;
    sendkey "up";
    sendkey "up";
    sendkey "ret";
    sendkey "ret";
}

1;
