from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson
from django.template import RequestContext
from noan.repository.models import *


from django.core.paginator import Paginator, InvalidPage, EmptyPage

def page_index(request, distName=None):
    if distName:
        distributions = Distribution.objects.filter(name=distName)
    else:
        distributions = Distribution.objects.all()

    context = {
        'distributions': distributions,
    }
    return render_to_response('repository/index.html', context, context_instance=RequestContext(request))


def page_sources(request, distName, distRelease):
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
    return render_to_response('repository/sources.html', context, context_instance=RequestContext(request))


def page_source(request, distName, distRelease, sourceName):
    distribution = Distribution.objects.get(name=distName, release=distRelease)
    source = Source.objects.get(name=sourceName, distribution=distribution)

    context = {
        'source': source,
    }
    return render_to_response('repository/source.html', context, context_instance=RequestContext(request))


def page_package(request, distName, distRelease, sourceName, packageName):
    distribution = Distribution.objects.get(name=distName, release=distRelease)
    source = Source.objects.get(name=sourceName, distribution=distribution)
    package = Package.objects.get(name=packageName, source=source)

    context = {
        'package': package,
    }
    return render_to_response('repository/package.html', context, context_instance=RequestContext(request))


def page_binary(request, distName, distRelease, sourceName, packageName, binaryNo):
    distribution = Distribution.objects.get(name=distName, release=distRelease)
    source = Source.objects.get(name=sourceName, distribution=distribution)
    package = Package.objects.get(name=packageName, source=source)
    binary = Binary.objects.get(no=binaryNo, package=package)

    context = {
        'binary': binary,
    }
    return render_to_response('repository/binary.html', context, context_instance=RequestContext(request))


def page_pending(request):
    binaries = Binary.objects.filter(resolution='pending')

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
    return render_to_response('repository/pending.html', context, context_instance=RequestContext(request))


"""
def releases(request, maintainer='*', resolution='*', ajax=False):
    if maintainer == '*':
        releases = Release.objects.all()
    else:
        releases = Release.objects.filter(Q(package__maintained_by__username=maintainer) | Q(updated_by__username=maintainer))

    if resolution != '*':
        releases = releases.filter(resolution=resolution)

    releases = releases.order_by('package__name')

    paginator = Paginator(releases, 25)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        releases = paginator.page(page)
    except (EmptyPage, InvalidPage):
        releases = paginator.page(paginator.num_pages)

    if ajax:
        context = {
            'releases': [unicode(x) for x in releases.object_list],
            'page': page,
            'page_total': paginator.num_pages,
        }
        return HttpResponse(simplejson.dumps(context))
    else:
        context = {
            'releases': releases,
            'users': User.objects.all(),
            'maintainer': maintainer,
            'resolutions': RELEASE_RESOLUTIONS,
            'resolution': resolution,
        }
        return render_to_response('repository/releases.html', context, context_instance=RequestContext(request))


def ajax_releases(request, maintainer='*', resolution='*'):
    return releases(request, maintainer, resolution, True)


def package(request, packageName):
    package = Package.objects.get(name=packageName)
    language = request.LANGUAGE_CODE.split('-')[0]
    context = {
        'package': package,
    }
    return render_to_response('repository/package.html', context, context_instance=RequestContext(request))


def release(request, packageName, version):
    build_no = version.rsplit('-', 1)[-1]
    package = Package.objects.get(name=packageName)
    release = Release.objects.get(package=package, build_no=build_no)
    cases = []
    for case in package.testcase_set.all():
        reports_yes = release.testresult_set.filter(case=case, result='yes').count()
        reports_no = release.testresult_set.filter(case=case, result='no').count()
        reports = release.testresult_set.filter(case=case)
        cases.append({'id': case.id, 'description': case.description(), 'reports': reports, 'yes': reports_yes, 'no': reports_no})
    context = {
        'package': package,
        'release': release,
        'cases': cases,
    }
    return render_to_response('repository/release.html', context, context_instance=RequestContext(request))


@login_required
def vote(request, packageName, version, result, caseNo):
    if result in ['yes', 'no']:
        build_no = version.rsplit('-', 1)[-1]
        case = TestCase.objects.get(id=caseNo)
        package = Package.objects.get(name=packageName)
        release = Release.objects.get(package=package, build_no=build_no)
        try:
            test_result = TestResult.objects.get(release=release, case=case, reported_by=request.user)
            test_result.result = result
        except TestResult.DoesNotExist:
            test_result = TestResult(release=release, case=case, reported_by=request.user, result=result)
        test_result.save()
    return HttpResponseRedirect('/repository/package/%s/%s/' % (packageName, version))


def releases_ack(request):
    releases = Release.objects.filter(resolution='pending')
    releases_acked = []
    for release in releases:
        if release.get_status() == 'passed':
            releases_acked.append(release)

    context = {
        'releases': releases_acked,
    }
    return render_to_response('repository/releases-ack.html', context, context_instance=RequestContext(request))


def releases_nack(request):
    releases = Release.objects.filter(resolution='pending')
    releases_nacked = []
    for release in releases:
        if release.get_status() == 'failed':
            releases_nacked.append(release)

    context = {
        'releases': releases_nacked,
    }
    return render_to_response('repository/releases-nack.html', context, context_instance=RequestContext(request))
"""
