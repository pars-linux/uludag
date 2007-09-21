from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from web.ciftci.models import Repository, Package

# Helper module for repo operations
import operations as op

def list_repository(request, repo_id=1):
    repo = get_object_or_404(Repository, pk=repo_id)

    pisi_list = op.getPisiList(repo.repo_path)
    return render_to_response('ciftci/ciftci_repodetails.html',
                              {'pisi_list' : pisi_list,
                               'repo_name' : repo.repo_name,
                               'repo_path' : repo.repo_path})




