use base "basetest";
use strict;
use bmwqemu;

sub run()
{
    waitidle;
    for(1..13) {sendkey "tab"}
    sendkey "spc";
    sleep 3;
}

1;
