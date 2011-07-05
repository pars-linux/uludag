use base "basetest";
use strict;
use bmwqemu;

sub run()
{
    waitidle;
    for(1..7) {sendkey "tab"}
    sendkey "spc";
}

1;
