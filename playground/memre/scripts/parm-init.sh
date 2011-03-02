#!/bin/bash
#
#  Copyright (C) 2010 TUBITAK BILGEM
#  Pardus Linux Project
#  ARM Architecture Sysroot and Buildfarm Preparator
#
#  Author: Mehmet Emre Atasever <memre ~ pardus.org.tr>
#
#  Tester and reviewer:
#          Renjith Gopinadhan <renjithg ~ pearlsoft.in>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation; either version 2 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
######################################################################
#
#  Test environment:
#   * Beagleboard which contains armv7l based Cortex-a8
#   * Pardus Corporate 2
#   * PiSi from memre's playground
#     - https://svn.pardus.org.tr/uludag/trunk/playground/memre/pisi
#       Release: 34138
#
# TODO:
# - sd card flasher support
# - beagle nandflash writer
# - If packages installed, do not emerge them.
#
######################################################################

# Trap all signals for more control
set -e
trap sighandler 1 2 3 6

# Start time for logging and printing
cur_time() { date +%0s%0N; } # prints the current time as nanoseconds
_start_time=$(cur_time)

# for printing time info in logger
_b_print_time=false

# some options for this script
# _b -> boolean value
_b_install_toolchain=true          # if true, then install toolchain
_b_install_sysroot=true            # if true, then use sysroot in the toolchain,
                                   # TODO:    else
_b_enable_colors=true  # colors are enabled by default
_b_force_yes=false     # if true, then don't ask any questions to user, use defaults.
_b_skip_pisi=false     # if true, then don't install pisi in memre's playground.
_b_skip_sbox2=false    # if true, then don't emerge sbox2
_b_skip_farm=true      # if true, then don't install and prepare buildfarm
_b_print_time=false    # if true, then print time at the screen

# log levels, also print levels.
# if LOG_LEVEL is equal or grater than the level, then it is
# also printed to the screen
#
# see log function for details.
_log_level_any=0   # neccessary stuff titles etc.
_log_level_err=1   # error messages
_log_level_warn=2  # add warning messages
_log_level_info=3  # add info messages
_log_level_debug=4 # add some debug messages

# Progress bar animation \ | / -
_prog_bar=( '\\' '|' '/' '-' )
_prog_bar_index=0

######################################################################
# Distro options and architecture settings

# Rootfs for initial ARM sysroot, this rootfs installs into sysroot
# directory before ARM buildfarm starts.
# FIXME: prepare one.
# rootfs_url="http://cekirdek.pardus.org.tr/~memre/pardus-arm/sd-image/pardus-arm_beagleboard_rootfs.tar.bz2"
# rootfs_sha1sum="df5b9c03cff1a2c000ad35978c83f5dade7e5daf"
# rootfs="`echo ${rootfs_url} | awk -F/ '{print $NF}'`"

# If another architecture other than armv7l is wanted, then
# change this $ARCH variable (and toolchain and *flags)
#
# Note that its all faults is your own responsibility
ARCH=${ARCH:-"armv7l"}

# Contains Cross build sysroot and repository directories
CROSS=${CROSS:-"/var/cross"}

# A temporary rootfs for building packages. This SYSROOT is using for
# build-time dependencies (generally required libraries) for packages.
SYSROOT=${SYSROOT:-"${CROSS}/sysroots/${ARCH}"}

# Toolchain directory. Remember that, we will add this directory in our
# PATH variable: PATH=${TOOLCHAIN_DIR}/bin:$PATH
TOOLCHAIN_UP_DIR="/opt/toolchain"
TOOLCHAIN_DIR=${TOOLCHAIN_DIR:-"${TOOLCHAIN_UP_DIR}/${ARCH}"}

# A log file for testing this script
LOG_FILE=${LOG_FILE:-"${CROSS}/pardus-${ARCH}.log"}

# Log level for printing logs to the screen
LOG_LEVEL=${LOG_LEVEL:-${_log_level_info}}

# Directory for downloaded tarballs
TARBALL_DIR=${TARBALL_DIR:-"${CROSS}/tarballs"}

# Temp directory
TMP_DIR=${TMP_DIR:-"${CROSS}/tmp"}

# pisi commands for cross and native platforms.
#
# For example, if pisi-armv7l is executed, pisi
# uses pisi-armv7l.conf configuration file.
_pisi_native="/usr/bin/pisi"
_pisi_cross="/usr/bin/pisi-${ARCH}"
_pisi_cross_conf="/etc/pisi/pisi-${ARCH}.conf"

# We need qemu for scratchbox2 builds
_qemu="qemu-arm"
# svn command for check out latest PiSi and Buildfarm from uludag repository
_svn="svn"

# if the environmental variables didnt defined, take it from lsb_release command
DISTRIB_ID=${DISTRIB_ID:-`lsb_release -i | cut -d: -f2 | tr -d '\t'`}
DISTRIB_RELEASE=${DISTRIB_RELEASE:-`lsb_release -r | cut -d: -f2 | tr -d '\t'`}
DISTRIB_DESCRIPTION=${DISTRIB_DESCRIPTION:-`lsb_release -d | cut -d: -f2 | tr -d '\t'`}
DISTRIB_CODENAME=${DISTRIB_CODENAME:-`lsb_release -c | cut -d: -f2 | tr -d '\t'`}

# dialog interface
_dialog_back_title="${DISTRIB_ID}${DISTRIB_RELEASE} ARM Sysroot Preparator"
_dialog_width=80
_dialog_height=20

# dialog colors
_dialog_cl_normal="\Zn"
_dialog_cl_reverse="\Zr"
_dialog_cl_noreverse="\ZR"
_dialog_cl_bold="\Zb"
_dialog_cl_nobold="\ZB"
_dialog_cl_underline="\Zu"
_dialog_cl_nounderline="\ZU"
_dialog_cl_black="\Z0"
_dialog_cl_red="\Z1"
_dialog_cl_green="\Z2"
_dialog_cl_yellow="\Z3"
_dialog_cl_blue="\Z4"
_dialog_cl_magenta="\Z5"
_dialog_cl_cyan="\Z6"
_dialog_cl_white="\Z7"

# Source repo for building PiSi packages from source codes
SRC_REPO="http://svn.pardus.org.tr/pardus/playground/memre/${ARCH}/${DISTRIB_ID}"
SRC_REPO_NAME="${DISTRIB_ID}_src"
SRC_REPO_INDEX="/var/lib/buildfarm/repositories/${DISTRIB_ID}${DISTRIB_RELEASE}/devel/pisi-index.xml"

