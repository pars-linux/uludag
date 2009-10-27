#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
import os
import sys

from pisi.version import Version as Pisi_Version

try:
    import pisi
except ImportError:
    print 'Unable to import module "pisi". Not using Pardus?'
    sys.exit(1)


def printUsage():
    print 'Usage: %s <path_to_noan> <path_to_stable> <path_to_test>' % sys.argv[0]
    sys.exit(1)


def updateDB(path_repo, repo_type, options):
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

    # Index binaries
    for filename in files_new:
        fullpath = os.path.join(path_repo, filename)

        print '  Found unindexed binary: %s' % fullpath

        pisi_file = pisi.package.Package(fullpath)
        pisi_meta = pisi_file.get_metadata()
        pisi_package = pisi_meta.package

        if options.release:
            release = options.release
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
    

    # Write pending dependencies of a package to it's model
    for bin in Binary.objects.filter(resolution='pending'):
        dependencies = []
        for dep in bin.package.runtimedependency_set.all():
            binaries = Binary.objects.filter(package__source__distribution = bin.package.source.distribution, package__name=dep.name)
            # version
            if dep.version != "" and binaries.filter(update__version_no=dep.version, resolution="released").count() == 0:
                dependencies.extend(binaries.filter(resolution="pending"))
            elif dep.version_from != "":
                in_stable = False
                for bin_released in binaries.filter(resolution="released"):
                    if Pisi_Version(bin_released.update.version_no) >= Pisi_Version(dep.version_from):
                        in_stable = True
                        break
                if not in_stable:
                    dependencies.extend(binaries.filter(resolution="pending"))
            elif dep.version_to != "":
                in_stable = False
                for bin_released in binaries.filter(resolution="released"):
                    if Pisi_Version(bin_released.update.version_no) <= Pisi_Version(dep.version_to):
                        in_stable = True
                        break
                if not in_stable:
                    dependencies.extend(binaries.filter(resolution="pending"))
            elif binaries.filter(resolution="released").count() == 0:
                dependencies.extend(binaries.filter(resolution="pending"))
            # release
            if dep.release != "" and binaries.filter(update__no=dep.release, resolution="released").count() == 0:
                dependencies.extend(binaries.filter(resolution="pending"))
            elif dep.release_from != "" and binaries.filter(update__no__gte=dep.release, resolution="released").count() == 0:
                dependencies.extend(binaries.filter(resolution="pending"))
            elif dep.release_to != "" and binaries.filter(update__no__lte=dep.release, resolution="released").count() == 0:
                dependencies.extend(binaries.filter(resolution="pending"))
            elif binaries.filter(resolution="released").count() == 0:
                dependencies.extend(binaries.filter(resolution="pending"))
        if len(dependencies):
            print '  Found %d pending dependencies of %s' % (len(dependencies), unicode(bin))
        bin.linked_binary.clear()
        for dep in dependencies:
            bin.linked_binary.add(dep)

    print 'Done'


def main():
    usage = "usage: %prog [options] path/to/noan path/to/binary/stable /path/to/binary/test"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-r", "--release", dest="release",
                      help="use RELEASE as ditro version instead", metavar="RELEASE")
    parser.add_option("-i", "--ignore-redundant",
                      action="store_true", dest="ignore_redundant", default=False,
                      help="Ignore redundant binaries")

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

    updateDB(path_stable, 'stable', options)
    updateDB(path_test, 'test', options)


if __name__ == '__main__':
    main()
