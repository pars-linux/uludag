#!/bin/bash
#
#  Copyright (C) 2010 TUBITAK BILGEM
#  Pardus Linux Project
#  ARM Architecture Sysroot and Buildfarm Preparator
#
#  Author: Mehmet Emre Atasever <memre ~ pardus.org.tr>
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
# - toolchain build from scratch
# - add more comments
#   . function explanations, parameter definitions etc.
#
# - Dialog based ui
#
######################################################################

# Trap all signals for more control
set -e
trap sighandler 1 2 3 6

# Colors for a better user interaction and logging
_clNoColor="\e[0m"
_clWhite="\e[1;37m"
_clYellow="\e[1;33m"
_clCyan="\e[0;36m"
_clBlack="\e[0;30m"
_clBlue="\e[0;34m"
_clGreen="\e[0;32m"
_clCyan="\e[0;36m"
_clRed="\e[0;31m"
_clPurple="\e[0;35m"
_clBrown="\e[0;33m"
_clLightGray="\e[0;37m"
_clLightPurple="\e[1;35m"
_clLightRed="\e[1;31m"
_clLightCyan="\e[1;36m"
_clLightGreen="\e[1;32m"
_clLightBlue="\e[1;34m"
_clDarkGray="\e[1;30m"

_clInfo=${_clWhite}
_clError=${_clRed}
_clWarning=${_clYellow}
_clHead=${_clLightPurple}
_clQuestion=${_clLightRed}
_clUserAnswer=${_clNoColor}
_clTime=${_clPurple}

# Title colors
_clTitle1=${_clGreen}
_clTitle2=${_clLightGreen}
_clTitle3=${_clLightBlue}

# Title Numbers
_tn1=0  # Main title [X]
_tn2=0  # 2nd title  [1.X]
_tn3=0  # 3rd title  [1.2.X]

# Start time for logging and printing
_start_time=$(date +%s)

# some options for this script
# _b -> boolean value
_b_install_toolchain_sysroot=true
_b_use_prebuilt_sysroot=true
_b_install_toolchain=true
_b_force_yes=false
_b_skip_pisi=
_b_skip_sbox2=
_b_skip_farm=

# log levels, also print levels.
# if LOG_FILE is equal or grater than the level, then it is
# also printed to the screen
#
# see log function for details.
_log_level_any=0   # neccessary stuff titles etc.
_log_level_err=1   # error messages
_log_level_warn=2  # add warning messages
_log_level_info=3  # add info messages
_log_level_debug=4 # add some debug messages

# Progress bar animation \ | / -
_prog_bar_cpt=0

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

# A log file for testing this scripts
LOG_FILE=${LOG_FILE:-"${CROSS}/pardus-${ARCH}.log"}

# Log level for printing logs to the screen.
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

# This repo contains pre-built binary packages
BIN_REPO="${DISTRIB_ID}_bin"
BIN_REPO_URL="http://cekirdek.pardus.org.tr/~memre/pardus-arm/${ARCH}/${BIN_REPO}/pisi-index.xml.xz"

# FIXME: remove me
BIN_REPO_DIR="http://cekirdek.pardus.org.tr/~memre/pardus-arm/${ARCH}/${BIN_REPO}/" # this is the place for compiled packages

# Source repo for building PiSi packages from source codes
SRC_REPO="${DISTRIB_ID}_src"
# SRC_REPO_URL="http://svn.pardus.org.tr/pardus/playground/memre/${ARCH}/${DISTRIB_ID}/pisi-index.xml.xz"
SRC_REPO_URL="/home/memre/workspace/pardus/playground/memre/${ARCH}/${DISTRIB_ID}/pisi-index.xml.xz"

# FIXME: remove me
SRC_REPO_DIR="/home/memre/workspace/pardus/playground/memre/${ARCH}/${DISTRIB_ID}"

# Compiled packages stored here.
BUILT_REPO="${DISTRIB_ID}_local"
BUILT_PACKAGES_DIR="${CROSS}/repos/${ARCH}" # this is the place for compiled packages

######################################################################
# Toolchain options