# This repo contains pre-built binary packages
BIN_REPO="http://cekirdek.pardus.org.tr/~memre/pardus-arm/${ARCH}/${BIN_REPO}"
BIN_REPO_NAME="${DISTRIB_ID}_bin"
BIN_REPO_INDEX="http://cekirdek.pardus.org.tr/~memre/pardus-arm/${ARCH}/${BIN_REPO}/pisi-index.xml.xz"

# This repo contains packages which compiled by buildfarm
FARM_REPO="/var/db/buildfarm/packages/${DISTRIB_ID}${DISTRIB_RELEASE}/devel/${ARCH}"
FARM_REPO_NAME="${DISTRIB_ID}_farm"
FARM_REPO_INDEX="/var/db/buildfarm/packages/${DISTRIB_ID}${DISTRIB_RELEASE}/devel/${ARCH}/pisi-index.xml"

######################################################################
# Toolchain options

TOOLCHAIN_URL="http://cekirdek.pardus.org.tr/~memre/parm/${ARCH}/${DISTRIB_ID}${DISTRIB_RELEASE}/${DISTRIB_ID}${DISTRIB_RELEASE}-${ARCH}-toolchain.tar.xz"
TOOLCHAIN_TARBALL="`echo ${TOOLCHAIN_URL} | awk -F/ '{print $NF}'`"

# export HOST=${HOST:-"`gcc -dumpmachine`"}
export HOST=${HOST:-"arm-pardus-linux-gnueabi"}
# export STRIP=${STRIP:-"${HOST}-strip"}
# export OBJCOPY=${OBJCOPY:-"${HOST}-objcopy"}
# export OBJDUMP=${OBJDUMP:-"${HOST}-objdump"}
# export RANLIB=${RANLIB:-"${HOST}-ranlib"}
# export AR=${AR:-"${HOST}-ar"}
# export AS=${AS:-"${HOST}-as"}
# export CPP=${CPP:-"${HOST}-gcc -E"}
# export CC=${CC:-"${HOST}-gcc"}
# export CXX=${CXX:-"${HOST}-g++"}
# export LD=${LD:-"${HOST}-ld"}


# FIXME: get these values from a config file.
# flags for target ${ARCH} platform, default optimized for cortex-a8
export CPPFLAGS=${CPPFLAGS:-"-isystem${SYSROOT}/usr/include"}
export CFLAGS=${CFLAGS:-"-march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -g3 -ggdb -funwind-tables -fasynchronous-unwind-tables"}
export CXXFLAGS=${CXXFLAGS:-"-march=armv7-a -mtune=cortex-a8 -mfpu=neon -mfloat-abi=softfp -pipe -fexpensive-optimizations -fomit-frame-pointer -frename-registers -O2 -g3 -ggdb -fpermissive -fvisibility-inlines-hidden -funwind-tables -fasynchronous-unwind-tables"}
export LDFLAGS=${LDFLAGS:-"-Wl,-O1 -Wl,-z,relro -Wl,--hash-style=gnu -Wl,--as-needed -Wl,--sort-common"}

export BUILD_ARCH=`uname -m`
export BUILD=`gcc -dumpmachine`

export PATH=${TOOLCHAIN_DIR}/bin:$PATH

######################################################################
# Logging and printing options

# gives verbose parameter to all applications `-v'
# default: "v"
VERBOSE="v"

# gives debug parameter to pisi, this is not same with _log_level_debug
# if you dont set log level as debug, debug data will just be logged
DEBUG="d"

# takes --ignore-check parameter to pisi,
# default yes
PISI_IGNORE_CHECK="--ignore-check"

# fifo for logging, this is a workaround of bash pipe operation
# we often use this fifo for logging
_log_fifo="${TMP_DIR}/.pardus_${ARCH}_logfifo"

# backup suffix
_backup_suffix=$(date +%Y%m%d_%H%M)

##################################
# @func: set_colors
# @desc: sets colors if user wants
#
set_colors()
{
    export _clNoColor="\e[0m"
    export _clWhite="\e[1;37m"
    export _clYellow="\e[1;33m"
    export _clCyan="\e[0;36m"
    export _clBlack="\e[0;30m"
    export _clBlue="\e[0;34m"
    export _clGreen="\e[0;32m"
    export _clCyan="\e[0;36m"
    export _clRed="\e[0;31m"
    export _clPurple="\e[0;35m"
    export _clBrown="\e[0;33m"
    export _clLightGray="\e[0;37m"
    export _clLightPurple="\e[1;35m"
    export _clLightRed="\e[1;31m"
    export _clLightCyan="\e[1;36m"
    export _clLightGreen="\e[1;32m"
    export _clLightBlue="\e[1;34m"
    export _clDarkGray="\e[1;30m"

    export _clInfo=${_clWhite}
    export _clError=${_clRed}
    export _clWarning=${_clYellow}
    export _clHead=${_clLightPurple}
    export _clQuestion=${_clCyan}
    export _clUserAnswer=${_clNoColor}
    export _clTime=${_clBrown}

    # Title colors
    export _clTitle1=${_clLightGreen}
    export _clTitle2=${_clLightCyan}
    export _clTitle3=${_clLightBlue}

    # Title Numbers
    export _tn1=0  # Main title [X]
    export _tn2=0  # 2nd title  [1.X]
    export _tn3=0  # 3rd title  [1.2.X]
}

##################################
# @func: sighandler
# @desc: when an exception caught, this function cleans up the
#        shits we left behind us.
sighandler()
{
    local head="$(toupper ${FUNCNAME})"

    print_err "An exception caught! Terminating..." "${head}"
    cleanup

    exit 1
}

##################################
# @func: cleanup
# @desc: for cleaning up the temp directories and unneccessary stuffs.
cleanup()
{
    local head="$(toupper ${FUNCNAME})"

    print_info "Cleaning up..." "${head}"

    # FIXME: kill all working stuff

    echo # new line
    # Wait for a while
    for i in 1 2 3; do
        echo -n '.'
        sleep 1
    done
    echo

    # FIXME: clean up the shits behind of you.
    print_info "Cleaning done." "${head}"
}

######################################################################
# Printing functions

##################################
# @func: print
# @desc: prints the message to the console. There is NO newline.
#        this function does not logging the message.
#
# @param*: message
print()
{
    # print something without newline
    echo -en "$*${_clNoColor}";
}

##################################
# @func: println
# @desc: prints the message to the console.
#        this function does not logging the message.
#
# @param*: message
println()
{
    # print something with newline
    echo -e "$*${_clNoColor}"
}

##################################
# @func: prep_log
# @desc: prepares logger to get logs from fifo
#
# @usage:
#         prep_log &
#         ls <dir> > ${_log_fifo} 2>&1
#         __r=$? # return value of ls
#         wait
#         if [ ${__r} -ne 0 ]; then die "yoh la boyle bi dizin.."; fi
prep_log()
{
    # run in background, since the next command will give us log ;)
    cat ${_log_fifo} | log ${_log_level_debug}
}

