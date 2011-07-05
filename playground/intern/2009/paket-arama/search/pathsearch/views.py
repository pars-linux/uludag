# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from search.pathsearch.models import Repo
from django.db import models
from search.settings import versions, default_version
from django.template import RequestContext
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from search.settings import LIST_SIZE


def pager(request, entry_list, per_page=LIST_SIZE):
    """Paginates the given resultset."""    
    paginator = Paginator(entry_list, per_page)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)
    return entries
    
    
def index(request, version=default_version):
    """ Index page for pathsearch. """
    if version not in versions:
        version = default_version
    if request.POST.get('q') or request.GET.get('q'):
        entry = request.POST.get('q')  or request.GET.get('q')
        # A workaround here: should be improved:
        if ' in:'in entry:
            in_start = entry.find('in:')
            in_end = in_start + 4
            term = entry[:in_start-1]
            pkg = entry[in_end-1:]
	    url = "/search/%s/package/%s/%s" % (version, pkg, term)
	    return HttpResponseRedirect(url)
            #return search_in_package(request, version, pkg, term)
        
        elif entry.strip().startswith('in:'):
            pkg = entry[3:].strip()
	    return HttpResponseRedirect("/search/%s/package/%s" % (version, pkg))
            #return list_package_contents(request, version, pkg)
        
        elif entry.strip().startswith('p:'):
            pkg = entry[2:].strip()
	    return HttpResponseRedirect("/search/%s/packages/%s" % (version, pkg))
            #return search_for_package(request, version, pkg)
            
        # If search form is submitted, redirect...
	group = request.GET.get('group')
	if group:
	    url = "/search/%s/%s?group=yes" % (version, entry)
	else:
	    url = "/search/%s/%s" % (version, entry)
	
	return HttpResponseRedirect(url)
        #return search_in_all_packages(request, version)#,term?
    
    # If no search is done, display main page.
    return render_to_response('index.html', {'current_version':version,
                                             'versions'       :versions})

def list_package_contents(request, version, package_name):
    entry_list = Repo.objects.filter(repo = version.replace("-", "_"), package = package_name)
    query = "in:%s" % package_name
    
    return render_to_response('pathsearch/results.html', {
							  'entries'	    : pager(request, entry_list),
							  'result_count'    : len(entry_list),
                                                          'package_name'    : package_name,
                                                          'current_version' : version,
                                                          'versions'        : versions,
							  'query'	    : query,
                                              })

def search_for_package(request, version, package_name=""):
    """Searches for a package related to given name"""
    if not package_name.strip():
        package_list = Repo.objects.values_list('package').order_by('package').distinct().filter(repo = version.replace("-","_"))

    else:
        package_list = Repo.objects.values_list('package').order_by('package').distinct().filter(repo = version.replace("-","_"), package__contains=package_name)
    
    #package_list = [p.package for p in package_list]
    package_list = [p[0] for p in package_list]
    query = "p:%s" % package_name

    # We have a sorting problem here!
    # package_list is the related package names.
    
    return render_to_response('pathsearch/packages.html',
                              { 'entries'		: pager(request, package_list),
				'result_count'	   	: len(package_list),
                                'package_name'          : package_name,
                                'current_version'       : version,
                                'versions'              : versions,
                                'query'                 : query,
                               },
                               context_instance = RequestContext(request)
                              )
def search_in_package(request, version, package_name, term):
    """Searches for term in the given package."""
    entry_list = Repo.objects.filter(repo = version.replace("-","_"), package = package_name, path__contains=term)
    query = "%s in:%s" % (term, package_name)
    
    return render_to_response('pathsearch/results.html', {
							  'entries'	    : pager(request, entry_list),
							  'result_count'    : len(entry_list),
                                                          'package_name'    : package_name,
                                                          'term'            : term,
                                                          'current_version' : version,
                                                          'versions'        : versions,
							  'query'	    : query,
                                              })
    
def search_in_all_packages(request, version, term = ""):
    """Searches for term in all packages' file paths.
    We have some problems here. If grouping is desired, that can't be combined with pagination.
    So we have to send entry_list instead of entries.    
    """
    
    #TODO: Delete the line below.
    term = term or request.GET('q','')    # If no URL term specified, get the GET data.
    group = request.GET.get('group')   # Is grouping enabled?

    query = term
    
    too_short = group and (len(term) < 3)
    if too_short:
	entry_list = []
    else:
	entry_list = Repo.objects.filter(repo = version.replace("-","_"), path__contains=term)
    
    if group:
	entries = entry_list
    else:
	entries = pager(request, entry_list)
    
    return render_to_response('pathsearch/results.html', {
							  'entries'	    : entries,  
							  'result_count'    : len(entry_list),
                                                          'term'            : term,
                                                          'group'           : group,
                                                          'current_version' : version,
                                                          'versions'        : versions,
							  'too_short'	    : too_short,
							  'query'	    : query,
                                                          
                                              })