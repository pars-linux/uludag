#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

# we use generic view for listing as it handles pagination easily. so we don't duplicate the code.
from django.views.generic.list_detail import object_list

from noan.repository.models import Distribution, Package, Source, Binary, TestResult

from noan.repository.forms import SearchForm

# we have this wrapper to avoid using "context_instance" kwarg in every function.
from noan.wrappers import render_response

from noan.settings import SOURCE_PACKAGES_PER_PAGE, PENDING_PACKAGES_PER_PAGE

import urllib
import os
import pisi
import hashlib
from django.core.cache import cache
from django.db.models import Q

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

    LANGUAGE_CODE = request.LANGUAGE_CODE
    # - generate dict to use in object_list
    # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
    object_dict = {
            'queryset': sources,
            'paginate_by': SOURCE_PACKAGES_PER_PAGE,
            'template_name': 'repository/source-packages-list.html',
            'template_object_name': 'source',
            'extra_context': {'LANGUAGE_CODE': LANGUAGE_CODE}
            }

    return object_list(request, **object_dict)


# Details in <Source> section of the package
def view_source_detail(request, distName, distRelease, sourceName):
    """
        sourceName: <Source> section in pspec.xml
    """
    source = Source.objects.get(name=sourceName, distribution__name=distName, distribution__release=distRelease)

    LANGUAGE_CODE = request.LANGUAGE_CODE
    context = {
        'source': source,
        'LANGUAGE_CODE': LANGUAGE_CODE,
    }
    return render_response(request, 'repository/source.html', context)


# List of source packages that belong to a certain isA category
def view_isa_info(request, distName, distRelease, repoType, isA):
    """
        isA: <isA> section in pspec.xml
    """
    sources = Source.objects.filter(distribution__type=repoType, distribution__name=distName, distribution__release=distRelease, info__isa__name=isA)
    values = str(sources.values())
    id = hashlib.md5(values).hexdigest()
    if not sources.count() > 0:
        return HttpResponse("Not Found, 404")

    LANGUAGE_CODE = request.LANGUAGE_CODE
    # - generate dict to use in object_list
    # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
    if request.method == 'GET' and request.GET.get('page'):
        try:
            sources = cache.get(id)['tmp']
            # default timeout is 3600 sec, if the timeout is passed, return to the form page
        except TypeError:
            return HttpResponseRedirect('./')
    else:
        rslt = dict()
        rslt['tmp'] = sources
        cache.set(id, rslt)

    object_dict = {
            'queryset': sources,
            'paginate_by': SOURCE_PACKAGES_PER_PAGE,
            'template_name': 'repository/isa_partof_list.html',
            'template_object_name': 'source',
            'extra_context': {'LANGUAGE_CODE': LANGUAGE_CODE}
            }
    
    return object_list(request, **object_dict)


# List of source packages that belong to a certain partOf category
def view_partof_info(request, distName, distRelease, repoType, partOf):
    """
        partOf: <partOf> section in pspec.xml
    """
    sources = Source.objects.filter(distribution__type=repoType, distribution__name=distName, distribution__release=distRelease, info__part_of=partOf)
    values = str(sources.values())
    id = hashlib.md5(values).hexdigest()
    if not sources.count() > 0:
        return HttpResponse("Not Found, 404")

    LANGUAGE_CODE = request.LANGUAGE_CODE
    # - generate dict to use in object_list
    # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
    if request.method == 'GET' and request.GET.get('page'):
        try:
            sources = cache.get(id)['tmp']
            # default timeout is 3600 sec, if the timeout is passed, return to the form page
        except TypeError:
            return HttpResponseRedirect('./')
    else:
        rslt = dict()
        rslt['tmp'] = sources
        cache.set(id, rslt)

    object_dict = {
            'queryset': sources,
            'paginate_by': SOURCE_PACKAGES_PER_PAGE,
            'template_name': 'repository/isa_partof_list.html',
            'template_object_name': 'source',
            'extra_context': {'LANGUAGE_CODE': LANGUAGE_CODE}
            }

    return object_list(request, **object_dict)


