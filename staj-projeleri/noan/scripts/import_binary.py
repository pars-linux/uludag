#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
import os
import sys

try:
    import pisi
except ImportError:
    print 'Unable to import module "pisi". Not using Pardus?'
    sys.exit(1)


def printUsage():
    print 'Usage: %s <path_to_noan> <path_to_stable> <path_to_test>' % sys.argv[0]
    sys.exit(1)


def updateDB(path_repo, repo_type, newRelease):
    from django.contrib.auth.models import User
    from noan.repository.models import Distribution, Source, Package, Binary, Update

    if repo_type not in ['stable', 'test']:
        return

    print 'Scanning %s...' % (path_repo)

    # Get latest builds only
    packages_farm = {}
    for filename in os.listdir(path_repo):
        if not filename.endswith('.pisi') or filename.endswith(".delta.pisi"):
            continue
        filename = filename[:-5]
        package_name, package_version, package_release, package_build = filename.rsplit('-', 3)
        package_build = int(package_build)
        if package_name in packages_farm:
            if package_build > packages_farm[package_name][2]:
                packages_farm[package_name] = (package_version, package_release, package_build)
        else:
            packages_farm[package_name] = (package_version, package_release, package_build)
    files_farm = ['%s-%s-%s-%s.pisi' % (name, version[0], version[1], version[2]) for name, version in packages_farm.iteritems()]

    files_db = [x.get_filename() for x in Binary.objects.all()]
    files_new = set(files_farm) - set(files_db)

    for filename in files_new:
        fullpath = os.path.join(path_repo, filename)

        print '  Importing %s' % fullpath

        pisi_file = pisi.package.Package(fullpath)
        pisi_meta = pisi_file.get_metadata()
        pisi_package = pisi_meta.package

        if newRelease:
            release = newRelease
        else:
            release = pisi_package.distributionRelease

        try:
            distribution = Distribution.objects.get(name=pisi_package.distribution, release=release)
        except Distribution.DoesNotExist:
            print  '    No such distribution in database: %s-%s' % (pisi_package.distribution, release)
            continue

        try:
            source = Source.objects.get(name=pisi_package.source.name, distribution=distribution)
        except Source.DoesNotExist:
            print  '    No such source in database: %s' % (pisi_package.source.name)
            continue

        try:
            package = Package.objects.get(name=pisi_package.name, source=source)
        except Package.DoesNotExist:
            print  '    No such package in database: %s' % (pisi_package.name)
            continue

        if repo_type == 'test':
            resolution = 'pending'
        elif repo_type == 'stable':
            resolution = 'released'

        updates = Update.objects.filter(source=source, no=pisi_package.history[0].release)
        if len(updates) == 0:
            print  '    No package update in database: %s' % (pisi_package.name)
            continue

        update = updates[0]
        try:
            binary = Binary.objects.get(no=pisi_package.build, package=package)
        except Binary.DoesNotExist:
            binary = Binary(no=pisi_package.build, package=package, update=update, resolution=resolution)
            binary.save()
            print '    New binary'

        if repo_type == 'test':
            # Mark other 'pending' binaries as 'reverted'
            binaries = Binary.objects.filter(package=package, resolution='pending', no__lt=binary.no)
            for bin in binaries:
                bin.resolution = 'reverted'
                bin.save()

    print 'Done'


def main():
    usage = "usage: %prog [options] path/to/noan path/to/binary/stable /path/to/binary/test"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-r", "--release", dest="release",
                      help="use RELEASE as ditro version instead", metavar="RELEASE")

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Incorrect number of arguments")

    path_noan, path_stable, path_test = args

    os.environ['DJANGO_SETTINGS_MODULE'] = 'noan.settings'
    sys.path.insert(0, path_noan)
    try:
        import noan.settings
    except ImportError:
        printUsage()

    updateDB(path_stable, 'stable', options.release)
    updateDB(path_test, 'test', options.release)


if __name__ == '__main__':
    main()
