#!/usr/bin/python
# -*- coding: utf-8 -*-

# DJANGO RELATED IMPORTS
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
# we use generic view for listing as it handles pagination easily. so we don't duplicate the code.
from django.views.generic.list_detail import object_list

# APP RELATED IMPORTS
from noan.repository.models import Distribution, Package, Source, Binary
# we have this wrapper to avoid using "context_instance" kwarg in every function.
from noan.wrappers import render_response
from noan.settings import SOURCE_PACKAGES_PER_PAGE, PENDING_PACKAGES_PER_PAGE

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


def page_pending_index(request):
    distributions = Distribution.objects.all()

    if len(distributions) == 1:
        dist = '%s/%s' % (distributions[0].name, distributions[0].release)
        return HttpResponseRedirect('/repository/pending/%s/' % dist)

    context = {
        'distributions': distributions,
    }
    return render_response(request, 'repository/pending/index.html', context)


def list_pending_packages(request, distName, distRelease):
    distribution = Distribution.objects.get(name=distName, release=distRelease)
    binaries = Binary.objects.filter(resolution='pending', package__source__distribution=distribution)

    # - generate dict to use in object_list
    # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
    object_dict = {
            'queryset': binaries,
            'paginate_by': PENDING_PACKAGES_PER_PAGE,
            'template_name': 'repository/source-packages-list.html',
            'template_object_name': 'binary_package'
            }

    return object_list(request, **object_dict)
