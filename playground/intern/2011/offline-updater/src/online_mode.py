#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as tree
import urllib2
import lzma
import cPickle


def downloadRepoXML(repo):
    file_name = repo.split('/')
    file_name = file_name[4]+"_"+file_name[5]+"_"+file_name[6]+".xz"
    
    download(file_name, repo)
    
    xml_object = open(file_name, 'rb').read()
    a = lzma.LZMADecompressor()
    str_object2 = a.decompress(xml_object)
    f = open(file_name+".xml", 'wb')
    f.write(str_object2)
    f.close()
    return file_name+".xml"

def getRepos():
    
    return cPickle.load(open("repoList.ofu"))

def findDependency(i):
    dep_list = []
    dep_handler = i.find("RuntimeDependencies")
    if dep_handler:
        deps = dep_handler.findall("Dependency")
        for dep in deps:
            dep_list.append(dep.text)
            
    #print dep_list
    return dep_list

def findReplaces(i):
    rep_list = [] #MAYBE: replace packages can be more than one
    rep_handler = i.find("Replaces")
    if rep_handler:
        reps = rep_handler.findall("Package")
        for rep in reps:
            rep_list.append(rep.text)
    #print rep_list
    return rep_list


def parsePisiXML(dependency = None):
    repo_packages = {}
    repos = getRepos()
    
    for repo in repos:
        packages = {}
        obselete_list = []
        
        pisi_xml = downloadRepoXML(repos[repo]) #XML dosyalarını indir
        pisi_data = open(pisi_xml) #Aç
        package_tree = tree.fromstring(pisi_data.read()) #XML dosyasını tree değişkenine aç
        packages_tree = package_tree.findall("Package") #tree içerisinden tüm Package taglerini çek
        obseletes = package_tree.find("Distribution").find("Obsoletes").findall("Package")

        for obsolete in obseletes:
            obselete_list.append(obsolete.text)
            
        for i in packages_tree:
            dep_list = []
            history_handler = i.find("History") 
            name = i.find("Name").text
            release = history_handler.find("Update").get("release")
            version = history_handler.find("Update").find("Version").text
            #url
            url = repos[repo].strip("pisi-index.xml.xz") + i.find("PackageURI").text
            #/url
            #Replaces
            rep_list = findReplaces(i)
            #/Replaces
            #Dependencies
            dep_list = findDependency(i)
            #/Dependencies
            packages[name] = (release, repo, dep_list, version, rep_list, url)
        print "\n"    
        repo_packages[repo] = (packages, obselete_list) #FIXED
        #print repo_packages[repo][0]["texlive-lang-spanish"][4]
    return repo_packages


def getInstalledPackages():
    return cPickle.load(open("packageList.ofu"))


def getUpdatedPackages(): #CODE: güncel paket listesi ile elimizdeki paket listesi karşılaştırılacak.
    
    
    installed_packages = getInstalledPackages()
    repo_packages = parsePisiXML()

    
    deplist = {}
    package_list = {}
    download_list = []
    print "\n"
    for ins_package in installed_packages:
        for repo in repo_packages:
            for package in repo_packages[repo][0]:
                if ins_package == package and repo_packages[repo][0][package][1] == installed_packages[ins_package][1]:
                    if int(repo_packages[repo][0][package][0]) > int(installed_packages[ins_package][0] or 
                         repo_packages[repo][0][package][3] > installed_packages[ins_package][3]):
                        if checkObsoletes(repo_packages[repo][1], package): 
                            isReplace = checkReplaces(repo_packages[repo][0][package][4], package, package_list)
                            if isReplace ==  None:
                                #print "%d.Paket adi:%s\t repo:%s\t guncelV:%s\t simdikiV:%s"%(cnt, package, repo, repo_packages[repo][0][package][0],installed_packages[ins_package][0])
                                download_list.append(repo_packages[repo][0][package][5])
                                for dep in repo_packages[repo][0][package][2]:
                                    deplist[dep] = repo_packages[repo][0][package][1]
                            else:
                                download_list.append(repo_packages[repo][0][isReplace][5])
        package_list[ins_package] = installed_packages[ins_package][1]
    deplist = checkDependencyUpdate(package_list, deplist, repo_packages)
    for dep in deplist:
        download_list.append(repo_packages[deplist[dep]][0][dep][5])
    
    print "%s packages and %s dependencies ready for download" %(int(len(download_list)-len(deplist)), len(deplist))
    #for a in download_list:
    #    print a

def checkDependencyUpdate(package_list, deplist, repo_packages):
    
    for i in package_list.keys():
        for j in deplist.keys():
            if i==j:
                deplist.pop(i)
    
    
    new_deplist = checkRecursiveDeps(deplist, repo_packages)
    
    for i in package_list.keys():
        for j in new_deplist.keys():
            if i==j:
                new_deplist.pop(i)
    
    #print deplist
    
    deplist.update(new_deplist)
    
    #print deplist
    return deplist
    

def checkRecursiveDeps(deplist, repo_packages):
    
    #print "Recursive Dep check"
    
    deps = {}
    for dep in deplist:
        for repo in repo_packages:
            for package in repo_packages[repo][0]:
                if deplist[dep] == repo_packages[repo][0][package][1] and dep == package:
                    for new_dep in repo_packages[repo][0][package][2]:
                        deps[new_dep] = deplist[dep]
                    
    #print deps
    if not len(deps) == 0:
        deps.update(checkRecursiveDeps(deps, repo_packages))
    return deps
        
def checkObsoletes(obselete_list, package):
    for obselete in obselete_list:
        if package == obselete:
            return False
        else:
            return True
    
def checkReplaces(rep_list, package, package_list):
    #print package_list
    #print "\n"
    for ins_package in package_list:
        for rep in rep_list:
            #print ins_package
            if ins_package == rep:
                return package
            else:
                return None

    #return True

def download(file_name, url):
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
    
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()
    



def start():
    print "-------------------------Lets we start-----------------------------"
    getUpdatedPackages()
    #print getInstalledPackages()
start()
