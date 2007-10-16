from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from web.ciftci.models import Repository, Package

# Helper module for repo operations
import operations as op

def sync_repositories(request):
    # First we must get the POST data
    try:
        selectRepoSource = request.POST['selectRepoSource']
        selectDestSource = request.POST['selectDestSource']

    except KeyError:
        # Can be caught if the from is modified before submitting..
        pass
    else:
        source_repo = get_object_or_404(Repository, repo_name=selectRepoSource)
        dest_repo = get_object_or_404(Repository, repo_name=selectDestSource)

        # Returns a list of packages(with deps) which are in source_path but not in dest_path
        pisi_list = op.getDifferences(source_repo.repo_path, dest_repo.repo_path)

        return render_to_response('ciftci/ciftci_repodifferences.html',
                                  {'pisi_list' : pisi_list,
                                   'source_repo' : source_repo,
                                   'dest_repo' : dest_repo})

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

def transfer_packages(request):
    # Get hidden values which contains the source and dest repo's
    source_repo = request.POST['source_repo']
    dest_repo = request.POST['dest_repo']

    # Get checked items list
    checked_items = [p.split("_")[0] for p in request.POST.keys() if p.endswith("_checkbox")]
    print checked_items

def choose_repository(request):

    return render_to_response('ciftci/ciftci_chooserepo.html',
                              {'repo_list' : [p.repo_name for p in get_list_or_404(Repository)]})


