#!/bin/bash
# Copyright © 2005  TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# Original work belongs Gentoo Linux

source /etc/init.d/functions.sh || exit 1

if [ "${EUID}" -ne 0 ]
then
	eerror "$0: must be root."
	exit 1
fi

usage() {
echo "usage: env-update.sh

note:
      This utility generates /etc/profile.env and /etc/csh.env
      from the contents of /etc/env.d/
"
	exit 1
}

export SVCDIR="${svcdir}"

# Only update if files have actually changed
if [ "$1" == "-u" ]
then
	is_older_than "${svcdir}/envcache" /etc/env.d && exit 0
	shift
fi

if [ "$#" -ne 0 ]
then
	usage
else
	/bin/gawk \
		-f /lib/rcscripts/awk/functions.awk \
		-f /lib/rcscripts/awk/genenviron.awk
fi


# vim:ts=4
