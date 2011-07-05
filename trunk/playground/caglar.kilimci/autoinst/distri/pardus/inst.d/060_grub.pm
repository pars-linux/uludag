use base "basetest";
use strict;
use bmwqemu;

sub run()
{
    waitidle;
    # mousemove_raw(16550, 18350);
    for(1..6) {sendkey "tab"}
    sendkey "spc";
    sleep 3;
}

1;
