# consts. 1:is static file, 2:is executable

standartLogs= {"/var/log/comar.log"         :1,
               "/var/log/user.log"          :1,
               "/var/log/Xorg.0.log"        :1,
               "/bin/dmesg"                 :2,
               "/usr/bin/uname -a"          :2}
hardwareInfo= {"/bin/mount"                 :2,
               "/sbin/ifconfig -a"          :2,
               "/usr/sbin/iwconfig"         :2,
               "/usr/sbin/lspci"            :2,
               "/usr/sbin/lspci -n"         :2,
               "/usr/sbin/lsusb"            :2,
               "/usr/bin/lsscsi -v"         :2,
               "/sbin/fdisk -l"             :2,
               "/usr/bin/df -h"             :2,
               "/bin/service"               :2,
               "/sbin/muavin.py --debug"    :2,
               "/usr/bin/free"              :2}
configFiles = {"/boot/grub/grub.conf"       :1,
               "/etc/fstab"                 :1,
               "/etc/X11/xorg.conf"         :1,
               "/etc/conf.d/915resolution"  :1,
               "/etc/conf.d/local.start"    :1,
               "/etc/resolv.conf"           :1,
               "/etc/conf.d/mudur"          :1,
               "/etc/mudur/language"        :1,
               "/etc/mudur/locale"          :1,
               "/etc/mudur/keymap"          :1}
packageInfo = {"/usr/bin/pisi li -l"        :2,
               "/usr/bin/pisi lr"           :2,
               "/usr/bin/pisi lu -l"        :2}
