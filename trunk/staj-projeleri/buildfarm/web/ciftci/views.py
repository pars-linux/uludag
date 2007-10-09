from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from web.ciftci.models import Repository, Package

# Helper module for repo operations
import operations as op

def list_repository(request, repo_name):

    # Gets the selected Repository instance
    repo = get_object_or_404(Repository, repo_name=repo_name)

    # Gets the pisi packages dictionary
    pisi_list = op.getPisiPackages(repo.repo_path)

    # Returns a rendered HTTP Response of the dictionary
    return render_to_response('ciftci/ciftci_repo.html',
                              {'pisi_list' : pisi_list,
                               'repo_name' : repo.repo_name,
                               'repo_path' : repo.repo_path})