##################################
# @func: log
# @desc: logs message to $LOG_FILE.
#
# @param1: LOG_LEVEL
# @param*: message comes from stdin
#
# @usage1: echo " [${FUNCNAME}] bu anam icin" | log ${_log_level_warn}
# @usage2: log ${_log_level_warn} "another message from me to you: (O)))"
log()
{
    local CR=$(printf "\n")
    local log_level=$1
    shift # other parameters are message

    # if log entered with pipe
    if [ $# -eq 0 ]; then
        cat -
    else
        # if log entered as parameter
        printf "%s\n" "$*"
    fi | (
        while IFS=${CR} read line; do # just newlines seperates the line
            local debug_out="/dev/null" # do not print to the console as default
            local current_time="[${_clTime}$(elapsed_time)${_clNoColor}]"
            local message=

            # if LOG_LEVEL is equal or grater than the log_level, which
            # is given from the function, then print this log to the console as well.
            #
            # this is good with debugging, but end user needn't to see
            # all the outputs.
            [ ${LOG_LEVEL} -ge ${log_level} ] && debug_out="/proc/self/fd/1"

            # if user want to see timer, then print it, otherwise just log it.
            ${_b_print_time} && \
                message="${current_time} " || \
                print "${current_time} " >> ${LOG_FILE}

            # if there are just blanks, remove the timer and animation
            [ -z "$(echo -n ${line})" ] && print "          \r"

            message="${message}${line}"

            println "${message}" | tee -a ${LOG_FILE} > ${debug_out} 2>&1

            echo -ne "${current_time} ${_prog_bar[$((_prog_bar_index/5))]} \r"
            _prog_bar_index=$(( (_prog_bar_index + 1) % 20 ))
        done
    ) # END OF LOGGING
}

##################################
# @func: elapsed_time
# @desc: prints elapsed time since this script started
#
# @param1: start_time (optinal, if $1="" then use global _start_time)
# @param2: nanosecond level (optinal)
#
# @usage: echo "$(elapsed_time)"
elapsed_time()
{
    local current_time=$(cur_time)
    local start_time=${1:-${_start_time}}

    local nsecs_passed=$(( current_time - start_time ))

    local nsecs=$((  nsecs_passed %    1000000000 ))
    local secs=$((  (nsecs_passed /    1000000000) % 60 ))
    local mins=$((   nsecs_passed /   60000000000 ))
    local hours=$((  nsecs_passed / 3600000000000 ))

    if [ x"$2" != x"fancy" ]; then
        printf "%02d:%02d" ${mins} ${secs}
    else
        printf "%02d mins %02d.%04d secs." ${mins} ${secs} ${nsecs}
    fi
}

##################################
# @func: print_info
# @desc: prints info message with _clInfo color
#
# @param1: message
# @param2: head
print_info()
{
    # info messages with newline
    local head=$2
    local message="${_clHead}${head}${_clInfo} ${1}"

    println "${message}" | log "${_log_level_info}"
}

##################################
# @func: print_err
# @desc: prints error message with _clError color
#
# @param1: message
# @param2: head
print_err()
{
    local head=$2
    local message="${_clHead}${head}${_clError} E: ${1}"

    println "${message}" | log "${_log_level_err}"
}

##################################
# @func: print_warn
# @desc: prints warning message with _clWarning color
#
# @param1: message
# @param2: head
print_warn()
{
    local head=$2
    local message="${_clHead}${head}${_clWarning} W: ${1}"

    println "${message}" | log "${_log_level_warn}"
}

##################################
# @func: print_t1
# @desc: prints title
#        This subtitle prints like this:
#         1) [this function]
#         ^
#           1.1) print_t2
#             1.1.1) print_t3
#           1.2) print_t2
#         2) [this function]
#         ^
#           2.1) print_t2
#             2.1.1) print_t3
#             2.1.2) print_t3
#
#         Automatically increses _tn1 and sets _tn2 and _tn3 as 0.
#
# @param*: title text
print_t1()
{
    # main title message,
    #  set the subtitle numbers as 0
    _tn1=$((${_tn1} + 1))
    _tn2="0"
    _tn3="0"

    local message=" ${_clTitle1}${_tn1}) $*"

    println "${message}" | log "${_log_level_any}"
}

##################################
# @func: print_t2
# @desc: prints subtitle 2
#        This subtitle prints like this:
#         1) print_t1
#         1.1) [this function]
#           ^
#         1.1.1) print_t3
#         1.1.2) print_t3
#         1.2) [this function]
#           ^
#         1.2.1) print_t3
#         1.2.2) print_t3
#
#         Increses _tn2 and sets _tn3 as 0.
#
# @param*: title text
print_t2()
{
    # title 2 [1.X]
    _tn2=$((${_tn2} + 1))
    _tn3="0"

    local message=" ${_clTitle2}${_tn1}.${_tn2}) $*"

    println "${message}" | log "${_log_level_any}"
}

##################################
# @func: print_t3
# @desc: prints subtitle 3
#        This subtitle prints like this:
#         1) print_t1
#         1.1) print_t2
#         1.1.1) [this function]
#             ^
#         1.1.2) [this function]
#             ^
#         Increses _tn3.
#
# @param*: title text
print_t3()
{
    # title 3 [1.2.X]
    _tn3=$(($_tn3 + 1))

    local message=" ${_clTitle3}${_tn1}.${_tn2}.${_tn3}) $*"

    println "${message}" | log "${_log_level_any}"
}

##################################
# @func: die
# @desc: terminates script for an error
#
# @param1: message to be printed
# @param2: head
die()
{
    local head=$2

    print_err "$1" "${head}"
    print_err "Build script is terminated! Removing temporary files and directories.
See log file \`${LOG_FILE}' for details.

If you think that this is a bug, then open a bug report to
http://bugs.pardus.org.tr and add ${LOG_FILE} as attattachment." "DIE:${head}"

    # cleanup

    exit 1 # byby cruel world
}

##################################
# @func: toupper
# @desc: converts the parameters uppercase
#
# @param*: message
toupper()
{
    local message="$*"

    echo "`echo $* | tr '[:lower:]' '[:upper:]'`"
}

##################################
# @func: dialog_
# @desc: manages dialog for helping other functions
#
# @param1: operation (eg. message-box, yesno dialog etc..)
# @param2: title
# @param3: text
#
# @param4: extra_param (if any, not mendatory)
#
# @usage:
#        dialog_ msgbox "welcome to parm init."
#        dialog_ yesno "Would you like to go on?" "really?" "--defaultno"
#
dialog_()
{
    local operation="$1"
    local title="$2"
    local text="$3"
    local extra_param="$4"
    local cmd="dialog --cr-wrap --colors "
    local ret_val=0

    # if user run this script with force-yes, then do not show dialog
    # boxes
    case ${operation} in
        msgbox)
            ${_b_force_yes} || ${cmd} \
                --backtitle "${_dialog_back_title}" \
                --title "${title}" \
                ${extra_param} \
                --msgbox "${text}" "-1" "-1"
            ret_val=$?
            echo -e " ==> DIALOG Message Box\n${text}\n\n ==> DIALOG --" | \
                sed -e 's/\\Z[bBuUrRnN01234567]//g' | \
                log ${_log_level_debug}

            ;;

        yesno)
            ${_b_force_yes} || ${cmd} \
                --backtitle "${_dialog_back_title}" \
                --title "${title}" \
                ${extra_param} \
                --yesno "${text}" "-1" "-1"
            ret_val=$?

            local user_answer=
            [ ${ret_val} -eq 0 ] && echo "yes" || echo "No"

            echo -e " ==> DIALOG YesNo Dialog Box\n${text} ==> DIALOG User answer: \"${user_answer}\"\n ==> DIALOG --" | \
                sed -e 's/\\Z[bBuUrRnN01234567]//g' | \
                log ${_log_level_debug}

            ;;

    esac

    # after dialog exits, it leaves a dirty blue screen behind of it, grrr.
    # It's best to go on with a clean page after dialog.
    clear

    return ${ret_val}
}

##################################
# @func: ask
# @desc: asks the question with a dialog and returns the answer
#
# @param1: message to be printed
# @param2: head
ask()
{
    local title=$1
    local message=$2
    local extra_param=$3

    dialog_ "yesno" "${title}" "${message}" "${extra_param}"
    return $?
}

##################################
# @func: pisi_
# @desc: uses native or cross pisi and logs the outputs to ${LOG_FILE}
#
# @param1: native or cross
# @param2: operation (same as pisi: it, up, em, bi, ..)
#
# @param-: other parameters depends on the operation.
#
# @usage:
#          pisi_ cross it heyya-hey
#          pisi_ native it -c games
#          pisi_ c em busybox
#          pisi_ c emerge glib2
#          pisi_ native update-repo
pisi_()
{
    local head="PISI"

    local system=$1      # refers cross or native
    local operation=$2   # refers which operation will be performed
    local pisi_cmd=      # refers the pisi command (native or cross)

    # Native or cross pisi, make your choice
    case ${system} in
        n|native)
          pisi_cmd=${_pisi_native}
          system="native"
          ;;

        c|cross)
          pisi_cmd=${_pisi_cross}
          system="${ARCH}"
          ;;

        *)
          die "Hmm, another \`build stayla'. Please let us know what this is.." "${head}"
          ;;
    esac

    # pisi operation
    case ${operation} in
        ur|update-repo)
            # update native or cross repositories
            # no more parameters
            print_info " ==> Updating ${system} repositories..." "${head}"

            prep_log &
            (${pisi_cmd} ur -y${VERBOSE}${DEBUG} > ${_log_fifo} 2>&1)
            __r=$?; wait

            [ ${__r} -eq 0 ] || die "Unable to update ${system} repositories!" "${head}"

            ;;

        up|upgrade)
            # upgrade native or cross repositories
            # no more parameters
            print_info " ==> Upgrading ${system} system..." "${head}"

            prep_log &
            (${pisi_cmd} up -y${VERBOSE}${DEBUG} > ${_log_fifo} 2>&1)
            __r=$?; wait

            [ ${__r} -eq 0 ] || die "Unable to upgrade ${system} system!" "${head}"

            ;;

        it|install)
            # @param3 packages
            # @param4 extra_parameters
            local packages=$3
            local extra_parameters="$4"

            print_info " ==> Installing \"${packages}\" to ${system} system..." "${head}"

            prep_log &
            (${pisi_cmd} it -y${VERBOSE}${DEBUG} ${extra_parameters} ${packages} > ${_log_fifo} 2>&1)
            __r=$?; wait

            [ ${__r} -eq 0 ] || die "Unable to install \"${packages}\" to ${system} system!" "${head}"

            ;;

        bi|build)
            # @param3 package_name
            # @param4 package_url (may be remote or a local file)
            # @param5 extra_parameters
            local package_name="$3"
            local package_url="$4"
            local extra_parameters="$5"
            local pspec="${package_url}/${package_name}/pspec.xml"

            print_info " ==> Building \"${package_name}\" for ${system} system..." "${head}"

            local start_=$(cur_time)
            prep_log &
            (${pisi_cmd} bi -y${VERBOSE}${DEBUG} ${PISI_IGNORE_CHECK} ${extra_parameters} ${pspec} > ${_log_fifo} 2>&1)
            __r=$?; wait

            [ ${__r} -eq 0 ] || die "Unable to build \"${package_name}\" to ${system} system!" "${head}"

            print_info "    * \"${package_name}\" built in $(elapsed_time ${start_} fancy)" "${head}"

            ;;

        em|emerge)
            # @param3 packages
            # @param4 extra_parameters
            local packages="$3"
            local extra_parameters="$4"

            print_info " ==> Emerging \"${packages}\" to ${system} system..." "${head}"

            start_=$(cur_time)
            prep_log &
            (${pisi_cmd} em -y${VERBOSE}${DEBUG} ${PISI_IGNORE_CHECK} ${extra_parameters} ${packages} > ${_log_fifo} 2>&1)
            __r=$?; wait

            [ ${__r} -eq 0 ] || die "Unable to emerge \"${packages}\" to ${system} system!" "${head}"

            print_info "    * \"${packages}\" emerged in $(elapsed_time ${start_} fancy)" "${head}"

            ;;

        ar|add-repo)
            # @param3 Repository name (eg. corp2-test)
            # @param4 Repository url (eg. http://packages.pardus.org.tr/pardus/corporate2/devel/x86_64/pisi-index.xml.xz)
            local repo_name=$3
            local repo_url=$4

            # repos=`cat ${SYSROOT}/var/lib/pisi/info/repos | \
            #        grep Name | \
            #        cut -d\> -f2 | \
            #        cut -d\< -f1 | \
            #        tr '\n' ' '`

            print_info " ==> Adding \"${repo_name}\":\"${repo_url}\" to ${system} system}..." "${head}"
            prep_log &
            (${pisi_cmd} ar -y${VERBOSE}${DEBUG} ${repo_name} ${repo_url} > ${_log_fifo} 2>&1)
            __r=$?; wait

            [ ${__r} -eq 0 ] || (
                # actually, this should be "die"
                print_err "Unable to add repo \"${repo_name}\" \"${repo_url}\"" "${head}";
                return 1;
            )

            ;;

        ix|index)
            # NO parameters
            print_info " ==> Creating pisi-index" "${head}"
            prep_log &
            (${pisi_cmd} ix -y${VERBOSE}${DEBUG} --skip-signing > ${_log_fifo} 2>&1)
            __r=$?; wait

            [ ${__r} -eq 0 ] || (
                print_err "Unable to create pisi-index!" "${head}";
                return 1;
            )

            ;;

         *)
            die "There is no such operation called \"${operation}\"!" "${head}"
            ;;

    esac
}

