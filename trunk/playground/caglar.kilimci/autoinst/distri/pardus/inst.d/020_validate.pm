use base "basetest";
use strict;
use bmwqemu;

sub run()
{
    waitidle;
    for(1..6) {sendkey "tab"}
    sendkey "spc"
}

1;
