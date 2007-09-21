from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from web.ciftci.models import Repository, Package

# Helper module for repo operations
import operations as op

def list_repository(request, repo_id=2):
    repo = get_object_or_404(Repository, pk=repo_id)

    pisi_list = op.getPisiList(repo.repo_path)
    dep_dict = op.getPisiDict(repo.repo_path)
    for pack in pisi_list:
        if dep_dict[pack["package_name"]]:
            pack["deplist"] = dep_dict[pack["package_name"]]
            #pisi_list[pack].append(dep_dict[pack["package_name"]])

    return render_to_response('ciftci/ciftci_repodetails.html',
                              {'pisi_list' : pisi_list,
                               'dep_dict'  : dep_dict,
                               'repo_name' : repo.repo_name,
                               'repo_path' : repo.repo_path})




