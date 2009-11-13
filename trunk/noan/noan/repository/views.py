#!/usr/bin/python
# -*- coding: utf-8 -*-

##########################
#                        #
# Django related imports #
#                        #
##########################

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

#######################
#                     #
# App related imports #
#                     #
#######################
from noan.repository.models import Distribution, Package, Source, Binary
# we have this wrapper to avoid using "context_instance" kwarg in every function.
from noan.wrappers import render_response

def repository_index(request):
    distributions = Distribution.objects.all()

    # If there is only one repository, redirect it to that
    # Or list available distributios
    if len(distributions) == 1:
        return HttpResponseRedirect(distributions[0].get_url())

    context = {
        'distributions': distributions,
    }
    return render_response(request, 'repository/index.html', context)


def list_source_packages(request, distName, distRelease):
    distribution = Distribution.objects.get(name=distName, release=distRelease)

    sources = Source.objects.filter(distribution=distribution)

    # Pagination
    paginator = Paginator(sources, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        sources = paginator.page(page)
    except (EmptyPage, InvalidPage):
        sources = paginator.page(paginator.num_pages)

    context = {
        'sources': sources,
    }
    return render_response(request, 'repository/source-packages-list.html', context)


# Details in <Source> section of the package
def view_source_detail(request, distName, distRelease, sourceName):
    """
        sourceName: <Source> section in pspec.xml
    """
    distribution = Distribution.objects.get(name=distName, release=distRelease)
    source = Source.objects.get(name=sourceName, distribution=distribution)

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

    distribution = Distribution.objects.get(name=distName, release=distRelease)
    source = Source.objects.get(name=sourceName, distribution=distribution)
    package = Package.objects.get(name=packageName, source=source)

    context = {
        'package': package,
    }
    return render_response(request, 'repository/package.html', context)

def view_binary_detail(request, distName, distRelease, sourceName, packageName, binaryNo):
    """
        sourceName: <Source> section in pspec.xml
        packageName: <Package> section in pspec.xml
    """

    distribution = Distribution.objects.get(name=distName, release=distRelease)
    source = Source.objects.get(name=sourceName, distribution=distribution)
    package = Package.objects.get(name=packageName, source=source)
    binary = Binary.objects.get(no=binaryNo, package=package)

    # FIXME: We also handle sending ACK/NACK info. Maybe it can be done in different view?
    if request.method == "POST" and request.user and request.user.is_authenticated():
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


##############################
#                            #
# Views for pending packages #
#                            #
##############################

def page_pending_index(request):
    distributions = Distribution.objects.all()

    if len(distributions) == 1:
        dist = '%s-%s' % (distributions[0].name, distributions[0].release)
        return HttpResponseRedirect('/repository/pending/%s/' % dist)

    context = {
        'distributions': distributions,
    }
    return render_response(request, 'repository/pending/index.html', context)


def list_pending_packages(request, distName, distRelease):
    distribution = Distribution.objects.get(name=distName, release=distRelease)

    binaries = Binary.objects.filter(resolution='pending', package__source__distribution=distribution)

    # Pagination
    paginator = Paginator(binaries, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        binaries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        binaries = paginator.page(paginator.num_pages)

    context = {
        'binaries': binaries,
    }
    return render_response(request, 'repository/pending/pending-packages-list.html', context)

