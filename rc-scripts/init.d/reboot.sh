# Copyright © 2005  TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# Original work belongs Gentoo Linux

/sbin/reboot -idp

# hmm, if the above failed, that's kind of odd ...
# so let's force a reboot
/sbin/reboot -f
