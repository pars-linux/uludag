use base "basetest";
use strict;
use bmwqemu;

sub run()
{
    # Re-initilaze harddisk
    waitidle;
    sendkey "spc";
    waitidle;
    sendkey "spc";
    waitidle;
    sendkey "spc";
    waitidle;
    sendkey "spc";

    # mousemove_raw(16550, 18350);

    # Choose harddisk
    waitidle;
    for(1..6) {sendkey "tab"}
    sendkey "spc";

    # mousemove_raw(16550, 14350);

    # Use all
    waitidle;
    sendkey "tab";
    sendkey "spc";
    for(1..5) {sendkey "tab"}
    sendkey "spc";

    # mousemove_raw(200, 200);
    sleep 3;
}

1;
