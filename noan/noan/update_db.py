#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import pisi
import sys


def printUsage():
    print 'Usage: %s <path_to_noan> <path_to_stable> <path_to_test>' % sys.argv[0]
    sys.exit(1)


def updateDB(path_repo, repo_type):
    from django.contrib.auth.models import User
    from noan.repository.models import Distribution, Source, Package, Binary, Update

    if repo_type not in ['stable', 'test']:
        return

    def createUser(email, name):
        user = None
        first_name, last_name = name.rsplit(' ', 1)
        count = 1
        username = email.split('@')[0]
        while not user:
            try:
                user = User.objects.get(email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            except User.DoesNotExist:
                user = User(email=email, username=username, first_name=first_name, last_name=last_name)
                user.set_password(username)
                try:
                    user.save()
                except:
                    user = None
                    username += str(count)
                    count += 1
        return user

    # Get latest builds only
    packages_farm = {}
    for filename in os.listdir(path_repo):
        if not filename.endswith('.pisi'):
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

    total = len(files_new)
    index = 1
    for filename in files_new:
        fullpath = os.path.join(path_repo, filename)

        print '[%s/%s] %s' % (index, total, fullpath)

        pisi_file = pisi.package.Package(fullpath)
        pisi_meta = pisi_file.get_metadata()
        pisi_package = pisi_meta.package

        maintained_by = createUser(pisi_package.source.packager.email, pisi_package.source.packager.name)

        try:
            distribution = Distribution.objects.get(name=pisi_package.distribution, release=pisi_package.distributionRelease)
        except Distribution.DoesNotExist:
            distribution = Distribution(name=pisi_package.distribution, release=pisi_package.distributionRelease)
            distribution.save()

        try:
            source = Source.objects.get(name=pisi_package.source.name, distribution=distribution)
            source.maintained_by = maintained_by
            source.save()
        except Source.DoesNotExist:
            source = Source(name=pisi_package.source.name, distribution=distribution, maintained_by=maintained_by)
            source.save()

        try:
            package = Package.objects.get(name=pisi_package.name, source=source)
        except Package.DoesNotExist:
            package = Package(name=pisi_package.name, source=source)
            package.save()

        for up in pisi_package.history:
            if Update.objects.filter(no=up.release, source=source).count() == 0:
                updated_by = createUser(up.email, up.name)
                update = Update(no=up.release, source=source, version_no=up.version, updated_by=updated_by, updated_on=up.date, comment=up.comment)
                update.save()
            else:
                break

        if repo_type == 'test':
            resolution = 'pending'
        elif repo_type == 'stable':
            resolution = 'released'

        update = Update.objects.filter(source=source, no=pisi_package.history[0].release)[0]
        try:
            binary = Binary.objects.get(no=pisi_package.build, package=package)
        except Binary.DoesNotExist:
            binary = Binary(no=pisi_package.build, package=package, update=update, resolution=resolution)
            binary.save()

        if repo_type == 'test':
            # Mark other 'pending' binaries as 'reverted'
            binaries = Binary.objects.filter(package=package, resolution='pending', no__lt=binary.no)
            for bin in binaries:
                bin.resolution = 'reverted'
                bin.save()

        index += 1


def main():
    try:
        path_noan = sys.argv[1]
        path_stable = sys.argv[2]
        path_test = sys.argv[3]
    except:
        printUsage()

    os.environ['DJANGO_SETTINGS_MODULE'] = 'noan.settings'
    sys.path.insert(0, path_noan)
    try:
        import noan.settings
    except ImportError:
        printUsage()

    updateDB(path_stable, 'stable')
    updateDB(path_test, 'test')


if __name__ == '__main__':
    main()
