#!/usr/bin/python
# -*- coding: utf-8 -*-

import bz2
import optparse
import os.path
import string
import sys
import urllib2

try:
    import pisi
    from pisi.version import Version as Pisi_Version
except ImportError:
    print 'Unable to import module "pisi". Not using Pardus?'
    sys.exit(1)


def toString(obj):
    if not obj:
        return ''
    return str(obj)

def toInt(obj):
    if not obj:
        return 0
    try:
        return int(obj)
    except ValueError:
        return 0

nickmap = {
    u"ğ": u"g",
    u"ü": u"u",
    u"ş": u"s",
    u"ı": u"i",
    u"ö": u"o",
    u"ç": u"c",
    u"Ğ": u"g",
    u"Ü": u"u",
    u"Ş": u"s",
    u"İ": u"i",
    u"Ö": u"o",
    u"Ç": u"c",
}

def convert(name):
    name = unicode(name).lower()
    text = ""
    for c in name:
        if c in string.ascii_letters:
            text += c
        else:
            c = nickmap.get(c, None)
            if c:
                text += c
    return text

def fetchIndex(target, tmp="/tmp"):
    if target.endswith("pisi-index.xml"):
        filetype = "xml"
    elif target.endswith("pisi-index.xml.bz2"):
        filetype = "bz2"
    else:
        target += "pisi-index.xml.bz2"
        filetype = "bz2"

    url = urllib2.urlopen(target)
    data = url.read()

    if filetype == "bz2":
        data = bz2.decompress(data)

    filename = os.path.join(tmp, "pisi-index-noan")
    file(filename, "w").write(data)

    ix = pisi.index.Index(filename)

    os.unlink(filename)

    return ix

