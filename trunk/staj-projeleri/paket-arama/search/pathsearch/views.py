from django.shortcuts import render_to_response
from search.pathsearch.models import Entry2007, Entry2008
from django.db import models
from search.settings import versions
from django.template import RequestContext
from django.http import Http404


def index(request, version='2008'):
    """ Index page for pathsearch. """
    if version not in versions:
        version = 2008
    if request.POST.get('q') or request.GET.get('q'):
        entry = request.POST.get('q')  or request.GET.get('q')
        # A workaround here: should be improved:
        if ' in:'in entry:
            in_start = entry.find('in:')
            in_end = in_start + 4
            term = entry[:in_start-1]
            pkg = entry[in_end-1:]
            return search_in_package(request, version, pkg, term)
        
        elif entry.strip().startswith('in:'):
            pkg = entry[3:].strip()
            return list_package_contents(request, version, pkg)
        
        elif entry.strip().startswith('p:'):
            pkg = entry[2:].strip()
            return search_for_package(request, version, pkg)
            
        # If search form is submitted, redirect...
        return search_in_all_packages(request, version)
    
    # If no search is done, display main page.
    return render_to_response('index.html', {'current_version':version,
                                             'versions'       :versions})

def ENTRY(version):
    match = {
             '2007' : Entry2007,
             '2008' : Entry2008,
             }
    try:
        return match[version]
    except:
        raise Http404

def list_package_contents(request, version, package_name):
    entry_list = ENTRY(version).objects.filter(package = package_name)
    
    return render_to_response('pathsearch/results.html', {
                                                          'entry_list'      :   entry_list,
                                                          'package_name'    :   package_name,
                                                          'current_version'         : version,
                                                          'versions'       :versions,
                                              })

def search_for_package(request, version, package_name):
    """Searches for a package related to given name in the URL."""
    if not package_name.strip():
        package_list = ENTRY(version).objects.values_list('package').order_by('package').distinct()

    else:
        package_list = ENTRY(version).objects.values_list('package').order_by('package').distinct().filter(package__contains=package_name)
    
    #package_list = [p.package for p in package_list]
    package_list = [p[0] for p in package_list]

    # We have a sorting problem here!
    # package_list is the related package names.
    
    return render_to_response('pathsearch/packages.html',
                              { 'package_list'         : package_list,
                                'package_name'         : package_name,
                                'current_version'      : version,
                                'versions'              :versions,
                                'q'                     : request.GET.get('q'),
                               },
                               context_instance = RequestContext(request)
                              )
def search_in_package(request, version, package_name, term):
    """Searches for term in the given package."""
    entry_list = ENTRY(version).objects.filter(package = package_name, path__contains=term)
    return render_to_response('pathsearch/results.html', {
                                                          'entry_list'      :   entry_list,
                                                          'package_name'    :   package_name,
                                                          'term'            :   term,
                                                          'current_version' : version,
                                                          'versions'       :versions,
                                              })
    
def search_in_all_packages(request, version, term = None):
    """Searches for term in all packages' file paths."""
    term = term or request.POST['q']    # If no URL term specified, get the POST data.
    group = request.POST.get('group')   # Is grouping enabled?

    entry_list = ENTRY(version).objects.filter(path__contains=term)
    
    return render_to_response('pathsearch/results.html', {
                                                          'entry_list'      :   entry_list,
                                                          'term'            :   term,
                                                          'group'           :   group,
                                                          'current_version' : version,
                                                          'versions'        :  versions,
                                                          
                                              })

