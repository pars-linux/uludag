#!/usr/bin/python
# -*- coding: utf-8 -*-

# Moves the given package list to the stable repository
# taking care of delta packages

import os
import sys
import glob
import cPickle

from shutil import copy as file_copy

from pisi.operations.delta import create_delta_package

# Global variables

default_ack_file    = "/root/2009-ack.txt"
test_path           = "/var/www/localhost/htdocs/2009-delta-test"
history_path        = "/var/www/localhost/htdocs/2009-delta"

# TODO: Rename this to the correct one.
stable_path         = "/root/stable-packages"
stable_path_test    = "./stable"

iso_packages_list   = "../data/packages.db"
iso_packages        = None

# Command line arguments
debug               = False
dryrun              = False

def _debug(msg):
    if debug:
        print msg

def get_build(p):
    return int(p.rstrip(".pisi").rsplit("-", 3)[3])

def get_name(p):
    return p.rstrip(".pisi").rsplit("-", 3)[0]

def sort_packages(p_name, path):
    """Sort packages named p_name found in patch in descending buildno order."""

    packages = glob.glob1(path, "%s-[0-9]*-[0-9]*-[0-9]*.pisi" % p_name)

    # Sort p_stable, highest build will be at index 0
    packages.sort(cmp=lambda x,y: int(get_build(x)) - int(get_build(y)), reverse=True)
    return packages

def get_delta_list(p):

    deltas_to_copy = []

    c_build = get_build(p)
    c_name = get_name(p)

    # Find the last build no of 'p' in stable
    try:

        delta_packages = []

        stable_builds = sort_packages(c_name, stable_path)
        _debug("Stable builds:\n  *** %s" % "\n  *** ".join(stable_builds))

        # Raises an exception if there's no package c_name at all
        l_build = get_build(stable_builds[0])

        _debug("\nThese are the delta names I've constructed:\n")

        # cb is in test, lb is in stable
        lb_cb_delta = "%s-%d-%d.delta.pisi" % (c_name, l_build, c_build)
        delta_packages.append(lb_cb_delta)
        _debug("  *** [Last->Current] delta is %s" % lb_cb_delta)

        # pb may not be lb-1.
        p_build = None
        try:
            p_build = get_build(stable_builds[1])
        except IndexError:
            pass

        if p_build:
            pb_cb_delta = "%s-%d-%d.delta.pisi" % (c_name, p_build, c_build)
            delta_packages.append(pb_cb_delta)
            _debug("  *** [Prev->Current] delta is %s" % pb_cb_delta)

        # ib does surely exist. It may be equal to pb or cb.
        if iso_packages.has_key(c_name):
            i_build = get_build(iso_packages[c_name])
            ib_cb_delta = "%s-%s-%s.delta.pisi" % (c_name, i_build, c_build)
            delta_packages.append(ib_cb_delta)
            _debug("  *** [ ISO->Current] delta is %s" % ib_cb_delta)

        # Unify delta_packages because ib_cb and pb_cb may be the same.
        delta_packages = list(set(delta_packages))

        _debug("\nNeeded delta packages are:\n")
        for delta in delta_packages:
            exists = os.path.exists(os.path.join(history_path, delta))
            _debug("  *** %s (In %s? ->%s)" % (delta, history_path, exists))
            if not exists:
                # We have to create the delta package 'delta'
                print "We have to build %s using PiSi API" % delta
                # TODO: Add delta build code
                new_delta = ""
                #deltas_to_copy.append(create_delta_package(..))
            else:
                # Add the delta to the list to be returned from this function
                print "Adding %s to list" % delta
                deltas_to_copy.append(delta)

    except IndexError:
        pass

    return deltas_to_copy

def main(ack_file):
    if not os.path.exists(ack_file):
        print "Error: File %s doesn't exists" % ack_file
        return

    # Bring ISO packages
    if os.path.exists(iso_packages_list):
        iso_packages = cPickle.Unpickler(open(iso_packages_list, "rb")).load()
    else:
        # Iso packages will be copied from history_path
        print "ISO packages list '%s' not found." % iso_packages_list

    # Parse ACK list
    package_list = open(ack_file, "rb").read().split()
    _debug("Number of packages: %d" % len(package_list))

    # Create another list containing the packages to be moved
    packages_to_copy = package_list[:]

    for p in package_list:
        # Move the package itself
        packages_to_copy.append(p)

        # Parse the package name, version, release and buildNo
        p_name = get_name(p)
        p_build = get_build(p)

        _debug("Current package is: %s\n" % p)
        packages_to_copy.extend(get_delta_list(p))

    print "\n".join(packages_to_copy)

    # Finally copy the packages
    for f in packages_to_copy:
        print "Copying %s.." % f
        file_copy(os.path.join(history_path, f), stable_path_test)

if __name__ == "__main__":
    if "--debug" in sys.argv:
        debug = True
        sys.argv.remove('--debug')
    if "--dryrun" in sys.argv:
        dryrun = True
        sys.argv.remove('--dryrun')
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        _debug("No arguments given, using %s" % default_ack_file)
        main(default_ack_file)

