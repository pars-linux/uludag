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

try:
    import pysvn
except ImportError:
    print 'Unable to import module "pysvn".'
    sys.exit(1)

def findSpecs(folder):
    specs = []
    for root, dirs, files in os.walk(folder):
        if 'pspec.xml' in files:
            specs.append(root)
        if '.svn' in dirs:
            dirs.remove(".svn")
    return specs

def updateDB(path_source, full_import, newRelease):
    from django.contrib.auth.models import User
    from noan.repository.models import Distribution, Source, Package, Binary, Update

    def createUser(email, name):
        user = None
        if ' ' in name:
            first_name, last_name = name.rsplit(' ', 1)
        else:
            first_name = name
            last_name = ''
        count = 1
        username = email.split('@')[0]
        while not user:
            try:
                user = User.objects.get(first_name=first_name, last_name=last_name)
            except User.DoesNotExist:
                user = User(email=email, username=username, first_name=first_name, last_name=last_name)
                user.set_password(username)
                try:
                    user.save()
                except:
                    user = None
                    username += str(count)
                    count += 1
                    continue
                print '    New developer: %s' % name
        return user

    print 'Scanning %s...' % path_source

    distroFile = os.path.join(path_source, 'distribution.xml')
    distro = pisi.component.Distribution(distroFile)
    distroName, distroRelease = distro.sourceName.rsplit('-', 1)
    distroRelease = distro.version
    if newRelease:
        distroRelease = newRelease
    print '  Distribution: %s-%s' % (distroName, distroRelease)

    try:
        distribution = Distribution.objects.get(name=distroName, release=distroRelease)
    except Distribution.DoesNotExist:
        distribution = Distribution(name=distroName, release=distroRelease)
        distribution.save()

    def importSpec(_spec):
        print '  Importing %s' % _spec
        pspec = pisi.specfile.SpecFile(_spec)

        maintained_by = createUser(pspec.source.packager.email, pspec.source.packager.name)

        try:
            source = Source.objects.get(name=pspec.source.name, distribution=distribution)
            source.maintained_by = maintained_by
            source.save()
        except Source.DoesNotExist:
            source = Source(name=pspec.source.name, distribution=distribution, maintained_by=maintained_by)
            source.save()
            print '    New source: %s' % source.name

        for pack in pspec.packages:
            try:
                package = Package.objects.get(name=pack.name, source=source)
                package.save()
            except Package.DoesNotExist:
                package = Package(name=pack.name, source=source)
                package.save()
                print '    New package: %s' % package.name

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

    cli = pysvn.Client()

    if full_import:
        cli.update(path_source)
        specDirs = findSpecs(path_source)
        for dir in specDirs:
            importSpec(os.path.join(dir, 'pspec.xml'))
    else:
        def cbNotify(_info):
            action = _info['action']
            path = _info['path']
            if path.endswith('pspec.xml'):
                if action in [pysvn.wc_notify_action.update_add, pysvn.wc_notify_action.update_update]:
                    importSpec(path)
        cli.callback_notify = cbNotify
        cli.update(path_source)

def main():
    usage = "usage: %prog [options] path/to/noan path/to/repo/source"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-r", "--release", dest="release",
                      help="use RELEASE as ditro version instead", metavar="RELEASE")
    parser.add_option("-u", "--update",
                      action="store_false", dest="full", default=True,
                      help="update changed files only")

    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Incorrect number of arguments")

    path_noan, path_source = args

    os.environ['DJANGO_SETTINGS_MODULE'] = 'noan.settings'
    sys.path.insert(0, path_noan)
    try:
        import noan.settings
    except ImportError:
        parser.error('Noan path is invalid.')

    updateDB(path_source, options.full, options.release)


if __name__ == '__main__':
    main()
