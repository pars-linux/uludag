from django.shortcuts import render_to_response
from pakettif.pathsearch.models import Entry
from django.db import models

def index(request):
    """ Index page for pathsearch. """
    if request.POST.get('q'):
        # If search form is submitted, redirect...
        return search_in_all_packages(request)
    
    # If no search is done, display main page.
    return render_to_response('index.html', {})

    
def search_for_package(request, package_name):
    """Searches for a package related to given name in the URL."""
    package_list = Entry.objects.filter(package__contains=package_name).order_by('package')
    package_list = [p.package for p in package_list]
    package_list = list(set(package_list))
    package_list.sort()
    # We have a sorting problem here!
    # package_list is the related package names.
    
    return render_to_response('pathsearch/packages.html',
                              { 'package_list'         : set(package_list),
                                'package_name'         : package_name,
                               }
                              )
def search_in_package(request, package_name, term):
    """Searches for term in the given package."""
    entry_list = Entry.objects.filter(package = package_name, path__contains=term).order_by('package')
    return render_to_response('pathsearch/results.html', {
                                                          'entry_list'      :   entry_list,
                                                          'package_name'    :   package_name,
                                                          'term'            :   term,
                                              })
    
def search_in_all_packages(request, term = None):
    """Searches for term in all packages' file paths."""
    term = term or request.POST['q']    # If no URL term specified, get the POST data.
    group = request.POST.get('group')   # Is grouping enabled?

    entry_list = Entry.objects.filter(path__contains=term).order_by('package')
    
    return render_to_response('pathsearch/results.html', {
                                                          'entry_list'      :   entry_list,
                                                          'term'            :   term,
                                                          'group'           :   group,
                                                          
                                              })

