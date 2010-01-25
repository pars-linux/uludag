#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

# we use generic view for listing as it handles pagination easily. so we don't duplicate the code.
from django.views.generic.list_detail import object_list

from noan.repository.models import Distribution, Package, Source, Binary, TestResult

# we have this wrapper to avoid using "context_instance" kwarg in every function.
from noan.wrappers import render_response

from noan.settings import SOURCE_PACKAGES_PER_PAGE, PENDING_PACKAGES_PER_PAGE


def repository_index(request):
    distributions = Distribution.objects.all()

    context = {
        'distributions': distributions,
    }
    return render_response(request, 'repository/index.html', context)


def list_source_packages(request, distName, distRelease):
    sources = Source.objects.filter(distribution__name=distName, distribution__release=distRelease)
    if not sources.count() > 0:
        return HttpResponse("Not Found, 404")

    # - generate dict to use in object_list
    # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
    object_dict = {
            'queryset': sources,
            'paginate_by': SOURCE_PACKAGES_PER_PAGE,
            'template_name': 'repository/source-packages-list.html',
            'template_object_name': 'source'
            }

    return object_list(request, **object_dict)


# Details in <Source> section of the package
def view_source_detail(request, distName, distRelease, sourceName):
    """
        sourceName: <Source> section in pspec.xml
    """
    source = Source.objects.get(name=sourceName, distribution__name=distName, distribution__release=distRelease)

    context = {
        'source': source,
    }
    return render_response(request, 'repository/source.html', context)


# Details in <Package> section of the package
def view_package_detail(request, distName, distRelease, sourceName, packageName):
    """
        sourceName: <Source> section in pspec.xml
        packageName: <Package> section in pspec.xml
    """

    package = Package.objects.get(name=packageName, source__name=sourceName, source__distribution__name=distName, source__distribution__release=distRelease)

    context = {
        'package': package,
    }
    return render_response(request, 'repository/package.html', context)


def view_binary_detail(request, distName, distRelease, sourceName, packageName, binaryNo):
    """
        sourceName: <Source> section in pspec.xml
        packageName: <Package> section in pspec.xml
    """
    binary = Binary.objects.get(no=binaryNo, package__name=packageName, package__source__name=sourceName, package__source__distribution__name=distName, package__source__distribution__release=distRelease)

    # FIXME: We also handle sending ACK/NACK info. Maybe it can be done in different view?
    if request.method == "POST" and request.user and request.user.is_authenticated():
        # if this package is not updated by the latest updater, give error:
        #if binary.update.updated_by != request.user:
        #    return HttpResponse("Sorry, you can not change another developer's package. Only the developer who changed the package can give ACK.")

        if request.POST['result'] == "unknown":
            TestResult.objects.filter(binary=binary, created_by=request.user).delete()
        elif request.POST['result'] in ("yes", "no"):
            result, created = TestResult.objects.get_or_create(binary=binary, created_by=request.user)
            result.result = request.POST['result']
            result.save()

    user_result = "unknown"
    if request.user and request.user.is_authenticated():
        results = binary.testresult_set.filter(created_by=request.user)
        if len(results):
            user_result = results[0].result

    context = {
        'binary': binary,
        'user_result': user_result,
    }
    return render_response(request, 'repository/binary.html', context)


def page_pending_index(request):
    distributions = Distribution.objects.all()

    context = {
        'distributions': distributions,
    }
    return render_response(request, 'repository/pending/index.html', context)


def list_pending_packages(request, distName, distRelease):
    binaries = Binary.objects.filter(resolution='pending', package__source__distribution__name=distName, package__source__distribution__release=distRelease)

    # - generate dict to use in object_list
    # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
    object_dict = {
            'queryset': binaries,
            'paginate_by': PENDING_PACKAGES_PER_PAGE,
            'template_name': 'repository/pending/pending-packages-list.html',
            'template_object_name': 'binary_package',
            }

    return object_list(request, **object_dict)


def list_pending_packages_in_txt(request, distName, distRelease):
    binaries = Binary.objects.filter(resolution='pending', package__source__distribution__name=distName, package__source__distribution__release=distRelease)

    acked_packages = []
    nacked_packages = []
    not_tested_packages = []

    for binary in binaries:
        # if a binary has test a result, we should not list it.
        testresult = binary.get_result()
        if testresult == "unknown":
            not_tested_packages.append(binary)
        elif testresult == "yes":
            acked_packages.append(binary)
        else:
            nacked_packages.append(binary)

    data = "Packages for %s %s\n\n" % (distName, distRelease)
    data += "ACKed Packages:\n"
    data += "===============\n"
    for ack in acked_packages:
        data += "    %s (%s)\n" % (ack.package.name, ack.update.updated_by.get_full_name())
    data += "\nNACked Packages:\n"
    data += "================\n"
    for nack in nacked_packages:
        data += "    %s (%s)\n" % (nack.package.name, nack.update.updated_by.get_full_name())
    data += "\nNot Tested Packages:\n"
    data += "====================\n"
    for not_tested in not_tested_packages:
        data += "    %s (%s)\n" % (not_tested.package.name, not_tested.update.updated_by.get_full_name())

    return HttpResponse(data)


@login_required
def list_pending_packages_for_user(request, distName, distRelease):
    binaries = Binary.objects.filter(resolution='pending', package__source__distribution__name=distName, package__source__distribution__release=distRelease, update__updated_by=request.user)

    # - generate dict to use in object_list
    # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
    object_dict = {
            'queryset': binaries,
            'paginate_by': PENDING_PACKAGES_PER_PAGE,
            'template_name': 'repository/pending/pending-packages-list-for-user.html',
            'template_object_name': 'binary_package',
            }

    return object_list(request, **object_dict)
