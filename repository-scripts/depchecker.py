#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pisi
import cPickle
from optparse import OptionParser

# Pisi DB instances
installdb = pisi.db.installdb.InstallDB()
packagedb = pisi.db.packagedb.PackageDB()
componentdb = pisi.db.componentdb.ComponentDB()


### Helper functions

def save_data_into(path, results, hide_system_base):
    # Create path if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Get system.base packages
    system_base = componentdb.get_packages("system.base")

    # Create sweet headers
    actual_deps_header = "Actual runtime dependencies in repository:"
    actual_deps_header += "\n%s\n" % (len(actual_deps_header)*'-')

    real_deps_header = "Real runtime dependencies according to depchecker:"
    real_deps_header += "\n%s\n" % (len(real_deps_header)*'-')

    missing_deps_header = "Missing runtime dependencies according to depchecker:"
    missing_deps_header += "\n%s\n" % (len(missing_deps_header)*'-')

    for p in results.keys():
        f = open(os.path.join(path, p), "w")

        # Get the lists
        real_deps = results[p][0]
        actual_deps = results[p][1]
        missing_deps = results[p][2]

        # Filter system.base packages if needed
        if hide_system_base:
            real_deps = [d for d in real_deps if d not in system_base]
            actual_deps = [d for d in actual_deps if d not in system_base]
            missing_deps = [d for d in missing_deps if d not in system_base]
        else:
            def format(x):
                if x in system_base:
                    return "(*) %s" % x
                else:
                    return "    %s" % x
            real_deps = [format(d) for d in real_deps]
            actual_deps = [format(d) for d in actual_deps]
            missing_deps = [format(d) for d in missing_deps]

        try:
            f.write(actual_deps_header)
            f.write("\n".join(["%s" % d for d in actual_deps]))
            f.write("\n\n"+real_deps_header)
            f.write("\n".join(["%s" % d for d in real_deps]))
            f.write("\n\n"+missing_deps_header)
            f.write("\n".join(["%s" % d for d in missing_deps]))

            if not hide_system_base:
                f.write("\n\n\n(*): The package is in system.base.")
        except IOError:
            print "** IO Error while writing %s" % os.path.join(path, p)
            pass
        finally:
            f.close()


def print_results(results, hide_system_base, colorize):
    def colorize(s):
        if colorize:
            if "B" in s:
                s = "\x1b[1;33m" + s    # system.base -> yellow
            elif s.startswith("-"):
                s = "\x1b[1;31m" + s    # missing dep -> red
            elif s.startswith("+"):
                s = "\x1b[0;32m" + s    # written dep -> green
            else:
                pass
        return s

    # Get system.base packages
    system_base = componentdb.get_packages("system.base")

    for p in results.keys():
        # Get the lists
        real_deps = results[p][0]
        actual_deps = results[p][1]
        missing_deps = results[p][2]

        deps = []

        # Filter system.base if requested
        if hide_system_base:
            real_deps = [d for d in real_deps if d not in system_base]

        for d in real_deps:
            marker = ""
            if d in actual_deps:
                marker += "+"
            elif d in missing_deps:
                marker += "-"
            else:
                marker += " "

            if d in system_base:
                marker += "B"
            else:
                marker += " "

            deps.append("%s  %s" % (colorize(marker), d))

        print "\n".join([d for d in sorted(deps)])


def generate_elf_cache(path):
    # Iterate over packages and generate ELF->Package mapping cache
    elf_to_package = {}
    for p in pisi.api.list_installed():
        print "Checking package %s.." % p,
        (dyns, execs) = get_elf_list(p, True)
        if len(dyns) > 0:
            elf_to_package.update(dict((k, p) for k in dyns))
            print " %d shared object(s) found and added to the mapping cache." % len(dyns)
        else:
            print " No shared object(s)."

    # Dump elf mapping dictionary for further usage
    print "Saving ELF mapping cache..",
    f = open(path, "w")
    cPickle.Pickler(f, protocol=2)
    cPickle.dump(elf_to_package, f, protocol=2)
    f.close()
    print "Done."

def load_elf_cache(path):
    d = {}
    if os.path.exists(path):
        d = cPickle.Unpickler(open(path, "r")).load()

    return d

