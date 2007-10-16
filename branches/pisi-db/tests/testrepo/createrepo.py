import os
import time

pspecTemplate = """<?xml version="1.0" ?>
<!DOCTYPE PISI SYSTEM "http://www.pardus.org.tr/projeler/pisi/pisi-spec.dtd">
<PISI>
    <Source>
        <Name>%(package)s</Name>
        <Homepage>%(homepage)s</Homepage>
        <Packager>
            <Name>%(packager_name)s</Name>
            <Email>%(packager_email)s</Email>
        </Packager>
        <License>GPL-2</License>
        <IsA>app:gui</IsA>
        <Summary>%(summary)s</Summary>
        <Description>%(description)s</Description>
        <Archive sha1sum="%(sha1sum)s" type="targz">%(archive)s</Archive>
    </Source>

    <Package>
        <Name>%(package)s</Name>
        <RuntimeDependencies>
            %(runtimedeps)s
        </RuntimeDependencies>
        <Files>
            <Path fileType="data">/usr/bin</Path>
        </Files>
    </Package>

    <History>
        <Update release="1">
            <Date>%(date)s</Date>
            <Version>0.3</Version>
            <Comment>First release</Comment>
            <Name>%(packager_name)s</Name>
            <Email>%(packager_email)s</Email>
        </Update>
    </History>
</PISI>
"""

componentTemplate = """
<PISI>
    <Name>%(name)s</Name>
    <LocalName xml:lang="tr">%(local_name)s</LocalName>
    <Summary xml:lang="tr">%(summary)s</Summary>
    <Description xml:lang="tr">%(description)s</Description>
    <Packager>
        <Name>Joe Packager</Name>
        <Email>joe@pardus.org.tr</Email>
    </Packager>
</PISI>
"""

actionsTemplate = """
from pisi.actionsapi import pisitools

WorkDir = "skeleton"

def install():
    pisitools.dobin("skeleton.py")
    pisitools.rename("/usr/bin/skeleton.py", "%s")
"""

class Component:
    def __init__(self, name):
        self.name = name

    def get_comp_template(self, subcomp):
        return componentTemplate % {"name":subcomp,
                                    "local_name":subcomp,
                                    "summary":subcomp,
                                    "description":subcomp}

    def get_comp_path(self):
        return "/".join(self.name.split("."))

    def create(self):
        component_path = self.get_comp_path()
        if not os.path.exists(component_path):
            os.makedirs(component_path)
            cur_dir = os.getcwd()
            for subcomp in self.name.split("."):
                os.chdir(subcomp)
                open("component.xml", "w").write(self.get_comp_template(subcomp))
            os.chdir(cur_dir)

class Package:

    def __init__(self, name, partof, deps):
        self.name = name
        self.partof = partof
        self.deps = deps
        self.component = Component(self.partof)

    def get_spec_template(self):
        package =  self.name
        homepage = "www.pardus.org.tr"
        packager_name = "Joe Packager"
        packager_email = "joe@pardus.org.tr"
        summary = "%s is a very useful package" % self.name
        description = "%s is a very useful package that is known for its usefulness." % self.name
        sha1sum = "cc64dfa6e068fe1f6fb68a635878b1ea21acfac7"
        archive = "http://cekirdek.uludag.org.tr/~faik/pisi/skeleton.tar.gz"
        date = time.strftime("%Y-%m-%d")
        partof = self.partof

        runtimedeps = ""
        for dep in self.deps:
            runtimedeps += "        <Dependency>%s</Dependency>\n" % dep

        return pspecTemplate % locals()

    def create(self):
        self.component.create()
        cur_dir = os.getcwd()
        os.chdir(self.component.get_comp_path())
        os.makedirs(self.name)
        os.chdir(self.name)
        open("pspec.xml", "w").write(self.get_spec_template())
        open("actions.py", "w").write(actionsTemplate % self.name)
        os.chdir(cur_dir)

class PackageFactory:
    def getPackage(self, name, runtimeDeps = [], component = "system.base"):
        return Package(name, component, runtimeDeps)

    def getPackageBundle(self, component, *packages):
        pkgs = []
        for pkg in packages:
            pkgs.append(Package(pkg, component, []))
        return pkgs

if __name__ == "__main__":

    pf = PackageFactory()
    
    packages = [
                # system.base
                pf.getPackage("bash"),
                pf.getPackage("curl", ["libidn", "zlib", "openssl"]),
                pf.getPackage("shadow", ["db4","pam", "cracklib"]),
                pf.getPackage("jpeg"),

                # applications.network
                pf.getPackage("ncftp", [], "applications.network"),
                pf.getPackage("bogofilter", ["gsl"], "applications.network"),
                pf.getPackage("gsl", [], "applications.network"),
                ]

    # system.base
    packages.extend(pf.getPackageBundle("system.base", "libidn", "zlib", "openssl", "db", "pam", "cracklib"))

    # applications.network
    packages.extend(pf.getPackageBundle("applications.network", "ethtool", "nfdump"))

    for pkg in packages:
        pkg.create()