TOOLCHAIN_URL="http://cekirdek.pardus.org.tr/~memre/pardus-arm/${ARCH}/${DISTRIB_ID}/${DISTRIB_ID}-${ARCH}-toolchain.tar.xz"
TOOLCHAIN_SHA1SUM="76f8211e3af869015d795ef7d1f9a8a676b61751"
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

# for printing time info in logger
PRINT_TIME=1

# fifo for logging, this is a workaround of bash pipe operation
# we often use this fifo for logging
_log_fifo="${TMP_DIR}/.pardus_${ARCH}_logfifo"

##################################
# @func: backup_suffix
# @desc: if there is a file which this script change, then backup previous one
#        with a suffix
backup_suffix()
{
    echo "$(date +%y_%m_%d_%H_%M_%S)"
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
    for i in 1 2 3 4 5; do
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
    echo -e "$*${_clNoColor}";
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
    local debug_out="/dev/null" # do not print to the console as default
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
            local message=
            local current_time="[${_clTime}$(elapsed_time)${_clNoColor}]"

            # if user want timer, then log it.
            [ "${PRINT_TIME}" ] && message="${current_time} "

            # for replacing the animation
            [ -z "${line}" ] &&  line="   "

            message="${message}${line}"

            # if LOG_LEVEL is equal or grater than the log_level, which
            # is given from the function which calls this log function,
            # then print this log to the console as well.
            #
            # this is good with debugging, but end user needn't to see
            # all the outputs of the applications.
            [ ${LOG_LEVEL} -ge ${log_level} ] && debug_out="/proc/self/fd/1"

            println "${message}" | tee -a ${LOG_FILE} > ${debug_out} 2>&1

            _prog_bar=( '\\'
                        '|'
                        '/'
                        '-' )

            echo -ne "${current_time} ${_prog_bar[$((_prog_bar_cpt/5))]} \r"
            _prog_bar_cpt=$(( (_prog_bar_cpt + 1) % 20 ))
        done
    ) # end of logging
}