##################################
# @func: checksum
# @desc: checks the tarballs with sha1sum
#
# @param1: tarball in filesystem
checksum()
{
    local head="CHECKSUM"

    local tarball=$1
    local sum=`cat ${tarball}.sha1sum | cut -d' ' -f1`

    # if there is no sha1sum file, then refetch it!
    [ -e "${tarball}.sha1sum" ] || (
        rm_ ${tarball}
        return 2 # fail, refetch
    )

    if [ -e "${tarball}" ]; then
        [ x"`sha1sum ${tarball} | cut -d' ' -f1`" == x"${sum}" ] && \
            return 0 # sum is good.

        if [ -e "${tarball}.aria2" ]; then
            return 3 # there is a downloaded image and can be proceeded
        else
            print_warn "Removing bad \"${tarball}\" image!" "${head}"
            rm_ ${tarball}
            return 2 # fail, refetch
        fi
    fi

    return 1 # no archive, fetch it.
}

##################################
# @func: fetch
# @desc: fetches something from net
#
# @param1: tarball description name for printing log (eg. toolchain)
# @param2: tarball full name (eg. PardusCorporate2-armv7l-toolchain.tar.xz)
# @param3: download link of the tarball (eg. http://hede.hodo/PardusCorporate2-armv7l-toolchain.tar.xz)
fetch()
{
    local head="FETCH"

    local name=$1
    local tarball=$2
    local download_link=$3
    local current_dir=$(pwd)

    cd ${TARBALL_DIR}
    if checksum ${tarball} ; then
        print_info "\"${name}\" is already fetched!" "${head}"
        return 0
    fi

    print_info " ==> Fetching \"${name}\"..." "${head}"
    prep_log &
    ( aria2c -c ${download_link} ${download_link}.sha1sum > ${_log_fifo} 2>&1 )
    __r=$?; wait

    # Is there any connection problem?
    [ ${__r} -eq 0 ] || (
        print_err "\"${name}\" cannot be fetched!" "${head}"
        return 1
    )

    # Check sha1sum
    if ! checksum ${tarball} ; then
        print_err "Downloaded image \"${tarball}\" is bad!" "${head}"
        rm_ ${tarball}
        return 2
    fi

    cd ${current_dir}

    return 0
}

