from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson
from django.template import RequestContext
from noan.repository.models import *
from django.contrib.auth import authenticate, login, logout

from  datetime import date
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def page_index(request):
    distributions = Distribution.objects.all()
    if len(distributions) == 1:
        return HttpResponseRedirect(distributions[0].get_url())

    updates= []
    context= {}
    for dist in distributions:
        up = Update.objects.filter(source__distribution__exact=dist.id).order_by("-updated_on")[:9]
        updates.append((dist, up))
    context["updates"] = updates

    context['distributions'] = distributions
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
    return render_to_response('repository/binary.html', context, context_instance=RequestContext(request))


def page_pending_index(request):
    distributions = Distribution.objects.all()
    if len(distributions) == 1:
        dist = '%s-%s' % (distributions[0].name, distributions[0].release)
        return HttpResponseRedirect('/repository/pending/%s/' % dist)

    context = {
        'distributions': distributions,
    }
    return render_to_response('repository/pending-index.html', context, context_instance=RequestContext(request))


def page_pending(request, distName, distRelease):
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
    return render_to_response('repository/pending.html', context, context_instance=RequestContext(request))


def page_users(request):
    users = User.objects.all().order_by('first_name', 'last_name')
    # Pagination
    paginator = Paginator(users, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)

    context = {
        'developers': users,
    }
    return render_to_response('repository/users.html', context, context_instance=RequestContext(request))


def page_user(request, userName):
    developer = User.objects.get(username=userName)
    pending = Binary.objects.filter(resolution='pending', update__updated_by=developer)
    context = {
        'developer': developer,
        'pending': pending,
    }
    return render_to_response('repository/user.html', context, context_instance=RequestContext(request))



def search_form(request):
    context= {}
    distributions = Distribution.objects.all()
    if request.method == 'POST' and request.POST["question"]:
        keyword = request.GET['question']
        search_area = request.GET['search_area']
        distro = request.GET['distro']
        results = []
        if search_area == "package":
            if distro != "null":
                results = Package.objects.filter(source__distribution__id=distro).filter(name__contains=keyword)
            else:
                results = Package.objects.filter(name__contains=keyword)
        elif search_area == "source":
                results = Package.objects.filter(source__name__contains=keyword)
        context['results'] = results

    context['distributions'] = distributions
    return render_to_response('repository/search.html', context, context_instance=RequestContext(request))


@login_required
def AckNackList(request):
    list=[]
    error = ()
    stateBinary = Binary.objects.filter(Q(resolution = 'pending'), Q(package__source__maintained_by = request.user) | Q(update__updated_by = request.user),Q(testresult__isnull=True))
    if request.method == 'POST':
        radio = {}
        comment = {}
        # have two dict for form data in post. formating data to meaningful info for db. (iterater all post data because not sort of key in post method.)
        for list in request.POST.lists():
            try:
                # catch the csrfmiddlewaretoken in post
                if list[0] == "csrfmiddlewaretoken":
                    pass
                else:
                    post_info = list[0].split("-")
                    binary_id = int(post_info[0])
                    if (post_info[1] == "radio"):
                        radio[post_info[0]] = list[1]
                    if (post_info[1] == "comment"):
                        comment[post_info[0]] = list[1]
            except Exception, err:
                print "Error: %s" %(str(err))
                error += err
        # Gettin binary id in radio dict. iteratior radio for add value to StateOfTest db.
        for binary_id in  radio:
            a = binary_id
            if binary_id in comment:
                Add_Comment = TestResult(binary = Binary.objects.get(id=binary_id), created_by = request.user, result = radio[binary_id][0], comment = comment[binary_id][-1])
                Add_Comment.save()
            else:
                Add_Comment = TestResult(binary = Binary.objects.get(id=binary_id), created_by = request.user, result = radio[binary_id][0])
                Add_Comment.save()
    if stateBinary or stateBinaryOfUpdate:
        distributions = Distribution.objects.all()

    else:
        distributions = ""
    paginator = Paginator(stateBinary, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        stateBinary = paginator.page(page)
    except (EmptyPage, InvalidPage):
        stateBinary = paginator.page(paginator.num_pages)
    context = {
            'error' : error,
            'distributions' : distributions,
            'stateBinarys' : stateBinary,
    }
    return render_to_response('repository/ack_nack.html', context, context_instance=RequestContext(request))

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/repository/')

def ListAllAckNack(request):
    AckNackList = TestResult.objects.all()
    distributions = Distribution.objects.all()
    context = {
            'distributions' : distributions,
            'AckNackList' : AckNackList,
    }
    return render_to_response('repository/acks_nacks.html', context, context_instance=RequestContext(request))