##################################
# @func: elapsed_time
# @desc: prints elapsed time since this script started
#
# @param1: start_time (optinal, if $1="" then use global _start_time)
#
# @usage: echo "$(elapsed_time)"
elapsed_time()
{
    local current_time=$(date +%0s)
    local start_time=${1:-${_start_time}}

    local secs=$(( current_time - start_time ))

    printf "%02d:%02d" $((secs/60)) $((secs%60))
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
#           1.1) [this function]
#             ^
#             1.1.1) print_t3
#             1.1.2) print_t3
#           1.2) [this function]
#             ^
#             1.2.1) print_t3
#             1.2.2) print_t3
#
#         Increses _tn2 and sets _tn3 as 0.
#
# @param*: title text
print_t2()
{
    # title 2 [1.X]
    _tn2=$((${_tn2} + 1))
    _tn3="0"

    local message="   ${_clTitle2}${_tn1}.${_tn2}) $*"

    println "${message}" | log "${_log_level_any}"
}

##################################
# @func: print_t3
# @desc: prints subtitle 3
#        This subtitle prints like this:
#         1) print_t1
#           1.1) print_t2
#             1.1.1) [this function]
#                 ^
#             1.1.2) [this function]
#                 ^
#         Increses _tn3.
#
# @param*: title text
print_t3()
{
    # title 3 [1.2.X]
    _tn3=$(($_tn3 + 1))

    local message="     ${_clTitle3}${_tn1}.${_tn2}.${_tn3}) $*"

    println "${message}" | log "${_log_level_any}"
}

##################################
# @func: ask
# @desc: asks a question to the user.
#
# @param1: message to be printed
# @param2: head
ask()
{
    local head=$2
    local message=" ${_clHead}${head} ${_clQuestion}${1}${_clUserAnswer} "

    println "${message}" | log "${_log_level_any}"
}

##################################
# @func: yesno
# @desc: gets answer from user and prints it to the screen
yesno()
{
    # default answer is NULL
    if ${_b_force_yes}; then echo; return; fi

    local ret_val=
    read answer

    # define ret_val values
    case "$answer" in
        [Nn]|[Nn][Oo])
            ret_val="no"
            ;;

        [Yy]|[Yy][Ee]|[Yy][Ee][Ss])
            ret_val="yes"
            ;;

        "")
            # this is used for default answers (eg. ok? [Yn] : default:Yes)
            ret_val="";;

        *)
            ret_val="${answer}";;

    esac

    echo $ret_val | tee -a ${LOG_FILE} 2>&1
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
    print_err "Build script is terminating! Removing temporary files and directories." "DIE"

    cleanup

    exit 1
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
    local head="$(toupper $FUNCNAME)"

    local system=$1     # refers cross or native
    local operation=$2  # refers which operation will be performed
    local pisi_cmd=     # refers the pisi command (native or cross)

    # Native or cross pisi, make your choice
    case ${system} in
        n|native)
          pisi_cmd=${_pisi_native}
          ;;

        c|cross)
          pisi_cmd=${_pisi_cross}
          ;;

        *)
          die "Hmm, another \`build stayla'.." "${head}"
          ;;
    esac

    # pisi operation
    case ${operation} in
        ur|update-repo)
            # update native or cross repositories
            # no more parameters
            print_t3 "Upgrading Repositories"
            prep_log &
            (${pisi_cmd} ur -y${VERBOSE}${DEBUG} > ${_log_fifo} 2>&1)
            __r=$?; wait

            if [ ${__r} -ne 0 ]; then die "Unable to update repositories!" "${head}"; fi
            ;;

        up|upgrade)
            # upgrade native or cross repositories
            # no more parameters
            print_t3 "Upgrading System"
            prep_log &
            (${pisi_cmd} up -y${VERBOSE}${DEBUG} > ${_log_fifo} 2>&1)
            __r=$?; wait

            if [ ${__r} -ne 0 ]; then die "Unable to upgrade system!" "${head}"; fi
            ;;

        it|install)
            # @param3 packages
            # @param4 extra_parameters
            local packages=$3
            local extra_parameters="$4"

            print_t3 "Installing packages"
            print_info "Following packages will be installed: \"${packages}\"" "${head}"
            prep_log &
            (${pisi_cmd} it -y${VERBOSE}${DEBUG} ${extra_parameters} ${packages} > ${_log_fifo} 2>&1)
            __r=$?; wait

            if [ ${__r} -ne 0 ]; then die "Unable to install packages: \"${packages}\"" "${head}"; fi
            ;;

        bi|build)
            # @param3 package_name
            # @param4 package_url
            # @param5 extra_parameters
            local package_name="$3"
            local package_url="$4"
            local extra_parameters="$5"

            local pspec="${package_url}/${package_name}/pspec.xml"

            print_t3 "Building package: ${package_name}"
            prep_log &

            (${pisi_cmd} bi -y${VERBOSE}${DEBUG} ${PISI_IGNORE_CHECK} ${extra_parameters} ${pspec} > ${_log_fifo} 2>&1)
            __r=$?; wait
            if [ ${__r} -ne 0 ]; then die "Unable to build \"${package_name}\"" "${head}"; fi
            ;;

        em|emerge)
            # @param3 packages
            # @param4 extra_parameters
            local packages="$3"
            local extra_parameters="$4"

            print_t3 "Emerging packages"
            print_info "Following packages will be emerged: \"${packages}\"" "${head}"
            prep_log &
            (${pisi_cmd} em -y${VERBOSE}${DEBUG} ${PISI_IGNORE_CHECK} ${extra_parameters} ${packages} > ${_log_fifo} 2>&1)
            __r=$?; wait

            if [ ${__r} -ne 0 ]; then die "Unable to emerge package: \"${packages}\"" "${head}"; fi
            ;;

        ar|add-repo)
            # @param3 Repository name (eg. corp2-test)
            # @param4 Repository url (eg. http://packages.pardus.org.tr/pardus/corporate2/devel/x86_64/pisi-index.xml.xz)
            local repo_name=$3
            local repo_url=$4

            repos=`cat ${SYSROOT}/var/lib/pisi/info/repos | \
                   grep Name | \
                   cut -d\> -f2 | \
                   cut -d\< -f1 | \
                   tr '\n' ' '`

            print_info "Adding repository: \"${repo_name}\"" "${head}"
            prep_log &
            (${pisi_cmd} ar -y${VERBOSE}${DEBUG} ${repo_name} ${repo_url} > ${_log_fifo} 2>&1)
            __r=$?; wait

            if [ ${__r} -ne 0 ]; then
                # actually, this should "die"
                print_err "Unable to add repo \"${repo_name}\"" "${head}";
                return 1;
            fi
            ;;

        ix|index)
            # NO parameters
            print_info "Creating pisi-index" "${head}"
            prep_log &
            (${pisi_cmd} ix -y${VERBOSE}${DEBUG} --skip-signing > ${_log_fifo} 2>&1)
            __r=$?; wait

            if [ ${__r} -ne 0 ]; then print_err "Unable to create pisi-index" "${head}"; return 1; fi
            ;;

         *)
            die "PiSi nin yetenekleri sinirli haci, her seyi yapamaz.." "${head}"
            ;;

    esac
}

