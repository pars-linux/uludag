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
            release_handler = i.find("History") 
            name = i.find("Name").text
            release = release_handler.find("Update").get("release")
            #Dependencies
            dep_list = findDependency(i)
            #obsolete_list = findObsoletes(i)
            #/Dependencies
            packages[name] = (release, repo, dep_list)
        print "\n"    
        #print len(dep_list)
        repo_packages[repo] = (packages, obselete_list) #FIXED
    #print repo_packages["pardus"][0]["firefox"]
    return repo_packages


def getInstalledPackages():
    return cPickle.load(open("packageList.ofu"))


def getUpdatedPackages(): #CODE: güncel paket listesi ile elimizdeki paket listesi karşılaştırılacak.
    
    
    installed_packages = getInstalledPackages()
    repo_packages = parsePisiXML()

    
    cnt = 1
    deplist = {}
    package_list = {}
    print "\n"
    for ins_package in installed_packages:
        for repo in repo_packages:
            for package in repo_packages[repo][0]:
                if ins_package == package and repo_packages[repo][0][package][1] == installed_packages[ins_package][1]:
                    if int(repo_packages[repo][0][package][0]) > int(installed_packages[ins_package][0]):
                        if checkObsoletes(repo_packages[repo][1], package):
                            print "%d.Paket adi:%s\t repo:%s\t guncelV:%s\t simdikiV:%s"%(cnt, package, repo, repo_packages[repo][0][package][0],installed_packages[ins_package][0])
                            cnt += 1
                            for dep in repo_packages[repo][0][package][2]:
                                deplist[dep] = repo_packages[repo][0][package][1]
        package_list[ins_package] = installed_packages[ins_package][1]
    checkDependencyUpdate(package_list, deplist, repo_packages)

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
    
    print deplist
    

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

