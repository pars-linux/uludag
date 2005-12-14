# Copyright © 2005  TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# Original work belongs Gentoo Linux

RC_GOT_FUNCTIONS="yes"

# daemontools dir
SVCDIR="/var/lib/supervise"

# Check /etc/conf.d/rc for a description of these ...
svcdir="/var/lib/init.d"
svclib="/lib/rcscripts"
svcmount="no"
svcfstype="tmpfs"
svcsize=1024

# Different types of dependencies
deptypes="need use"
# Different types of order deps
ordtypes="before after"

#
# Internal variables
#

# Dont output to stdout?
RC_QUIET_STDOUT="no"
RC_VERBOSE=${RC_VERBOSE:-no}

# Should we use color?
RC_NOCOLOR=${RC_NOCOLOR:-no}
# Can the terminal handle endcols?
RC_ENDCOL="yes"

#
# Default values for rc system
#
RC_TTY_NUMBER=11
RC_NET_STRICT_CHECKING="no"
RC_PARALLEL_STARTUP="no"
RC_USE_CONFIG_PROFILE="yes"

#
# Default values for e-message indentation and dots
#
RC_INDENTATION=''
RC_DEFAULT_INDENT=2
#RC_DOT_PATTERN=' .'
RC_DOT_PATTERN=''

# Override defaults with user settings ...
[ -f /etc/conf.d/rc ] && source /etc/conf.d/rc

# void import_addon(char *addon)
#
#  Import code from the specified addon if it exists
#
import_addon() {
	local addon=${svclib}/addons/$1
	if [[ -r ${addon} ]] ; then
		source "${addon}"
		return 0
	fi
	return 1
}

# void splash(...)
#
#  Notify bootsplash/splashutils/gensplash/whatever about
#  important events.
#
splash() {
	return 0
}
# This will override the splash() function...
if ! import_addon splash-functions.sh ; then
	[ -f /sbin/splash-functions.sh ] && source /sbin/splash-functions.sh
fi

# void profiling(...)
#
#  Notify bootsplash/whatever about important events.
#
profiling() {
	return 0
}
import_addon profiling-functions.sh

# void bootlog(...)
#
#  Notify bootlogger about important events.
bootlog() {
	return 0
}
import_addon bootlogger.sh

# void get_bootconfig()
#
#    Get the BOOTLEVEL and SOFTLEVEL by setting
#    'bootlevel' and 'softlevel' via kernel
#    parameters.
#
get_bootconfig() {
	local copt=
	local newbootlevel=
	local newsoftlevel=

	if [[ -r /proc/cmdline ]] ; then
		for copt in $(</proc/cmdline) ; do
			case "${copt%=*}" in
				bootlevel)
					newbootlevel=${copt##*=}
					;;
				softlevel)
					newsoftlevel=${copt##*=}
					;;
			esac
		done
	fi

	if [[ -n ${newbootlevel} ]] ; then
		export BOOTLEVEL=${newbootlevel}
	else
		export BOOTLEVEL="boot"
	fi

	if [[ -n ${newsoftlevel} ]] ; then
		export DEFAULTLEVEL=${newsoftlevel}
	else
		export DEFAULTLEVEL="default"
	fi

	return 0
}

setup_defaultlevels() {
	get_bootconfig

	if get_bootparam "noconfigprofile" ; then
		export RC_USE_CONFIG_PROFILE="no"

	elif get_bootparam "configprofile" ; then
		export RC_USE_CONFIG_PROFILE="yes"
	fi

	if [ "${RC_USE_CONFIG_PROFILE}" = "yes" -a -n "${DEFAULTLEVEL}" ] && \
	   [ -d "/etc/runlevels/${BOOTLEVEL}.${DEFAULTLEVEL}" -o \
	     -L "/etc/runlevels/${BOOTLEVEL}.${DEFAULTLEVEL}" ]
	then
		export BOOTLEVEL="${BOOTLEVEL}.${DEFAULTLEVEL}"
	fi

	if [ -z "${SOFTLEVEL}" ] ; then
		if [ -f "${svcdir}/softlevel" ] ; then
			export SOFTLEVEL="$(< ${svcdir}/softlevel)"
		else
			export SOFTLEVEL="${BOOTLEVEL}"
		fi
	fi

	return 0
}

# void get_libdir(void)
#
#    prints the current libdir {lib,lib32,lib64}
#
get_libdir() {
	if [ -n "${CONF_LIBDIR_OVERRIDE}" ] ; then
		CONF_LIBDIR="${CONF_LIBDIR_OVERRIDE}"
	fi
	echo ${CONF_LIBDIR:=lib}
}