def get_elf_list(package, dont_trust_packager):
    # Eliminate symbolic links and return a list of all the files that needs to be investigated (ELF)
    def filter_file(f):
        if os.path.exists("/%s" % f.path):
            if dont_trust_packager:
                return True
            else:
                return (f.type == 'library' or f.type == 'executable')
        else:
            return False

    files = [("/%s" % p.path) for p in installdb.get_files(package).list if filter_file(p)]
    dyns = []
    execs = []

    for f in files:
        elf_type = os.popen("/usr/bin/readelf -h \"%s\" 2>/dev/null | grep \"^  Type:\" | gawk '{ print $2 }'" % f).read().strip()
        if elf_type == "DYN":
            dyns.append(f)
        elif elf_type == "EXEC":
            execs.append(f)
        else:
            continue

    return (dyns, execs)

def get_needed_objects(f):
    objs = [l.strip().split()[1] for l in os.popen("/usr/bin/objdump -p \"%s\" | grep 'NEEDED'" % f).readlines()]

    # Get full path to the objects

    filemap = {}
    for l in [_l for _l in os.popen("/usr/bin/ldd \"%s\" 2> /dev/null" % f).readlines() if "=>" in _l]:
        # Filter these special objects
        if "linux-gate" in l or "ld-linux.so" in l:
            continue
        ls = l.split("=>")
        filemap[ls[0].strip()] = ls[1].split(" (")[0].strip()

    for i in range(len(objs)):
        if filemap.has_key(objs[i]):
            objs[i] = filemap[objs[i]]

    return objs


### Entry point

if __name__ == "__main__":

    if len(sys.argv) == 1:
        sys.argv.append("--help")

    parser = OptionParser()
    parser.add_option("-C", "--color",
                      action="store_true",
                      dest="colorize",
                      default=False,
                      help="Colorize output")

    parser.add_option("-s", "--hide-system-base",
                      action="store_true",
                      dest="hide_system_base",
                      default=False,
                      help="Hide system.base dependencies")

    parser.add_option("-c", "--component",
                      action="store",
                      dest="component",
                      help="Check dependencies only for the given component")

    parser.add_option("-g", "--generate-elf-cache",
                      action="store_true",
                      dest="generate_elf_cache",
                      default=False,
                      help="Generate elf cache for pisi packages in /var/lib/pisi")

    parser.add_option("-D", "--dont-trust-packager",
                      action="store_true",
                      dest="dont_trust_packager",
                      default=False,
                      help="Checks for all the files regardless of their types in pspec.xml. This will bring a performance penalty.")

    parser.add_option("-d", "--output-directory",
                      action="store",
                      dest="output_directory",
                      help="If given, the dependency informations will be written into the output directory")

    (options, packages) = parser.parse_args()

    if options.generate_elf_cache:
        generate_elf_cache("/var/lib/pisi/elfcache.db")
        sys.exit(0)

    # Load elf cache
    elf_to_package = load_elf_cache("/var/lib/pisi/elfcache.db")
    if not elf_to_package:
        print "You first have to create the elf cache using -c parameter."
        sys.exit(1)

    # Get packages from the given component
    if options.component:
        packages = componentdb.get_packages(options.component)

    # Some loop counters here
    pindex = 1
    total = len(packages)

    if total > 1:
        # Automatically fallback to directory output if there are multiple packages
        options.output_directory = "results"

    # Results dictionary: (package->deps)
    results = {}

    # Iterate over packages and find the dependencies
    for p in packages:

        needed = set()
        actual_deps = set()
        missing_deps = set()
        real_deps = set()

        (dyns, execs) = get_elf_list(p, options.dont_trust_packager)
        for elf in dyns+execs:
            needed.update(set(get_needed_objects(elf)))

        real_deps = set([elf_to_package.get(k, '<Not found>') for k in needed.intersection(elf_to_package.keys())])
        try:
            actual_deps = set([d.package for d in packagedb.get_package(p).runtimeDependencies()])
            missing_deps = real_deps.difference(actual_deps)
        except:
            print "**** %s cannot be found in package DB, probably the package has been deleted from the repository." % p
            continue

        # Push the informations to the results dictionary filtering the current package from the sets
        results[p] = (real_deps.difference([p]),
                      actual_deps.difference([p]),
                      missing_deps.difference([p]))

        # Increment the counter
        pindex += 1

    if options.output_directory:
        print "Saving results into %s" % options.output_directory,
        save_data_into(options.output_directory, results, options.hide_system_base)
        print "done."
    else:
        # The informations will be printed to the screen
        print_results(results, options.hide_system_base, options.colorize)

    sys.exit(0)
