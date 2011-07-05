use base "basetest";
use strict;
use bmwqemu;

sub run()
{
    waitidle;
    for(1..6) {sendkey "tab"}
    sendkey "spc";
    # mousemove_raw(16550, 18350);

    waitidle;
    sendkey "spc";
}

1;