# Wrapper function for i18n support
translate() {
    aux=${*}
    if test -f /etc/init.$LC_ALL
    then
        file=/etc/init.$LC_ALL

        value="$(grep "\"$aux\"" -n $file > /dev/null; if [ $? == 0 ]; then echo $(grep "$aux" -n $file | head -n `awk 'BEGIN{FS=":"}{print $1+1}'` $file |  tail -n 1 | awk 'BEGIN {FS="\""}{print $2}'); else echo $aux; fi)"

        # not translated
        if [ ! -z "$value" ]
        then
            aux=$value
        fi
    fi
}

# void esyslog(char* priority, char* tag, char* message)
#
#    use the system logger to log a message
#
esyslog() {
	local pri=
	local tag=

	if [ -x /usr/bin/logger ]
	then
		pri="$1"
		tag="$2"

		shift 2
		[[ -z "$*" ]] && return 0

		/usr/bin/logger -p "${pri}" -t "${tag}" -- "$*"
	fi

	return 0
}

# void eindent(int num)
#
#    increase the indent used for e-commands.
#
eindent() {
	local i=$1
	(( i > 0 )) || (( i = RC_DEFAULT_INDENT ))
	esetdent $(( ${#RC_INDENTATION} + i ))
}

# void eoutdent(int num)
#
#    decrease the indent used for e-commands.
#
eoutdent() {
	local i=$1
	(( i > 0 )) || (( i = RC_DEFAULT_INDENT ))
	esetdent $(( ${#RC_INDENTATION} - i ))
}

# void esetdent(int num)
#
#    hard set the indent used for e-commands.
#    num defaults to 0
#
esetdent() {
	local i=$1
	(( i < 0 )) && (( i = 0 ))
	RC_INDENTATION=$(printf "%${i}s" '')
}

# void einfo(char* message)
#
#    show an informative message (with a newline)
#
einfo() {
	einfon "$*\n"
	LAST_E_CMD=einfo
	return 0
}

# void einfon(char* message)
#
#    show an informative message (without a newline)
#
einfon() {
	[[ ${RC_QUIET_STDOUT} == yes ]] && return 0
	[[ ${RC_ENDCOL} != yes && ${LAST_E_CMD} == ebegin ]] && echo
	translate ${*}
	echo -ne " ${GOOD}*${NORMAL} ${RC_INDENTATION}${aux}"
	LAST_E_CMD=einfon
	return 0
}

# void ewarn(char* message)
#
#    show a warning message + log it
#
ewarn() {
	translate ${*}
	if [[ ${RC_QUIET_STDOUT} == yes ]]; then
		echo " ${aux}"
	else
		[[ ${RC_ENDCOL} != yes && ${LAST_E_CMD} == ebegin ]] && echo
		echo -e " ${WARN}*${NORMAL} ${RC_INDENTATION}${aux}"
	fi

	# Log warnings to system log
	esyslog "daemon.warning" "rc-scripts" "$*"

	LAST_E_CMD=ewarn
	return 0
}

# void eerror(char* message)
#
#    show an error message + log it
#
eerror() {
	translate ${*}
	if [[ ${RC_QUIET_STDOUT} == yes ]]; then
		echo " ${aux}" >/dev/stderr
	else
		[[ ${RC_ENDCOL} != yes && ${LAST_E_CMD} == ebegin ]] && echo
		echo -e " ${BAD}*${NORMAL} ${RC_INDENTATION}${aux}"
	fi

	# Log errors to system log
	esyslog "daemon.err" "rc-scripts" "$*"

	LAST_E_CMD=eerror
	return 0
}

# void ebegin(char* message)
#
#    show a message indicating the start of a process
#
ebegin() {
	local msg="$*" dots spaces=${RC_DOT_PATTERN//?/ }
	[[ ${RC_QUIET_STDOUT} == yes ]] && return 0

	einfon "${msg}"
	[[ ${RC_ENDCOL} == yes ]] && echo

	LAST_E_LEN=$(( 3 + ${#RC_INDENTATION} + ${#msg} ))
	LAST_E_CMD=ebegin
	return 0
}

# void _eend(int error, char *efunc, char* errstr)
#
#    indicate the completion of process, called from eend/ewend
#    if error, show errstr via efunc
#
#    This function is private to functions.sh.  Do not call it from a
#    script.
#
_eend() {
	local retval=${1:-0} efunc=${2:-eerror} msg
	shift 2

	if [[ ${retval} == 0 ]]; then
		[[ ${RC_QUIET_STDOUT} == yes ]] && return 0
		msg="${BRACKET}[ ${GOOD}ok${BRACKET} ]${NORMAL}"
	else
		if [[ -c /dev/null ]]; then
			rc_splash "stop" &>/dev/null &
		else
			rc_splash "stop" &
		fi
		if [[ -n "$*" ]]; then
			${efunc} "$*"
		fi
		msg="${BRACKET}[ ${BAD}!!${BRACKET} ]${NORMAL}"
	fi

	if [[ ${RC_ENDCOL} == yes ]]; then
		echo -e "${ENDCOL}  ${msg}"
	else
		[[ ${LAST_E_CMD} == ebegin ]] || LAST_E_LEN=0
		printf "%$(( COLS - LAST_E_LEN - 6 ))s%b\n" '' "${msg}"
	fi

	return ${retval}
}

# void eend(int error, char* errstr)
#
#    indicate the completion of process
#    if error, show errstr via eerror
#
eend() {
	local retval=${1:-0}
	shift

	_eend ${retval} eerror "$*"

	LAST_E_CMD=eend
	return $retval
}

# void ewend(int error, char* errstr)
#
#    indicate the completion of process
#    if error, show errstr via ewarn
#
ewend() {
	local retval=${1:-0}
	shift

	_eend ${retval} ewarn "$*"

	LAST_E_CMD=ewend
	return $retval
}

# v-e-commands honor RC_VERBOSE which defaults to no.
# The condition is negated so the return value will be zero.
veinfo() { [[ "${RC_VERBOSE}" != yes ]] || einfo "$@"; }
veinfon() { [[ "${RC_VERBOSE}" != yes ]] || einfon "$@"; }
vewarn() { [[ "${RC_VERBOSE}" != yes ]] || ewarn "$@"; }
veerror() { [[ "${RC_VERBOSE}" != yes ]] || eerror "$@"; }
vebegin() { [[ "${RC_VERBOSE}" != yes ]] || ebegin "$@"; }
veend() {
	[[ "${RC_VERBOSE}" == yes ]] && { eend "$@"; return $?; }
	return ${1:-0}
}
veend() {
	[[ "${RC_VERBOSE}" == yes ]] && { ewend "$@"; return $?; }
	return ${1:-0}
}

# char *KV_major(string)
#
#    Return the Major (X of X.Y.Z) kernel version
#
KV_major() {
	[[ -z $1 ]] && return 1

	local KV=$@
	echo ${KV%%.*}
}

# char *KV_minor(string)
#
#    Return the Minor (Y of X.Y.Z) kernel version
#
KV_minor() {
	[[ -z $1 ]] && return 1

	local KV=$@
	KV=${KV#*.}
	echo ${KV%%.*}
}

# char *KV_micro(string)
#
#    Return the Micro (Z of X.Y.Z) kernel version.
#
KV_micro() {
	[[ -z $1 ]] && return 1

	local KV=$@
	KV=${KV#*.*.}
	echo ${KV%%[^[:digit:]]*}
}

# int KV_to_int(string)
#
#    Convert a string type kernel version (2.4.0) to an int (132096)
#    for easy compairing or versions ...
#
KV_to_int() {
	[[ -z $1 ]] && return 1

	local KV_MAJOR=$(KV_major "$1")
	local KV_MINOR=$(KV_minor "$1")
	local KV_MICRO=$(KV_micro "$1")
	local KV_int=$(( KV_MAJOR * 65536 + KV_MINOR * 256 + KV_MICRO ))

	# We make version 2.2.0 the minimum version we will handle as
	# a sanity check ... if its less, we fail ...
	if [[ ${KV_int} -ge 131584 ]] ; then
		echo "${KV_int}"
		return 0
	fi

	return 1
}

# int get_KV()
#
#    Return the kernel version (major, minor and micro concated) as an integer.
#    Assumes X and Y of X.Y.Z are numbers.  Also assumes that some leading
#    portion of Z is a number.
#    e.g. 2.4.25, 2.6.10, 2.6.4-rc3, 2.2.40-poop, 2.0.15+foo
#
get_KV() {
	local KV=$(uname -r)

	echo $(KV_to_int "${KV}")

	return $?
}

# bool get_bootparam(param)
#
#   return 0 if pardus=param was passed to the kernel
#
#   EXAMPLE:  if get_bootparam "nodevfs" ; then ....
#
get_bootparam() {
	local x copt params retval=1

	[ ! -r "/proc/cmdline" ] && return 1

	for copt in $(< /proc/cmdline)
	do
		if [ "${copt%=*}" = "pardus" ]
		then
			params="$(gawk -v PARAMS="${copt##*=}" '
				BEGIN {
					split(PARAMS, nodes, ",")
					for (x in nodes)
						print nodes[x]
				}')"

			# Parse pardus option
			for x in ${params}
			do
				if [ "${x}" = "$1" ]
				then
#					echo "YES"
					retval=0
				fi
			done
		fi
	done

	return ${retval}
}

# Safer way to list the contents of a directory,
# as it do not have the "empty dir bug".
#
# char *dolisting(param)
#
#    print a list of the directory contents
#
#    NOTE: quote the params if they contain globs.
#          also, error checking is not that extensive ...
#
dolisting() {
	local x=
	local y=
	local tmpstr=
	local mylist=
	local mypath="$*"

	if [ "${mypath%/\*}" != "${mypath}" ]
	then
		mypath="${mypath%/\*}"
	fi

	for x in ${mypath}
	do
		[ ! -e "${x}" ] && continue

		if [ ! -d "${x}" ] && ( [ -L "${x}" -o -f "${x}" ] )
		then
			mylist="${mylist} $(ls "${x}" 2> /dev/null)"
		else
			[ "${x%/}" != "${x}" ] && x="${x%/}"

			cd "${x}"; tmpstr="$(ls)"

			for y in ${tmpstr}
			do
				mylist="${mylist} ${x}/${y}"
			done
		fi
	done

	echo "${mylist}"
}

# void save_options(char *option, char *optstring)
#
#    save the settings ("optstring") for "option"
#
save_options() {
	local myopts="$1"

	shift
	if [ ! -d "${svcdir}/options/${myservice}" ]
	then
		mkdir -p -m 0755 "${svcdir}/options/${myservice}"
	fi

	echo "$*" > "${svcdir}/options/${myservice}/${myopts}"

	return 0
}

# char *get_options(char *option)
#
#    get the "optstring" for "option" that was saved
#    by calling the save_options function
#
get_options() {
	if [ -f "${svcdir}/options/${myservice}/$1" ]
	then
		echo "$(< ${svcdir}/options/${myservice}/$1)"
	fi

	return 0
}

# char *add_suffix(char * configfile)
#
#    Returns a config file name with the softlevel suffix
#    appended to it.  For use with multi-config services.
add_suffix() {
	if [ "${RC_USE_CONFIG_PROFILE}" = "yes" -a -e "$1.${DEFAULTLEVEL}" ]
	then
		echo "$1.${DEFAULTLEVEL}"
	else
		echo "$1"
	fi

	return 0
}

# char *get_base_ver()
#
#    get the version of baselayout that this system is running
#
get_base_ver() {
	[[ ! -r /etc/pardus-release ]] && return 0
	local ver=$(</etc/pardus-release)
	echo ${ver##* }
}

# Network filesystems list for common use in rc-scripts.
# This variable is used in is_net_fs and other places such as
# localmount.
NET_FS_LIST="afs cifs coda davfs gfs ncpfs nfs nfs4 shfs smbfs"

# bool is_net_fs(path)
#
#   return 0 if path is the mountpoint of a networked filesystem
#
#   EXAMPLE:  if is_net_fs / ; then ...
#
is_net_fs() {
	local fstype
	# /proc/mounts is always accurate but may not always be available
	if [[ -e /proc/mounts ]]; then
		fstype=$( sed -n -e '/^rootfs/!s:.* '"$1"' \([^ ]*\).*:\1:p' /proc/mounts )
	else
		fstype=$( mount | sed -n -e 's:.* on '"$1"' type \([^ ]*\).*:\1:p' )
	fi
	[[ " ${NET_FS_LIST} " == *" ${fstype} "* ]]
	return $?
}

# bool is_uml_sys()
#
#   return 0 if the currently running system is User Mode Linux
#
#   EXAMPLE:  if is_uml_sys ; then ...
#
is_uml_sys() {
	grep -qs 'UML' /proc/cpuinfo
	return $?
}

# bool is_vserver_sys()
#
#   return 0 if the currently running system is a Linux VServer
#
#   EXAMPLE:  if is_vserver_sys ; then ...
#
is_vserver_sys() {
	grep -qs '^s_context:[[:space:]]*[1-9]' /proc/self/status
	return $?
}

# bool is_xenU_sys()
#
#   return 0 if the currently running system is an unprivileged Xen domain
#
#   EXAMPLE:  if is_xenU_sys ; then ...
#
is_xenU_sys() {
	[[ -d /proc/xen && ! -f /proc/xen/privcmd ]]
}

# bool get_mount_fstab(path)
#
#   return the parameters to pass to the mount command generated from fstab
#
#   EXAMPLE: cmd=$( get_mount_fstab /proc )
#            cmd=${cmd:--t proc none /proc}
#            mount -n ${cmd}
#
get_mount_fstab() {
	awk '$1 ~ "^#" { next }
	     $2 == "'$*'" { if (found++ == 0) { print "-t "$3,"-o "$4,$1,$2 } }
	     END { if (found > 1) { print "More than one entry for '$*' found in /etc/fstab!" > "/dev/stderr" } }
	' /etc/fstab
}

# char *reverse_list(list)
#
#   Returns the reversed order of list
#
reverse_list() {
	for (( i = $# ; i > 0 ; --i )); do
		echo -n "${!i} "
	done
}

# void start_addon(addon)
#
#   Starts addon.
#
start_addon() {
	local addon=$1
	(import_addon ${addon}-start.sh)
	return 0
}

# void start_volumes()
#
#   Starts all volumes in RC_VOLUME_ORDER.
#
start_volumes() {
	local x=

	for x in ${RC_VOLUME_ORDER}; do
		start_addon "${x}"
	done

	return 0
}

# void stop_addon(addon)
#
#   Stops addon.
#
stop_addon() {
	local addon=$1
	(import_addon ${addon}-stop.sh)
	return 0
}

# void stop_volumes()
#
#   Stops all volumes in RC_VOLUME_ORDER (reverse order).
#
stop_volumes() {
	local x=

	for x in $(reverse_list ${RC_VOLUME_ORDER}); do
		stop_addon "${x}"
	done

	return 0
}

# bool is_older_than(reference, files/dirs to check)
#
#   return 0 if any of the files/dirs are newer than
#   the reference file
#
#   EXAMPLE: if is_older_than a.out *.o ; then ...
is_older_than() {
	local x=
	local ref="$1"
	shift

	for x in "$@" ; do
		[[ ${x} -nt ${ref} ]] && return 0

		if [[ -d ${x} ]] ; then
			is_older_than "${ref}" "${x}"/* && return 0
		fi
	done

	return 1
}


##############################################################################
#                                                                            #
# This should be the last code in here, please add all functions above!!     #
#                                                                            #
# *** START LAST CODE ***                                                    #
#                                                                            #
##############################################################################

if [ -z "${EBUILD}" ] ; then
	# Setup a basic $PATH.  Just add system default to existing.
	# This should solve both /sbin and /usr/sbin not present when
	# doing 'su -c foo', or for something like:  PATH= rcscript start
	PATH="/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/sbin:${PATH}"

	if [ "$(/sbin/consoletype 2> /dev/null)" = "serial" ] ; then
		# We do not want colors/endcols on serial terminals
		RC_NOCOLOR="yes"
		RC_ENDCOL="no"
	fi

	for arg in "$@" ; do
		case "${arg}" in
			# Lastly check if the user disabled it with --nocolor argument
			--nocolor|-nc)
				RC_NOCOLOR="yes"
				;;
		esac
	done

	if [ -r "/proc/cmdline" ] ; then
		setup_defaultlevels
	fi
else
	# Should we use colors ?
	if [[ $* != *depend* ]]; then
		# Check user pref in portage
		[ "${RC_NOCOLOR}" = "true" ] && RC_NOCOLOR="yes"
	else
		RC_NOCOLOR="yes"
		RC_ENDCOL="no"
	fi
fi

if [[ -n ${EBUILD} && $* == *depend* ]]; then
	COLS=80
else
	# Setup COLS and ENDCOL so eend can line up the [ ok ]
	COLS=${COLUMNS:-0}		# bash's internal COLUMNS variable
	(( COLS == 0 )) && COLS=$(stty size 2>/dev/null | cut -d' ' -f2)
	(( COLS > 0 )) || (( COLS = 80 ))	# width of [ ok ] == 7
fi

if [[ ${RC_ENDCOL} == yes ]]; then
	ENDCOL=$'\e[A\e['$(( COLS - 7 ))'G'
else
	ENDCOL=''
fi

# Setup the colors so our messages all look pretty
if [[ ${RC_NOCOLOR} == yes ]]; then
	unset GOOD WARN BAD NORMAL HILITE BRACKET
else
	GOOD=$'\e[32;01m'
	WARN=$'\e[33;01m'
	BAD=$'\e[31;01m'
	NORMAL=$'\e[0m'
	HILITE=$'\e[36;01m'
	BRACKET=$'\e[34;01m'
fi

##############################################################################
#                                                                            #
# *** END LAST CODE ***                                                      #
#                                                                            #
# This should be the last code in here, please add all functions above!!     #
#                                                                            #
##############################################################################


# vim:ts=4
