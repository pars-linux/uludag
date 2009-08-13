from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson
from django.template import RequestContext
from noan.repository.models import *
from django.contrib.auth import authenticate, login, logout
from django.forms.formsets import formset_factory
from django import forms
from noan.forms import *

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
    if 'statu' in request.POST:
        if request.POST['statu'] == "nack":
            State = "nack"
        else:
            State = "ack"
        state = StateOfTest.objects.get(binary = binary)
        print state.state
        state.state = State
        state.save()
        print state.state
    context = {
        'binary': binary,
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
    if 'question' in request.GET and request.GET['question'] != "":
        keyword = request.GET['question']
        search_area = request.GET['search_area']
        distro = request.GET['distro']
        results = []
        if search_area == "package":
            if distro != "null":
                results = Package.objects.filter(source__distribution__id=distro).filter(name__contains=keyword)
            else:
                results = Package.objects.filter(name__contains=keyword)
        elif search_area == "descript":
            result = Package.objects.filter(source__distribution__id=distro).filter(source__name__contains=keyword)
        else :
            result = results = Package.objects.filter(source__name__contains=keyword)
        context['results'] = results

    context['distributions'] = distributions
    return render_to_response('repository/search.html', context, context_instance=RequestContext(request))

@login_required
def AckNackList(request):
    list=[]
    stateBinary = Binary.objects.filter(resolution='pending').filter(package__source__maintained_by= request.user)
    stateBinaryOfUpdate = Binary.objects.filter(resolution='pending').filter(update__updated_by = request.user).order_by('package__name')
    for binary in stateBinary:
            list.append({'binary': binary.get_filename(),
                    'distro' : binary.package.source.distribution
                })
    ArticleFormSet = formset_factory(AckNackForm, extra=0)
  #  if request.method == 'POST':

  #      for list in request.POST.lists()
  #          try:
  #              post_info = list[0].split("-")
  #              binary_id = int(post_info[0])
  #              if (post_info[1] == "radio"):
  #                  pass
  #              print post_info,list[1]
  #
  #          except:
  #              print "middleware"""
    if request.method == 'POST':
        formset = ArticleFormSet(request.POST)
        if formset.is_valid():
            for form in formset.cleaned_data:
                print form
    formset = ArticleFormSet(initial = list)
    if stateBinary or stateBinaryOfUpdate:
        distributions = Distribution.objects.all()
    else:
        distributions = ""
    context = {
            'formset' : formset,
            'distributions' : distributions,
            'stateBinarys' : stateBinary,
            'stateBinarysOfUpdate' : stateBinaryOfUpdate,
    }
    return render_to_response('repository/ack_nack.html', context, context_instance=RequestContext(request))

@login_required
def log_out(request):
    logout(request)
    context = {}
    return HttpResponseRedirect('/')

#################################################################################
#   testing form model 


def acknack(request):
    ArticleFormSet = formset_factory(AckNackForm, extra=2)
    if request.method == 'POST':
        formset = ArticleFormSet(request.POST)
        if formset.is_valid():
            for form in formset.cleaned_data:
                print form['binary']
            # do something with the formset.cleaned_data
    else:
        formset = ArticleFormSet()
    return render_to_response('repository/acknack.html', {'formset': formset})

##################################################################################3