##################################
# @func: extract
# @desc: extracts tarballs (@param2) (in ${TARBALL_DIR} directory)
# to given directory (@param3)
#
# @param1: tarball description name for printing log (eg. toolchain)
# @param2: tarball full name (eg. PardusCorporate2-armv7l-toolchain.tar.xz)
# @param3: destinationdirectory directory for tarball
extract()
{
    local head="EXTRACT"

    local ret_val=0

    local name=$1
    local tarball=$2
    local target=$3

    print_info " ==> Extracting \"${name}\" into \"${target}\"" "${head}"

    prep_log &
    (tar xfp${VERBOSE} ${TARBALL_DIR}/$2 -C ${target} > ${_log_fifo} 2>&1)
    __r=$?; wait

    # Is there any problem with tarball?
    [ ${__r} -eq 0 ] || (
        print_err "\"${name}\" cannot be extracted!" "${head}"
        return 1
    )

    return 0
}

##################################
# @func: rm_
# @desc: removes given parameter
#
# @param*: directories or files
rm_()
{
    rm -rf${VERBOSE} ${*} 2>&1 | log ${_log_level_debug}
}

##################################
# @func: mkdir_
# @desc: makes directories
#
# @param*: directories or files
mkdir_()
{
    mkdir -p${VERBOSE} ${*} 2>&1 | log ${_log_level_debug}
}

##################################
# @func: prepare
# @desc: prepares build environment
#
# NO parameters
prepare()
{
    local head="$(toupper $FUNCNAME)"

    print_t2 "Checking for toolchain"
    {
        if [ -d "${TOOLCHAIN_DIR}" ]; then
            ask "Toolchain Initialization" \
                "There is also a toolchain directory: \"${TOOLCHAIN_DIR}\".\n\nDo you want to ${_dialog_cl_bold}backup old toolchain and recreate${_dialog_cl_nobold} it?"
            [ $? -eq 0 ] && _b_install_toolchain=true || _b_install_toolchain=false
        else
            _b_install_toolchain=true
        fi
    } # END OF TOOLCHAIN

    print_t2 "Checking for sysroot"
    {
        if [ -d "${SYSROOT}" ]; then
            ask "Sysroot Initialization" \
                "There is also a sysroot directory: \"${SYSROOT}\".\n\nDo you want to ${_dialog_cl_bold}backup old sysroot and recreate${_dialog_cl_nobold} it?"
            [ $? -eq 0 ] && _b_install_sysroot=true || _b_install_sysroot=false
        else
             _b_install_sysroot=true
        fi
    } # END OF SYSROOT

    print_t2 "Cleaning up temp directory: ${TMP_DIR}"
    rm_ ${TMP_DIR}

    print_info "Creating some minimal required directories and files" "${head}"
    # we need temp dir, tarball dir, built packages dir
    mkdir_ ${TMP_DIR} ${TOOLCHAIN_UP_DIR}

    # and we also need a fifo for outputs
    rm ${_log_fifo} 2>/dev/null
    mkfifo ${_log_fifo} 2>/dev/null

    # Be sure your system is up to date.
    print_t2 "Upgrading native Pardus system"
    {
        (DEBUG= VERBOSE= pisi_ native ur)
        (DEBUG= VERBOSE= pisi_ native up)
    } # END OF UPGRADE

    # Install toolchain, scratchbox2 and all other development tools..
    print_t2 "Installing required packages"
    {
        local native_packages="-c system.devel git subversion aria2 wget most cvs"
        DEBUG= VERBOSE= pisi_ native it "${native_packages}"

        # FIXME: remove me
        #        make nonexisting packages: scratchbox2, sbrsh and fakeroot
        for package_name in fakeroot scratchbox2; do
            if ! [ -z "$(pisi li | grep ${package_name})" ]; then continue; fi

            local package_url="http://svn.pardus.org.tr/pardus/playground/memre/"
            pisi_ native bi ${package_name} ${package_url}
            pisi_ native it ${pack}*pisi

            rm ${pack}*pisi
        done
    } # END OF INSTALL NATIVE COMPONENTS

    # Create neccessary directories
    print_t2 "Creating neccessary directories"
    mkdir_ ${SYSROOT} ${TARBALL_DIR} ${BUILT_PACKAGES_DIR} ${TARBALL_DIR} ${BUILT_PACKAGES_DIR}

    print_t2 "Fetching required components"
    {
        # ${_b_install_sysroot} && ( \
        # fetch "${DISTRIB_ID} rootfs" \
        #       ${rootfs} \
        #       ${rootfs_url}  || die "rootfs yoksa arm da yok"
        # ) # INSTALL SYSROOT
        ${_b_install_toolchain} && ( \
            fetch "${DISTRIB_ID} cross-toolchain" \
                ${TOOLCHAIN_TARBALL} \
                ${TOOLCHAIN_URL}  || die "Toolchain cannot be fetched!" "${head}"
        ) # INSTALL TOOLCHAIN
    } # END OF FETCH

    # Let user see the details at least 5 secs.
    dialog_ "msgbox" "Preparation summary" "
    Architecture......: ${_dialog_cl_red}${ARCH}${_dialog_cl_black}
    Sysroot...........: ${_dialog_cl_red}${SYSROOT}${_dialog_cl_black}
    Tarball Dir.......: ${_dialog_cl_red}${TARBALL_DIR}${_dialog_cl_black}
    Toolchain Dir.....: ${_dialog_cl_red}${TOOLCHAIN_DIR}${_dialog_cl_black}
    Temp Dir..........: ${_dialog_cl_red}${TMP_DIR}${_dialog_cl_black}" "--timeout 5"

    return 0 # success.
}

