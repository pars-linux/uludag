use base "basetest";
use strict;
use bmwqemu;

sub run()
{
    # sleep 10;
    waitidle;
    # sendkeyw "\t\t\t\t ";
    # mousemove_raw(16550, 18350);
    # sleep 2;
    # mouseclick();
    for(1..4) {sendkey "tab"}
    sendkey "spc";
    # sleep 3;
    for(1..4) {sendkey "tab"}
    sendkey "spc";
    # sendkey "alt-n";
    # mousemove_raw(16550, 18350);
}

1;