##################################
# @func: checksum
# @desc: checks the tarballs with sha1sum
#
# @param1: tarball in filesystem
# @param2: sha1sum
checksum()
{
    local head="$(toupper $FUNCNAME)"

    local tarball=$1
    local sum=$2

    if [ -e "${tarball}" ]; then
        if [ x"`sha1sum ${tarball} | cut -d' ' -f1`" != x"${sum}" ]; then
            if [ -e "${tarball}.aria2" ]; then
                return 2 # there is a downloaded image and can be proceeded
            else
                print_warn "Removing bad \"${tarball}\" image!" "${head}"
                rm -fv ${tarball} 2>&1 | log ${_log_level_debug}
                return 1 # fail, refetch
            fi
        else
            return 0 # already fetched
        fi
    fi

    return 1 # no archive, fetch it.
}

##################################
# @func: fetch
# @desc: fetches something from net
#
# @param1: tarball description name for printing log (eg. toolchain)
# @param2: tarball full name (eg. PardusCorporate-armv7l-toolchain.tar.xz)
# @param3: download link of the tarball (eg. http://hede.hodo/PardusCorporate-armv7l-toolchain.tar.xz)
# @param4: sha1sum of the tarball
fetch()
{
    local head="$(toupper $FUNCNAME)"

    local name=$1
    local tarball=$2
    local download_link=$3
    local sum=$4

    cd ${TARBALL_DIR}
    if checksum ${tarball} ${sum} ; then
        print_warn "Already fetched: \"${name}\"" "${head}"
        return 0
    fi

    print_info "Fetching: \"${name}\"" "${head}"
    prep_log &
    (aria2c -c ${download_link} > ${_log_fifo} 2>&1)
    __r=$?; wait

    # Is there any connection problem?
    if [ ${__r} -ne 0 ]; then
        print_err "Couldn't fetch \"${name}\"" "${head}"
        return 1
    fi

    # Check sha1sum
    if ! checksum ${tarball} ${sum} ; then
        print_err "Downloaded Image is bad: \"${name}\"" "${head}"
        return 1
    fi

    return 0
}

