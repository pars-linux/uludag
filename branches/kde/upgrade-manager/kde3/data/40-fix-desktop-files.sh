/bin/cp -f /usr/kde/4/share/apps/kio_desktop/DesktopLinks/Home.desktop `/usr/bin/xdg-user-dir DESKTOP`
/bin/sed -i s/Icon=system/Icon=computer/g `/usr/bin/xdg-user-dir DESKTOP`/System.desktop