# Details in <Package> section of the package
def view_package_detail(request, distName, distRelease, sourceName, packageName):
    """
        sourceName: <Source> section in pspec.xml
        packageName: <Package> section in pspec.xml
    """

    package = Package.objects.get(name=packageName, source__name=sourceName, source__distribution__name=distName, source__distribution__release=distRelease)

    LANGUAGE_CODE = request.LANGUAGE_CODE
    context = {
        'package': package,
        'LANGUAGE_CODE': LANGUAGE_CODE,
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
            result.result = request.POST.get('result', 'unknown')
            result.comment = request.POST.get('comment', '')
            result.save()

    user_result = None
    if request.user and request.user.is_authenticated():
        results = binary.testresult_set.filter(created_by=request.user)
        if len(results):
            user_result = results[0]

    # get the files of the pisi package
    # it is better to download the package from a local machine, it will be faster
    base_path = 'http://packages.pardus.org.tr'
    if binary.package.source.distribution.type == 'corporate':
        distro = 'corporate'
        release = '2'
        suffix = distro + release
    else:
        distro = binary.package.source.distribution.name.lower()
        release = binary.package.source.distribution.release
        suffix = "-".join([distro, release])
    if binary.resolution == 'pending': suffix += '-test'
    path = os.path.join(base_path, suffix)
    pisi_package = binary.get_filename()
    pisi_url = os.path.join(path, pisi_package)
    tmp_path = os.path.join('/tmp', pisi_package)
    url = urllib.URLopener()
    if os.path.exists(tmp_path): os.unlink(tmp_path)
    try:
        url.retrieve(pisi_url, tmp_path)
    except IOError:
        context = {
            'msg': _('The file you requested is not at the server. There may be an update.'),
        }
        return render_response(request, 'repository/404.html', context)

    package = pisi.package.Package(tmp_path)
    files = package.get_files()
    os.unlink(tmp_path)

    context = {
        'binary': binary,
        'user_result': user_result,
        'files': files,
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


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = request.POST.get('keyword', '')
            #source = request.POST.get('source', False)
            #binary = request.POST.get('binary', False)
            in_package = request.POST.get('in_package', 'Binary')
            summary = request.POST.get('summary', False)
            description = request.POST.get('description', False)
            dist_name = request.POST.get('dist_name', 'Pardus')
            dist_release = request.POST.get('dist_release', '2008')
            exact = request.POST.get('exact', '')

            unified_sources = None
            unified_binaries = None

            if in_package == 'Source':
                if exact:
                    sources = Source.objects.filter(name__exact=keyword)
                    unified_sources = sources
                else:
                    sources = Source.objects.filter(name__icontains=keyword)
                    summaries = Source.objects.filter(info__summary__id = -1)
                    descriptions = Source.objects.filter(info__description__id = -1)
                    if summary:
                        summaries = Source.objects.filter(info__summary__text__icontains=keyword)
                    if description: 
                        descriptions = Source.objects.filter(info__description__text__icontains=keyword)
                    unified_sources = sources | summaries | descriptions
                    # i need to find a better way here like using set
                    #s1 = set(sources).union(set(summaries).union(set(descriptions))
                unified_sources = unified_sources.filter(distribution__name__exact=dist_name)
                unified_sources = unified_sources.filter(distribution__release__exact=dist_release)
                unified_sources = unified_sources.distinct()

            if in_package == 'Binary':
                if exact:
                    binaries = Package.objects.filter(name__exact=keyword)
                    unified_binaries = binaries
                else:
                    binaries = Package.objects.filter(name__icontains=keyword)
                    summaries = Package.objects.filter(source__info__summary__id = -1)
                    descriptions = Package.objects.filter(source__info__description__id = -1)
                    if summary:
                        summaries = Package.objects.filter(source__info__summary__text__icontains=keyword)
                    if description: 
                        descriptions = Package.objects.filter(source__info__description__text__icontains=keyword)

                    unified_binaries = binaries | summaries | descriptions
                    unified_binaries = unified_binaries.distinct()

                unified_binaries =  unified_binaries.filter(source__distribution__name__exact=dist_name)
                unified_binaries =  unified_binaries.filter(source__distribution__release__exact=dist_release)

            if unified_sources and not unified_binaries:
                result = unified_sources
                sources_len = unified_sources.count()
                binary_len = 0
            elif unified_binaries and not unified_sources:
                result = unified_binaries
                binary_len = unified_binaries.count()
                sources_len = 0
            else:
                # create an empty result
                result = Source.objects.filter(id=-1)
                sources_len = result.count()
                binary_len = 0

            sources_len = str(sources_len)
            binary_len = str(binary_len)

            # create unique ids for the cache query result
            values = str(result.values())
            result_id = hashlib.md5(values).hexdigest()
            request.session['result_id'] = result_id

            sources_len_id = hashlib.md5(sources_len).hexdigest()
            request.session['sources_len_id'] = sources_len_id
            binary_len_id = hashlib.md5(binary_len).hexdigest()
            request.session['binary_len_id'] = binary_len_id

            # set the result to the db, pagination will use results from cache when the GET request is called
            # saving the result at the dictionary is a workaround, it is nto possible to save the queryset object directly at the db
            rslt = dict()
            rslt['tmp'] = result
            cache.set(result_id, rslt)
            cache.set(sources_len_id, sources_len)
            cache.set(binary_len_id, binary_len)

            LANGUAGE_CODE = request.LANGUAGE_CODE
            # - generate dict to use in object_list
            # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
            object_dict = {
                'queryset': result,
                'paginate_by': SOURCE_PACKAGES_PER_PAGE,
                'template_name': 'repository/search_result.html',
                'template_object_name': 'packages',
                'extra_context': {'LANGUAGE_CODE': LANGUAGE_CODE, 'sources_len': sources_len, 'binary_len': binary_len}
                }

            return object_list(request, **object_dict)

    elif request.method == 'GET' and request.GET.get('page'):

        result_id = request.session.get('result_id')

        try:
            result = cache.get(result_id)['tmp']
            # default timeout is 3600 sec, if the timeout is passed, return to the form page
        except TypeError:
            return HttpResponseRedirect('./')

        sources_len_id = request.session.get('sources_len_id')
        binary_len_id = request.session.get('binary_len_id')

        sources_len = cache.get(sources_len_id)
        binary_len = cache.get(binary_len_id)
        LANGUAGE_CODE = request.LANGUAGE_CODE
        # - generate dict to use in object_list
        # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
        object_dict = {
            'queryset': result,
            'paginate_by': SOURCE_PACKAGES_PER_PAGE,
            'template_name': 'repository/search_result.html',
            'template_object_name': 'packages',
            'extra_context': {'LANGUAGE_CODE': LANGUAGE_CODE, 'sources_len': sources_len, 'binary_len': binary_len}
        }
        
        return object_list(request, **object_dict)

    else:
        form = SearchForm()

    context = {
            'form': form,
        }

    return render_response(request, 'repository/search.html', context)

def orphan(request):
    distributions = Distribution.objects.all()

    context = {
            'distributions': distributions,
        }

    return render_response(request, 'repository/orphan.html', context)

def list_orphan_packages(request, distName, distRelease):
    distribution = Distribution.objects.get(name=distName, release=distRelease)
    result = distribution.get_orphan_list(distribution.name, distribution.release)
    values = str(result.values())
    id = hashlib.md5(values).hexdigest()
    
    if request.method == 'GET' and request.GET.get('page'):
        try:
            result = cache.get(id)['tmp']
            # default timeout is 3600 sec, if the timeout is passed, return to the form page
        except TypeError:
            return HttpResponseRedirect('./')
    else:
        rslt = dict()
        rslt['tmp'] = result
        cache.set(id, rslt)
   
    LANGUAGE_CODE = request.LANGUAGE_CODE
    object_dict = {
        'queryset': result,
        'paginate_by': SOURCE_PACKAGES_PER_PAGE,
        'template_name': 'repository/source-packages-list.html',
        'template_object_name': 'source',
        'extra_context': {'LANGUAGE_CODE': LANGUAGE_CODE}
    }
    
    return object_list(request, **object_dict)
