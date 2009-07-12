#!/bin/sh

lang=`kreadconfig --group Locale --key Language`
if [ -n "$lang" ]; then
    desktopfile=`kde4-config --path xdgdata-apps --locate kde4/displaysettings.desktop`
    title=$(grep "^Name\[$lang\]=" $desktopfile | cut -d= -f 2)
else
    title=$(TEXTDOMAINDIR=`kde4-config --install locale` gettext display-settings "Display Settings")
fi

exec kcmshell4 --icon preferences-desktop-display --caption "$title" kcm_displaysettings kcm_displaydevices energy kgamma