init_toolchain()
{
    # Cleanup and create directories
    local head="TOOLCHAIN"

    # FIXME: download or cat crosstool-ng configuration
    # wget http://cekirdek.pardus.org.tr/~memre/pardus-arm/corp2/ct-ng-config
    # mv ct-ng-config .config
    # /opt/ct-ng/bin/ct-ng build

    ${_b_install_toolchain} && (
        [ -d "${TOOLCHAIN_DIR}" ] && (
            print_info " ==> Backing up \"${TOOLCHAIN_DIR}\" -> \"${TOOLCHAIN_DIR}_${_backup_suffix}\"..." "${head}"
            mv ${TOOLCHAIN_DIR}{,_${_backup_suffix}} -v | log ${_log_level_debug}
        ) # BACKUP TOOLCHAIN DIRECTORY IF EXISTS

        extract "${DISTRIB_DESCRIPTION} cross-toolchain" \
            ${TOOLCHAIN_TARBALL} ${TOOLCHAIN_UP_DIR} || \
            die "Cannot extract \"cross-toolchain\"!" "${head}"
    ) # INSTALL TOOLCHAIN
}

init_sysroot()
{
    local head="SYSROOT"

    ${_b_install_sysroot} && (
        [ -d "${SYSROOT}" ] && (
            print_info " ==> Backing up \"${SYSROOT}\" -> \"${SYSROOT}_${_backup_suffix}\"..." "${head}"
            mv ${SYSROOT}{,_${_backup_suffix}} -v | log ${_log_level_debug}
        ) # BACKUP SYSROOT DIRECTORY IF EXISTS

        mkdir_ ${SYSROOT}

        # sysroot should be extracted from a tarball, but toolchain's sysroot directory
        # might be used before
        cp -rf${VERBOSE} ${TOOLCHAIN_DIR}/${HOST}/sysroot/* ${SYSROOT} | log ${_log_level_debug}
    ) # INSTALL SYSROOT
}

##################################
# @func: init_sbox2
# @desc: Initializes Scratchbox2.
#
# NO parameters
init_sbox2()
{
    local head="SBOX2"

    print_info " ==> sbox2 is building libtool for native-like cross-build" "${head}"
    cd ${SYSROOT}
    prep_log &
    (sb2-init -c ${_qemu} ${DISTRIB_ID} ${HOST}-gcc > ${_log_fifo} 2>&1)
    __r=$?; wait

    [ ${__r} -eq 0 ] || die "Scratchbox cannot be initialized!" "${head}"
}

##################################
# @func: init_pisi
# @desc: Initializes pisi for cross-build
#
# NO parameters
init_pisi()
{
    local head="PISI"

    print_info " ==> Preparing PiSi-Cross..." ${head}

    [ -L "${_pisi_cross}" ] || rm_ ${_pisi_cross}

    ln -s${VERBOSE} pisi ${_pisi_cross} | log ${_log_level_debug}

    # if there is a config file, keep it
    [ -e "${_pisi_cross_conf}" ] && mv ${_pisi_cross_conf}{,_${_backup_suffix}}

    print_info "Generating pisi-${ARCH}.conf" "${head}"

    cat > ${_pisi_cross_conf} << __EOF
#
# Pardus Linux ARM Architecture sysroot PiSi config file
# Copyright (C) 2009-2011 TUBITAK/BILGEM
#
# Generated at   : "`date -u`"
# Distribution   : ${DISTRIB_DESCRIPTION}
# Build Arch     : ${BUILD_ARCH}
# Target Arch    : ${ARCH}
# Build          : ${BUILD}
# Host           : ${HOST}
# Toolchain Dir  : ${TOOLCHAIN_DIR}
# SysRoot Dir    : ${SYSROOT}
#
# This configuration file is optimized for cortex-a8 based cores.
# tested with beagleboard. Some of the contents have taken from
# /etc/pisi/pisi.conf
#
# The host system and the development system should be the same
# distro, if you build Corporate 2 ARM, then use Corporate 2 as
# the host system. Otherwise I cannot guaranty that the system
# builds and works well.
#
# Have fun,
# Let the game begin ;)
#

[build]
build_host = localhost
# buildhelper = None
# http://comments.gmane.org/gmane.comp.gcc.cross-compiling/11513
enableSandbox = False
compressionlevel = 9
fallback = ftp://ftp.pardus.org.tr/pub/source/corporate2
generateDebug = False
crosscompiling = True
cppflags = ${CPPFLAGS}
cflags = ${CFLAGS}
cxxflags = ${CXXFLAGS}
ldflags = ${LDFLAGS}
build = ${HOST}
host = ${HOST}
target = ${HOST}
jobs = `cat /etc/pisi/pisi.conf | egrep "jobs\s+" | cut -d= -f2`
max_delta_count = `cat /etc/pisi/pisi.conf | egrep "max_delta_count\s+" | cut -d= -f2`

[directories]
archives_dir = /var/cache/pisi/archives
cache_root_dir = /var/cache/pisi
cached_packages_dir = /var/cache/pisi/packages
compiled_packages_dir = /var/cache/pisi/packages
debug_packages_dir = /var/cache/pisi/packages-debug
history_dir = /var/lib/pisi/history
index_dir = /var/lib/pisi/index
info_dir = /var/lib/pisi/info
kde_dir = `cat /etc/pisi/pisi.conf | egrep "kde_dir\s+" | cut -d= -f2`
lib_dir = /var/lib/pisi
lock_dir = /var/lock/subsys
log_dir = /var/log
packages_dir = /var/lib/pisi/package
qt_dir = `cat /etc/pisi/pisi.conf | egrep "qt_dir\s+" | cut -d= -f2`
tmp_dir = /var/pisi

[general]
autoclean = False
bandwidth_limit = 0
architecture = ${ARCH}
destinationdirectory = ${SYSROOT}
# we use destinationdirectory as SYSROOT as well
distribution = `cat /etc/pisi/pisi.conf | egrep "distribution\s+" | cut -d= -f2`
distribution_release = `cat /etc/pisi/pisi.conf | egrep "distribution_release\s+" | cut -d= -f2`
distribution_id = `cat /etc/pisi/pisi.conf | egrep "distribution_id\s+" | cut -d= -f2`
# ftp_proxy = None
# http_proxy = None
# https_proxy = None
ignore_delta = False
ignore_safety = False
package_cache = False
package_cache_limit = 0
__EOF

    print_info " ==> Checking out the latest cross-build supported PiSi" "${head}"
    cd ${TMP_DIR}
    prep_log &
    (${_svn} co https://svn.pardus.org.tr/uludag/trunk/playground/memre/pisi pisi > ${_log_fifo} 2>&1)
    __r=$?; wait

    [ ${__r} -eq 0 ] || \
        die "pisi-cross cannot be checked out, so parm initialization cannot be proceeded!" "${head}"

    print_info " ==> Removing old pisi" "${head}"
    rm -rf${VERBOSE} /usr/lib/pardus/pisi | log ${_log_level_debug}

    print_info " ==> Installing new Pisi" "${head}"
    cd pisi
    prep_log &
    (python ./setup.py install --install-lib=/usr/lib/pardus > ${_log_fifo} 2>&1)
    __r=$?; wait

    [ ${__r} -eq 0 ] || die "Unable to install new pisi!: ${__r}" "${head}"

    ${_b_install_sysroot} && (
        print_info "Adding the latest source repo to ${DISTRIB_DESCRIPTION} ${ARCH} sysroot" "${head}"
        # FIXME: no binary repo for now
        (pisi_ cross ar ${BIN_REPO_NAME} ${BIN_REPO_INDEX})
        (pisi_ cross ar ${SRC_REPO_NAME} ${SRC_REPO_INDEX})
        __r=$?; wait

        [ ${__r} -eq 0 ] || die "PiSi initialization failed!" "${head}"
    )

    return 0 # Success
}

##################################
# @func: init_farm
# @desc: Initializes buildfarm for cross-build
#
# NO parameters
init_farm()
{
    local head="$(toupper $FUNCNAME)"

    print_t2 "Preparing Buildfarm"
    print_t2 "Oh, I just changed my mind, later baby :)"
}

##################################
# @func: emerge_minimum
# @desc: Builds and installs minimum build environment to the sysroot
#
# NO parameters
emerge_minimum()
{
    local head="$(toupper $FUNCNAME)"

    # TODO:
    #  - prep initial rootfs with old rootfs.
    #  - switch to curses interface
    #  - make generic list for packages to be installed
    #  - ui enhancement, decisions with colors etc

    local min_list=(
        # Package    # Component    : Dependencies
        ##########################################
        # 'binutils'   # system.devel
        # 'libsigsegv' # system.devel
        # 'gnuconfig'  # system.devel
        # 'patch'      # system.devel
        # 'zip'        # system.base
        # 'bzip2'      # system.base
        # 'zlib'       # system.base
        # 'gdbm'       # system.base
        # 'ncurses'    # system.base  : gnuconfig
        # 'texinfo'    # system.base  : ncurses
        # 'attr'       # system.base
        # 'acl'        # system.base  : attr
        # 'libpcre'    # system.base
        # 'glib2'      # system.base  : libpcre zlib
        # 'groff'      # system.base  : texinfo
        # 'gettext'    # system.base  : glib2 acl ncurses
        # 'diffutils'  # system.base  : gettext patch
        # 'expat'      # system.base  : diffutils gnuconfig
        # 'm4'         # system.devel : gettext libsigsegv
        # 'sed'        # system.base  : gettext
        # 'bison'      # system.devel : gettext m4 patch
        # 'gmp'        # system.devel
        # 'mpfr'       # system.devel : gmp
        'busybox'    # system.base
        'glibc'      # system.base  : gettext
        'gcc'        # system.devel : binutils bison gettext gnuconfig
                     #                gmp mpfr ncurses patch sed texinfo zlib
        'db4'        # system.base
        # 'perl'       # system.base  : bzip2 db4 gdbm groff
    )

    print_t2 "Emerging minimum development tools"
    for ((pack=0; pack<${#min_list[*]}; pack++)); do
        local p=${min_list[$pack]}
        print_info " [$((pack + 1))/${#min_list[*]}] ${p}" "${head}"
        pisi_ cross emerge ${p}
    done

    print_info "Done."
}

##################################
# @func: poke_farm
# @desc: Builds all system.base, system.devel and kernel for
#        current distribution.
#
# NO parameters
poke_farm()
{
    print_info "dag basini duman almis, gumus dere durmaz akar.." "Dürtük Farm"
}

usage()
{
cat << __EOF
${DISTRIB_DESCRIPTION} ${ARCH} builder script
Copyright (C) 2010 TUBITAK/BILGEM

Please do NOT change defaults if you don't know what you do..

usage: $(basename $0) [options]
options:
  -a --arch <arch>
      Architecture of the target system.
      Or you can export \$ARCH variable.
      (default: ${ARCH})

  -t --toolchain-dir <dir>
      If you do not use default toolchain, then you must set toolchain
      directory. Please know that, we add \$TOOLCHAIN_DIR/bin to \$PATH
      variable.
      Or you can export \$TOOLCHAIN_DIR variable.
      (default: ${TOOLCHAIN_DIR})

  -c --cross <dir>
      Cross build directory, as default log, sysroot, repo etc. saves in this
      directory.
      Or you can export \$CROSS variable.
      (default: ${CROSS})

  -s --sysroot <dir>
      Sysroot directory. All dependencies based on ${ARCH} architecture, will
      be stored at here. This is heard of the build.
      Or you can export \$SYSROOT variable.
      (default: ${SYSROOT} = \$CROSS/sysroots/\$ARCH)

  -l --log-file <file-name>
      Set logfile, no need to explain.
      Or you can export \$LOG_FILE variable
      (default: ${LOG_FILE} = \$CROSS/pardus-\$ARCH.log)

  -L --log-level <digit 0..4>
      Log level. There are 5 log levels, according to this log level, you will
      see more details:
        0 : ANY   ==> neccessary stuff titles etc. In any case, you will see this log level.
        1 : ERR   ==> log error messages (inherits ANY)
        2 : WARN  ==> log warning messages (inherits ERR)
        3 : INFO  ==> log info messages (inherits WARN)
        4 : DEBUG ==> log debug messages (inherits INFO)
      Or you can export \$LOG_LEVEL variable
      (default: ${LOG_LEVEL})

  -v --verbose
      Verbose messages on

  -d --debug
      Debug messages on

  -C --disable-colors
      Don't use colors for both logging and debugging

  -f --force-yes
      Do not ask questions, go on with default values

  --skip-sbox2
      Do not initialize sbox2

  --skip-pisi
      Do not initialize pisi

  --skip-farm
      Do not initialize buildfarm

  -h --help
      Most probably you are smart enough to figure out what this is.
      If you don't think you are, then please DO NOT run this script
      or forget existence of http://bugs.pardus.org.tr

  All effected variables:
      Yazarım bi ara la, öf..
__EOF
}

######################################################################
###               L E T   T H E   G A M E   B E G I N              ###
######################################################################

# :: refers upper scope
head="::"

# some functions/commands writes absurd sh*ts to log, this is the best ;)
export LC_ALL=C

# Parse commandline options
while [ $# -ne 0 ]; do
    command=$1
    shift

    case $command in
        -a|--arch)
            ARCH=$1
            [ -z "` echo ${ARCH} | grep arm`" ] && \
                die "Architecture must be an ARM variant."
            shift
            ;;

        -t|--toolchain-dir)
            TOOLCHAIN_DIR=$1
            shift
            ;;

        -c|--cross)
            CROSS=$1
            shift
            ;;

        -s|--sysroot)
            SYSROOT=$1
            shift
            ;;

        -l|--log-file)
            LOG_FILE=$1
            shift
            ;;

        -L|--log-level)
            LOG_LEVEL=$1
            shift
            ;;

        -v|--verbose)
            VERBOSE="v"
            ;;

        -d|--debug)
            DEBUG="d"
            ;;

        -C|--disable-colors)
            _b_enable_colors=false
            ;;

        -f|--force-yes)
            _b_force_yes=true
            ;;

        --skip-sbox2)
            _b_skip_sbox2=true
            ;;

        --skip-pisi)
            _b_skip_pisi=true
            ;;

        --skip-farm)
            _b_skip_farm=true
            ;;

        -h|--help|*)
            usage
            exit 0
            ;;
    esac
done

# in order to build/install pisi packages, we need root privileges
if [ x"`id -u`" != x"0" ]; then
    echo "You need root privileges in order to go on!!"
    exit 1
fi

# If there is a logfile, then backup. We dont want to lose
# old logs, maybe its neccessary for the user.
if [ -f "${LOG_FILE}" ]; then
    cp ${LOG_FILE}{,_${_backup_suffix}}
    :> ${LOG_FILE}
fi

# Enable colors for logs, if user wants it
${_b_enable_colors} && set_colors

# Log the start date on top of the ${LOG_FILE}
log ${_log_level_debug} "Build date: `date -u`"

# Greetings
dialog_ "msgbox" "Welcome to ${DISTRIB_DESCRIPTION} ARM sysroot initializator" "
TUBITAK BILGEM
Pardus Linux Project
Copyright (C) 2010, 2011
${_dialog_cl_bold}${_dialog_cl_red}${DISTRIB_DESCRIPTION}${_dialog_cl_nobold}${_dialog_cl_black} ARM build system initializator.
${_dialog_cl_normal}
    This script prepares a complete Pardus ARM development environment.

    Please know that, your PiSi will be replaced by cross-build
    supported PiSi. If you want to reinstall your original PiSi,
    then run \`pisi it pisi -y --reinstall'.

    If you want to cancel the build operation, press Ctrl+C

    If you want to follow logs, open a new console and give this
    command: \`tail -f ${LOG_FILE}' or start this script
    with debug log level parameter.
"

# emerge_minimum
# return 0

### 1st, prepare the environment for building
print_t1 "Preparing build environment"
prepare || die "Preparation failed!" "$head"

# let user see details for 3 secs, if force-yes, then no need to wait.
${_b_force_yes} || sleep 3

${_b_install_toolchain} && {
    print_t1 "Toolchain Initialization"
    init_toolchain || die "Toolchain couldn't be initialized!" "${head}"
}

${_b_install_sysroot} && {
    print_t1 "Sysroot Initialization"
    init_sysroot || die "Sysroot couldn't be initialized!" "${head}"
}

${_b_skip_pisi} || {
    print_t1 "Cross-build supported PiSi Initialization"
    init_pisi || die "Cross-build supported PiSi couldn't be initialized!" "${head}"
}

${_b_skip_sbox2} || {
    print_t1 "Scratchbox Initialization"
    init_sbox2 || die "Scratchbox2 couldn't be initialized!" "${head}"
}

${_b_skip_farm} || {
    print_t1 "Buildfarm Initialization"
    init_farm || die "Buildfarm couldn't be initialized!" "${head}"
}

# END OF INITIALIZATION
######################################################################

# Now its time to build and install some packages.
# emerge_minimum function builds and installs minimal packages to sysroot
# print_t1 "Emerging minimal-development environment for ${ARCH} architecture"
# emerge_minimum

# Lastly, build all kernel-headers, system.base and system.devel with buildfarm.
# After that step, developer would make his/her packages ;)
# print_t1 "Building ${DISTRIB_DESCRIPTION} system.{base,devel} and kernel for ${ARCH} architecture"
# FIXME: prep queue for first build
# poke_farm

println "${DISTRIB_DESCRIPTION} ${DISTRIB_RELEASE} sysroot initializing operation complated." | log ${_log_level_any}
println "Congrats, happy hacking ;)" | log ${_log_level_any}

cleanup