def updateDB(path_source, path_stable, path_test, options):
    from django.contrib.auth.models import User
    from noan.repository.models import Distribution, Source, Package, Binary, Update, BuildDependency, RuntimeDependency, Replaces
    from noan.profile.models import Profile

    def createUser(email, name):
        user = None
        if ' ' in name:
            first_name, last_name = name.rsplit(' ', 1)
        else:
            first_name = name
            last_name = ''
        username = convert(name.replace(' ', '.'))
        try:
            user = User.objects.get(username=username)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except User.DoesNotExist:
            user = User(email=email, username=username, first_name=first_name, last_name=last_name)
            print '    New developer: %s' % username
            user.save()
        return user

    def parseSourceIndex(_index):
        distroName, distroRelease = _index.distribution.sourceName.split('-', 1)
        print '  Distribution: %s-%s' % (distroName, distroRelease)

        # Add distribution to database
        try:
            distribution = Distribution.objects.get(name=distroName, release=distroRelease)
        except Distribution.DoesNotExist:
            distribution = Distribution(name=distroName, release=distroRelease)
            distribution.save()

        def importSpec(pspec):
            # Add or update developer
            maintained_by = createUser(pspec.source.packager.email, pspec.source.packager.name)

            # Add source or update maintainer
            try:
                source = Source.objects.get(name=pspec.source.name, distribution=distribution)
                source.maintained_by = maintained_by
                source.save()
            except Source.DoesNotExist:
                source = Source(name=pspec.source.name, distribution=distribution, maintained_by=maintained_by)
                source.save()
            print '  Source: %s' % source.name

            # Update build dependencies
            for dep in BuildDependency.objects.filter(source=source):
                dep.delete()
            for dep in pspec.source.buildDependencies:
                dependency = BuildDependency(source=source, name=dep.package, version=toString(dep.version), version_to=toString(dep.versionTo), version_from=toString(dep.versionFrom), release=toInt(dep.release), release_to=toInt(dep.releaseTo), release_from=toInt(dep.releaseFrom))
                dependency.save()

            # Add or update package info
            for pack in pspec.packages:
                try:
                    package = Package.objects.get(name=pack.name, source=source)
                    package.save()
                except Package.DoesNotExist:
                    package = Package(name=pack.name, source=source)
                    package.save()
                    print '    New package: %s' % package.name

                for rep in pack.replaces:
                    replaces = Replaces(name=str(rep), package=package)
                    replaces.save()
                    for bin in Binary.objects.filter(package__name=str(rep), package__source__distribution=distribution):
                        bin.resolution = 'removed'
                        bin.save()
                        print '    Marking %s-%s as removed' % (rep, bin.build)

                # Update runtime dependencies
                for dep in RuntimeDependency.objects.filter(package=package):
                    dep.delete()
                for dep in pack.runtimeDependencies():
                    if isinstance(dep, pisi.specfile.AnyDependency):
                        # Any dependencies
                        for any_dep in dep.dependencies:
                            dependency = RuntimeDependency(package=package, name=any_dep.package, version=toString(any_dep.version), version_to=toString(any_dep.versionTo), version_from=toString(any_dep.versionFrom), release=toInt(any_dep.release), release_to=toInt(any_dep.releaseTo), release_from=toInt(any_dep.releaseFrom))
                            dependency.save()
                    else:
                        dependency = RuntimeDependency(package=package, name=dep.package, version=toString(dep.version), version_to=toString(dep.versionTo), version_from=toString(dep.versionFrom), release=toInt(dep.release), release_to=toInt(dep.releaseTo), release_from=toInt(dep.releaseFrom))
                        dependency.save()

            up_count = 0
            for up in pspec.history:
                updated_by = createUser(up.email, up.name)
                try:
                    update = Update.objects.get(no=up.release, source=source)
                    update.updated_on = up.date
                    update.updated_by = updated_by
                    #update.version_no = up.version_no
                    update.comment = up.comment
                    update.save()
                except Update.DoesNotExist:
                    update = Update(no=up.release, source=source, version_no=up.version, updated_by=updated_by, updated_on=up.date, comment=up.comment)
                    update.save()
                    up_count += 1
            if up_count > 0:
                print '    New Updates: %s' % up_count

        for pspec in _index.specs:
            importSpec(pspec)

    def parseBinaryIndex(_index, _type):
        if _type == 'test':
            resolution = 'pending'
        elif _type == 'stable':
            resolution = 'released'

        distroName, distroRelease = _index.distribution.sourceName.split('-', 1)
        print '  Distribution: %s-%s' % (distroName, distroRelease)

        # Add distribution to database
        try:
            distribution = Distribution.objects.get(name=distroName, release=distroRelease)
        except Distribution.DoesNotExist:
            return

        def importPackage(pisi_package):
            try:
                source = Source.objects.get(name=pisi_package.source.name, distribution=distribution)
            except Source.DoesNotExist:
                return

            try:
                package = Package.objects.get(name=pisi_package.name, source=source)
            except Package.DoesNotExist:
                return

            updates = Update.objects.filter(source=source, no=pisi_package.history[0].release)
            if len(updates) == 0:
                return

            update = updates[0]
            try:
                binary = Binary.objects.get(no=pisi_package.build, package=package)
                if _type == 'stable' and binary.resolution == 'pending':
                    binary.resolution = 'released'
                    binary.save()
                    print '  Marking %s-%s as %s' % (package.name, pisi_package.build, binary.resolution)
            except Binary.DoesNotExist:
                binary = Binary(no=pisi_package.build, package=package, update=update, resolution=resolution)
                binary.save()
                print '  Marking %s-%s as %s' % (package.name, pisi_package.build, binary.resolution)

            if _type == 'test':
                # Mark other 'pending' binaries as 'reverted'
                binaries = Binary.objects.filter(package=package, resolution='pending', no__lt=binary.no)
                for bin in binaries:
                    bin.resolution = 'reverted'
                    bin.save()
                    print '  Marking %s-%s as %s' % (package.name, bin.build, bin.resolution)

        for pack in _index.packages:
            importPackage(pack)

        # Write pending dependencies of a package to it's model
        if _type != 'test':
            return
        for bin in Binary.objects.filter(resolution='pending'):
            dependencies = []
            for dep in bin.package.runtimedependency_set.all():
                binaries = Binary.objects.filter(package__source__distribution = bin.package.source.distribution, package__name=dep.name)
                #
                if binaries.filter(resolution="released").count() == 0:
                    dependencies.extend(binaries.filter(resolution="pending"))
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

                # release
                if dep.release != 0 and binaries.filter(update__no=dep.release, resolution="released").count() == 0:
                    dependencies.extend(binaries.filter(resolution="pending"))
                elif dep.release_from != 0 and binaries.filter(update__no__gte=dep.release, resolution="released").count() == 0:
                    dependencies.extend(binaries.filter(resolution="pending"))
                elif dep.release_to != 0 and binaries.filter(update__no__lte=dep.release, resolution="released").count() == 0:
                    dependencies.extend(binaries.filter(resolution="pending"))

            dependencies = set(dependencies)

            if len(dependencies):
                print '  Found %d pending dependencies of %s' % (len(dependencies), unicode(bin))
            bin.linked_binary.clear()
            for dep in dependencies:
                bin.linked_binary.add(dep)

    # Indexes
    print "Fetching source index..."
    index_source = fetchIndex(path_source)

    print "Fetching stable (binary) index..."
    index_stable = fetchIndex(path_stable)

    if path_test:
        print "Fetching test (binary) index..."
        index_test = fetchIndex(path_test)
    else:
        index_test = None

    # Parse source indes
    print "Parsing source index..."
    parseSourceIndex(index_source)
    # Parse test (binary) index for new packages
    if index_test:
        parseBinaryIndex(index_test, "test")
    # Parse stable (binary) index for released packages
    parseBinaryIndex(index_stable, "stable")


def main():
    usage = "usage: %prog [options] path/to/noan http://url.to/source-repo http://url.to/stable-repo [http://url.to/test-repo]"
    parser = optparse.OptionParser(usage=usage)

    (options, args) = parser.parse_args()

    if len(args) == 4:
        path_noan, path_source, path_stable, path_test = args
    elif len(args) == 3:
        path_noan, path_source, path_stable = args
        path_test = None
    else:
        parser.error("Incorrect number of arguments")

    os.environ['DJANGO_SETTINGS_MODULE'] = 'noan.settings'
    sys.path.insert(0, path_noan)
    try:
        import noan.settings
    except ImportError:
        parser.error('Noan path is invalid.')

    updateDB(path_source, path_stable, path_test, options)


if __name__ == '__main__':
    main()
