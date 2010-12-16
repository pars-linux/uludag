#!/usr/bin/python
# -*- coding: utf-8 -*-

import bz2
import optparse
import os.path
import random
import string
import sys
import urllib2
import datetime

try:
    import pisi
    from pisi.version import Version as Pisi_Version
except ImportError:
    print 'Unable to import module "pisi". Not using Pardus?'
    sys.exit(1)


MAIL_SUBJECT = "NOAN Developer Account: %(username)s"
MAIL_BODY = """Hello %(name)s,

Your developer account password for NOAN package management system is:

    %(password)s

Cheers,
NOAN - http://noan.pardus.org.tr/noan/
"""


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
    from django.core.mail import send_mail
    from django.contrib.auth.models import User
    from noan.repository.models import Distribution, Source, Package, Binary, Update, BuildDependency, RuntimeDependency, Replaces, SourcePackageDetail, IsA, License, Summary, Description, BinaryPackageDetail, ReviewInfo
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
            password = ''.join([random.choice("1234567890qwertyupasdfghjklizxcvbnm") for x in range(8)])
            user.set_password(password)
            user.save()
            print '    New developer: %s' % username
            # E-mail password
            data = {"username": username, "password": password, "name": name, "email": email}
            #send_mail(MAIL_SUBJECT % data, MAIL_BODY % data, 'no-reply@pardus.org.tr', [email])
        return user

    def parseSourceIndex(_index, review=False, traverse_time=False):
        if not review:
            try:
                distroName, distroRelease = _index.distribution.sourceName.split('-', 1)
            except ValueError:
                distroName = _index.distribution.sourceName
                distroRelease = _index.distribution.version
            print '  Distribution: %s-%s' % (distroName, distroRelease)

            # repo name
            try:
                if _index.distribution.sourceName.find(" ") != -1:
                    binaryName = _index.distribution.sourceName.split()[1]
                else:
                    binaryName = _index.distribution.sourceName.split('-', 1)[1]
            except IndexError:
                if _index.distribution.binaryName == 'Contrib': binaryName = 'Contrib'
                else: binaryName = 'Pardus'
            if binaryName == 'Contrib': repoType = 'contrib'
            elif binaryName == 'Corporate': repoType = 'corporate'
            else: repoType = 'stable'
        else:
            distroName = "Pardus"
            distroRelease = "Playground"
            repoType = "review"

        # Add distribution to database
        try:
            distribution = Distribution.objects.get(name=distroName, release=distroRelease, type=repoType)
        except Distribution.DoesNotExist:
            distribution = Distribution(name=distroName, release=distroRelease, type=repoType)
            distribution.save()

        def importSpec(pspec, local_uri=None):
            # Add or update developer
            maintained_by = createUser(pspec.source.packager.email, pspec.source.packager.name)
            review_flag = False
            # Create the source package information
            part_of = pspec.source.partOf
            if not local_uri:
                source_uri = pspec.source.sourceURI
            else:
                index = local_uri.find("review")
                source_uri = local_uri[index:]
                review_flag = True
            print '     Source URI: %s' % source_uri

            home_page = pspec.source.homepage
            print '     Homepage: %s' % home_page
            source_info = SourcePackageDetail.objects.create(part_of=part_of, source_uri=source_uri, home_page=home_page)
            for is_a in pspec.source.isA:
                print '     IsA: %s' % is_a
                source_info.isa_set.create(name=is_a)
            for license in pspec.source.license:
                print '     License: %s' % license
                source_info.license_set.create(name=license)
            summary = pspec.source.summary
            for language in summary.keys():
                print '     Summary Language: %s' % language
                print '     Summary Text: %s' % summary[language]
                source_info.summary_set.create(language=language, text=summary[language])
            description = pspec.source.description
            for language in description.keys():
                print '     Description Language: %s' % language
                print '     Description Text: %s' % description[language]
                source_info.description_set.create(language=language, text=description[language])

            # Add source or update maintainer
            try:
                source = Source.objects.get(name=pspec.source.name, distribution=distribution)
                source.maintained_by = maintained_by
                source.info = source_info
            except Source.DoesNotExist:
                source = Source(name=pspec.source.name, distribution=distribution, maintained_by=maintained_by, info=source_info)
            print '  Source: %s' % source.name

            # Save the traverse time of the review path for the next check
            if review_flag:
                review = ReviewInfo.objects.create(check_time=traverse_time,status=True)
            else:
                review = ReviewInfo.objects.create(status=False)
            source.review = review
            source.save()

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
                        print '    Marking %s-%s as removed' % (rep, bin.no)

                # Update runtime dependencies
                for dep in RuntimeDependency.objects.filter(package=package):
                    dep.delete()
                for dep in pack.runtimeDependencies():
                    try:
                        if isinstance(dep, pisi.specfile.AnyDependency):
                            # Any dependencies
                            for any_dep in dep.dependencies:
                                dependency = RuntimeDependency(package=package, name=any_dep.package, version=toString(any_dep.version), version_to=toString(any_dep.versionTo), version_from=toString(any_dep.versionFrom), release=toInt(any_dep.release), release_to=toInt(any_dep.releaseTo), release_from=toInt(any_dep.releaseFrom))
                                dependency.save()
                        else:
                            dependency = RuntimeDependency(package=package, name=dep.package, version=toString(dep.version), version_to=toString(dep.versionTo), version_from=toString(dep.versionFrom), release=toInt(dep.release), release_to=toInt(dep.releaseTo), release_from=toInt(dep.releaseFrom))
                            dependency.save()
                    except:
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

        if not review:
            for pspec in _index.specs:
                importSpec(pspec)
        else:
            pspec = pisi.specfile.SpecFile(_index)
            importSpec(pspec, local_uri=_index)

    def parseBinaryIndex(_index, _type):
        if _type == 'test':
            resolution = 'pending'
        elif _type == 'stable':
            resolution = 'released'

        try:
            distroName, distroRelease = _index.distribution.sourceName.split('-', 1)
        except ValueError:
            distroName = _index.distribution.sourceName
            distroRelease = _index.distribution.version
        print '  Distribution: %s-%s' % (distroName, distroRelease)
        
        # repo name
        try:
            if _index.distribution.sourceName.find(" ") != -1:
                binaryName = _index.distribution.sourceName.split()[1]
            else:
                binaryName = _index.distribution.sourceName.split('-', 1)[1]
        except IndexError:
            if _index.distribution.binaryName == 'Contrib': binaryName = 'Contrib'
            else: binaryName = 'Pardus'
        if binaryName == 'Contrib': repoType = 'contrib'
        elif binaryName == 'Corporate': repoType = 'corporate'
        else: repoType = 'stable'

        # Add distribution to database
        try:
            distribution = Distribution.objects.get(name=distroName, release=distroRelease, type=repoType)
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

            # Create the binary package information
            binary_info = BinaryPackageDetail.objects.create(architecture=pisi_package.architecture, installed_size=int(pisi_package.installedSize), package_size=int(pisi_package.packageSize), package_hash=pisi_package.packageHash)

            update = updates[0]
            release = pisi_package.history[0].release
            try:
                binary = Binary.objects.get(no=release, package=package)
                if binary.info == binary_info: binary_info.delete()
                else: binary.info = binary_info
                if _type == 'stable' and binary.resolution == 'pending':
                    binary.resolution = 'released'
                    binary.save()
                    print '  Marking %s-%s as %s' % (package.name, release, binary.resolution)
            except Binary.DoesNotExist:
                binary = Binary(no=release, package=package, update=update, resolution=resolution, info=binary_info)
                binary.save()
                print '  Marking %s-%s as %s' % (package.name, release, binary.resolution)
            print '     Architecture: %s' % (binary.info.architecture)
            print '     Installed Size: %s' % (binary.info.installed_size)
            print '     Package Size: %s' % (binary.info.package_size)
            print '     Hash: %s' % (binary.info.package_hash)

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


    def removeDeletedReview(traverse_time):
        sources = Source.objects.filter(review__status = True).exclude(review__check_time = traverse_time)
        for source in sources:
            #print "Deleting distribution information"
            #source.distribution.delete()
            #print "Deleting maintainer information"
            #source.maintained_by.delete()
            print "Deleting source details"
            source.info.delete()
            print "Deleting review details"
            source.review.delete()
            # delete also packages if any exist
            print "Deleting package information"
            packages = source.package_set.all()
            for package in packages:
                package.delete()
            print "Deleting source itself"
            source.delete()


    # Indexes
    if options.type != "review":
        print "Fetching source index..."
        index_source = fetchIndex(path_source)

    if path_stable:
        print "Fetching stable (binary) index..."
        index_stable = fetchIndex(path_stable)
    else:
        index_stable = None

    if path_test:
        print "Fetching test (binary) index..."
        index_test = fetchIndex(path_test)
    else:
        index_test = None

    # Parse source indes
    print "Parsing source index..."
    if options.type == "review":
        current_time = datetime.datetime.now()
        # start traversing reviwe svn directory structure
        print "Traversing the review svn directory..."
        for root, dirs, files in os.walk(path_source):
            if "pspec.xml" in files:
                for f in files:
                    if f == "pspec.xml":
                        pspec_path = os.path.join(root, "pspec.xml")
                        print "Parsing %s " % pspec_path
                        parseSourceIndex(pspec_path, review=True, traverse_time=current_time)
        removeDeletedReview(traverse_time=current_time)
    else:
        parseSourceIndex(index_source)

    # Parse test (binary) index for new packages
    if index_test:
        parseBinaryIndex(index_test, "test")
    if index_stable:
        # Parse stable (binary) index for released packages
        parseBinaryIndex(index_stable, "stable")


def main():
    usage = "usage: %prog [options] path/to/noan http://url.to/source-repo http://url.to/stable-repo [http://url.to/test-repo]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-t", "--type",
                      action="store",
                      dest="type",
                      type="string",
                      help="Review path will be traversed")
    (options, args) = parser.parse_args()

    if len(args) == 4:
        path_noan, path_source, path_stable, path_test = args
    elif len(args) == 3:
        path_noan, path_source, path_stable = args
        path_test = None
    elif len(args) == 2:
        path_noan, path_source = args
        path_stable, path_test = None, None
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
