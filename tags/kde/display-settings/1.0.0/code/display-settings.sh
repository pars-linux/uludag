#!/bin/sh

name="Display Settings"
lang=`kreadconfig --group Locale --key Language`
if [ -n "$lang" ]; then
    desktopfile=`kde4-config --path xdgdata-apps --locate kde4/displaysettings.desktop`
    title=$(grep "^Name\[$lang\]=" $desktopfile | cut -d= -f 2)
    test -z "$title" && title="$name"
else
    title=$(TEXTDOMAINDIR=`kde4-config --install locale` gettext display-settings "$name")
fi

exec kcmshell4 --icon preferences-desktop-display --caption "$title" kcm_displaysettings kcm_displaydevices energy kgamma