##################################
# @func: extract
# @desc: extracts tarballs (@param2) (in ${TARBALL_DIR} directory)
# to given directory (@param3)
#
# @param1: tarball description name for printing log (eg. toolchain)
# @param2: tarball full name (eg. PardusCorporate-armv7l-toolchain.tar.xz)
# @param3: destinationdirectory directory for tarball
extract()
{
    local head="$(toupper $FUNCNAME)"

    local ret_val=0

    local name=$1
    local tarball=$2
    local target=$3

    print_info "Extracting: \"${name}\"" "${head}"

    prep_log &
    tar xfp${VERBOSE} ${TARBALL_DIR}/$2 -C ${target} > ${_log_fifo} 2>&1
    __r=$?; wait

    # Is there any problem with tarball?
    if [ ${__r} -ne 0 ]; then
        print_err "Couldn't extract \"${name}\"" "${head}"
        ret_val=1
    fi

    return ${ret_val}
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
# @desc: prepares initial `hede's
#
# NO parameters
prepare()
{
    local head="$(toupper $FUNCNAME)" # 1st. Preparation Phase

    print_t2 "Cleaning up temp directory: ${TMP_DIR}"
    rm_ ${TMP_DIR}
    print_info "Creating some minimal required directories and files" "${head}"
    # we need temp dir, tarball dir, built packages dir
    mkdir_ ${TMP_DIR} ${TOOLCHAIN_UP_DIR}
    # and we need a fifo for outputs also
    rm ${_log_fifo} 2>/dev/null
    mkfifo ${_log_fifo} 2>/dev/null

    # Be sure your system is up to date.
    print_t2 "Upgrading system"
    {
        pisi_ native ur
        pisi_ native up
    } # END OF UPGRADE

    # Install toolchain, scratchbox2 and all other development tools..
    print_t2 "Installing required packages"
    {
        # FIXME: make nonexisting packages : fakechroot sbrsh
        # WORKAROUND: emerge from playground
        # local native_packages="-c system.devel git git-svn subversion scratchbox2 fakeroot aria2 most"
        local native_packages="-c system.devel git subversion aria2 wget most"
        pisi_ native it "${native_packages}"

        # FIXME: make nonexisting packages and remove me
        for package_name in fakeroot scratchbox2; do
            local package_url="http://svn.pardus.org.tr/pardus/playground/memre/"
            pisi_ native bi ${package_name} ${package_url}
            pisi_ native it ${pack}*pisi
            rm ${pack}*pisi
        done
    } # END OF INSTALL NATIVE COMPONENTS

    # FIXME: download or cat crosstool-ng configuration
    # wget http://cekirdek.pardus.org.tr/~memre/pardus-arm/corp2/ct-ng-config
    # mv ct-ng-config .config
    # /opt/ct-ng/bin/ct-ng build

    # Cleanup and create directories
    print_t2 "Checking for toolchain"
    {
        local sub_head="TOOLCHAIN"

        if [ -d "${TOOLCHAIN_DIR}" ]; then
            print_warn "There is also a toolchain directory: \"${TOOLCHAIN_DIR}\"" "${head}::${sub_head}"

            while true; do
                ask "Do you want to remove and recreate \"${TOOLCHAIN_DIR}\"? [yN] " "${head}::${sub_head}"
                answer=$(yesno)

                if [ x"$answer" == x"yes" ]; then
                    print_t3 "Removing all ${TOOLCHAIN_DIR} contents"
                    rm_ ${TOOLCHAIN_DIR}
                    _b_install_toolchain=true
                    break
                elif [[ x"$answer" == x"no" || x"$answer" == x"" ]]; then
                    print_info "Skiped removing ${TOOLCHAIN_DIR}" "${head}::${sub_head}"
                    _b_install_toolchain=false
                    break
                else
                    print_err "Wrong answer" "${head}::${sub_head}"
                fi
            done
        fi

        print_info "Toolchain checked." "${head}"
    } # END OF TOOLCHAIN

    print_t2 "Checking for sysroot"
    {
        local sub_head="SYSROOT"

        if [ -d "${SYSROOT}" ]; then
            print_warn "There is also a sysroot directory: \"${SYSROOT}\"" "${head}::${sub_head}"

            while true; do
                ask "Do you want to remove and recreate \"${SYSROOT}\"? [yN] " "${head}::${sub_head}"
                answer=$(yesno)

                if [ x"$answer" == x"yes" ]; then
                    print_t3 "Removing all \"${SYSROOT}\" contents"
                    rm_ ${SYSROOT}

                    # FIXME:
                    # this option enables copying a temporary sysroot
                    # into the sysroot directory.
                    _b_install_toolchain_sysroot=true
                    break
                elif [[ x"$answer" == x"no" || x"$answer" == x"" ]]; then
                    print_info "Skiped removing \"${SYSROOT}\"" "${head}::${sub_head}"
                    _b_install_toolchain_sysroot=false
                    break
                else
                    print_err "Wrong answer" "${head}::${sub_head}"
                fi
            done
        fi

        print_info "Sysroot checked." "${head}"
    } # END OF SYSROOT

    # Create neccessary directories
    print_t2 "Creating neccessary directories"
    mkdir_ ${SYSROOT} ${TARBALL_DIR} ${BUILT_PACKAGES_DIR} ${TARBALL_DIR} ${BUILT_PACKAGES_DIR}

    print_t2 "Fetching required components"
    {
        # fetch "${DISTRIB_ID} rootfs" \
        #       ${rootfs} \
        #       ${rootfs_url} \
        #       ${rootfs_sha1sum} || die "rootfs yoksa arm da yok"
        if ${_b_install_toolchain}; then
            fetch "${DISTRIB_ID} cross-toolchain" \
                  ${TOOLCHAIN_TARBALL} \
                  ${TOOLCHAIN_URL} \
                  ${TOOLCHAIN_SHA1SUM} || die "Toolchainsiz bunu (o))) insa edersin" "${head}"
        fi

        print_info "Required components fetched" "${head}"
    } # END OF FETCH

    print_t2 "Extracting fetched components"
    {
        if ${_b_install_toolchain}; then
            extract "Pardus ${DISTRIB_DESCRIPTION} cross-toolchain" ${TOOLCHAIN_TARBALL} ${TOOLCHAIN_UP_DIR} || \
                die "Toolchain, aah toolchain, esekler kovalasin seni.." "${head}"
        fi
    } # END OF EXTRACTING

    print_t2 "Preparing first temporary sysroot"
    {
        # Copy the toolchain's minimal sys-root to $SYSROOT directory.
        # During the build processes, this sys-root will be changed.
        if ${_b_install_toolchain_sysroot}; then
            print_info "Copying toolchain sysroot as temporary-rootfs"
            cp -rf${VERBOSE} ${TOOLCHAIN_DIR}/${HOST}/sys-root/* ${SYSROOT} | log ${_log_level_debug}
        fi
    } # END OF INITIAL SYSROOT PREPARATION

    return 0 # success.
}

##################################
# @func: init_sbox2
# @desc: Initializes Scratchbox2.
#
# NO parameters
init_sbox2()
{
    local head="$(toupper $FUNCNAME)"

    # FIXME: scratchbox2 emerge support
    print_info "Scratchbox2 is building libtool for native-like crossbuild" "${head}"
    cd ${SYSROOT}
    prep_log &
    (sb2-init -c ${_qemu} ${DISTRIB_ID} ${HOST}-gcc > ${_log_fifo} 2>&1)
    __r=$?; wait

    # Is there any problem with scratchbox2 init?
    if [ ${__r} -ne 0 ]; then
        print_err "Scratchbox2 couldn't initialized" "${head}"
        die "Without Scratchbox2, you can only build this: (O)))"
    fi

    print_info "Done." "${head}"

    return 0
}

##################################
# @func: init_pisi
# @desc: Initializes pisi for cross-build
#
# NO parameters
init_pisi()
{
    local head="$(toupper $FUNCNAME)"

    print_t2 "Preparing PiSi-Cross"

    if [ -L "${_pisi_cross}" ]; then
        rm_ ${_pisi_cross}
    fi

    ln -s${VERBOSE} pisi ${_pisi_cross} | log ${_log_level_debug}

    print_info "Generating pisi-${ARCH}.conf" "${head}"

    # if there is a config file, keep it
    if [ -e "${_pisi_cross_conf}" ]; then
        mv ${_pisi_cross_conf}{,_$(backup_suffix)}
    fi

    cat > ${_pisi_cross_conf} << __EOF
#
# Copyright (C) 2010 TUBITAK/BILGEM
# Pardus Linux ARM Architecture sysroot PiSi config file
#
# Generated at   : "`date`"
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
enableSandbox = True
compressionlevel = 9
fallback = ftp://ftp.pardus.org.tr/pub/source/corporate2
generateDebug = False
crosscompiling = True
cflags = ${CFLAGS}
cxxflags = ${CXXFLAGS}
ldflags = ${LDFLAGS}
host = ${HOST}
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

    print_t3 "Removing old pisi"
    rm -rf${VERBOSE} /usr/lib/pardus/pisi | log ${_log_level_debug}

    print_t3 "Checking out the latest cross-build supported PiSi from memre's playground"
    cd ${TMP_DIR}
    prep_log &
    (${_svn} co https://svn.pardus.org.tr/uludag/trunk/playground/memre/pisi pisi > ${_log_fifo} 2>&1)
    __r=$?; wait
    if [ ${__r} -ne 0 ]; then die "Unable to checkout pisi-cross!" "${head}"; fi

    print_t3 "Installing new Pisi"
    cd pisi
    prep_log &
    (python ./setup.py install --install-lib=/usr/lib/pardus> ${_log_fifo} 2>&1)
    __r=$?; wait
    if [ ${__r} -ne 0 ]; then die "Unable to install new pisi!: ${__r}" "${head}"; fi

    print_t3 "Adding latest source repo to ${DISTRIB_DESCRIPTION} ${ARCH} sysroot"
    # FIXME: no binary repo for now
    # pisi_ cross ar ${BIN_REPO} ${BIN_REPO_URL}
    (pisi_ cross ar ${SRC_REPO} ${SRC_REPO_URL})
    __r=$?
    if [ ${__r} -ne 0 ]; then print_err "Unable to add repo!" "${head}"; fi

    return 0
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
# @desc: Builds and installs minimum requirements to the sysroot
#
# NO parameters
emerge_minimum()
{
    print_info "ehehehehe, I won't emerge anything, I will make farm to emerge all of it!! :P"
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
      Verbose messages on.

  -d --debug
      Debug messages on.

  -f --force-yes
      Do not ask questions, go on with default values.

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

# some functions/commands writes absurd sh*ts to log, this is the best ;)
export LC_ALL=C

# Parse commandline options
while [ $# -ne 0 ]; do
    command=$1
    shift

    case $command in
        -a|--arch)
            ARCH=$1
            if [ -z "` echo ${ARCH} | grep arm`" ]; then
                die "Architecture must be an ARM variant."
            fi
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
    cp ${LOG_FILE}{,_$(backup_suffix)}
    :> ${LOG_FILE}
fi

# :: refers upper scope
head="::"

# Lets start with a clean page.
clear

# Log the start date on top of the ${LOG_FILE}
log ${_log_level_debug} "Build date: `date`"

# Greetings
println "
 ${_clGreen}TUBITAK BILGEM
 ${_clGreen}Pardus Linux Project
 ${_clGreen}Copyright (C) 2010, 2011
 ${_clYellow}Welcome to ${_clRed}${DISTRIB_DESCRIPTION}${_clYellow} ARM build system.
 ${_clNoColor}
    If you want to cancel build operation, press Ctrl+C

    Please know that, your PiSi will be replaced by the PiSi of memre\'s.
    If you want to reinstall your original PiSi, run \`pisi it pisi -y --reinstall'.

    If you want to follow logs, open a new console and give this command: \`tail -f ${LOG_FILE}'

    Press return to continue... " | log ${_log_level_any}

# if user doesnt want to answer questions, then assume that he/she doesnt want
# to wait. Otherwise show all the stuff.
if ! ${_b_force_yes}; then read; fi

### 1st, prepare the environment for building
print_t1 "Preparing build environment"
prepare || die "Preparation failed!" "$head"

# Print info
print_info "Architecture......: ${ARCH}" "${head}"
print_info "Sysroot...........: ${SYSROOT}"  "${head}"
print_info "Tarball Dir.......: ${TARBALL_DIR}" "${head}"
print_info "Toolchain Dir.....: ${TOOLCHAIN_DIR}" "${head}"
print_info "Temp Dir..........: ${TMP_DIR}" "${head}"

# let user see details for 3 secs, if he/she want to see details.
if ! ${_b_force_yes}; then sleep 3; fi

### 2nd phase of the building is scratchbox2 initialization
[ ${_b_skip_sbox2} ] || {
    print_t1 "Initializing scratchbox for ${DISTRIB_DESCRIPTION}"
    init_sbox2 || die "Scratchbox2 couldn't be initialized" "${head}"
}

### 3rd phase is preparing PiSi
[ ${_b_skip_pisi} ] || {
    print_t1 "Preparing PiSi for ${DISTRIB_DESCRIPTION}"
    init_pisi || die "PiSi couldn't be initialized" "${head}"
}

### 4th phase is preparing buildfarm
# [ ${_b_skip_farm} ] || {
#     print_t1 "Preparing buildfarm for ${DISTRIB_DESCRIPTION}"
#     init_farm || die "Buildfarm couldn't be initialized" "${head}"
# }

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

println "Pardus ${DISTRIB_DESCRIPTION} sysroot initializing operation complated." | log ${_log_level_any}
println "Congrats, happy hacking ;)" | log ${_log_level_any}

cleanup

