# -*- coding: utf-8 -*-
import unittest
import pisi
import pisi.context as ctx
import pisi.relation
import pisi.conflict

class ConflictTestCase(unittest.TestCase):

    def testInstalledPackageConflicts(self):
        pisi.api.install(["ethtool"])
        relation = pisi.relation.Relation()
        confinfo = pisi.conflict.Conflict(relation)
        confinfo.package = "ethtool"
        confinfo.version = "6"
        confinfo.release = "1"
        flag = pisi.conflict.installed_package_conflicts(confinfo)
        if flag:
            pisi.api.remove(["ethtool"])
            pass
        assert not flag
        pisi.api.remove(["ethtool"])

    def testCalculateConflicts(self):
        packagedb = pisi.db.packagedb.PackageDB()
        packages = ["ethtool", "zlib", "ctorrent"]
        assert pisi.conflict.calculate_conflicts(packages, packagedb)

    def testConflictCheck(self):
        #In our imaginary repo1, bash conflicts with openssl
        #If this fails, it may affect database test case results
        pisi.api.add_repo("repo1", "repos/repo1-bin/pisi-index.xml.bz2")
        pisi.api.update_repo("repo1")

        pisi.api.install(["osman"])
        relation = pisi.relation.Relation()
        myconflict = pisi.conflict.Conflict(relation)
        myconflict.package = "kolpapaket"
        myconflict.version = "0.3"
        myconflict.release = "1"
        flag = "osman" in pisi.api.list_installed()
        if not flag:
            pisi.api.remove(["osman"])
            pisi.api.remove_repo("repo1")
        assert flag

        pisi.api.install(["kolpapaket"])

        flag = "osman" not in pisi.api.list_installed()
        # clean up
        if not flag:
            pisi.api.remove(["kolpapaket"])
            pisi.api.remove(["osman"])
            pisi.api.remove_repo("repo1")

        assert flag
        pisi.api.remove(["kolpapaket"])
        pisi.api.remove(["osman"])
        pisi.api.remove_repo("repo1")

    def testInterRepoCrossConflicts(self):
        #If this fails, it may affect database test case results
        pisi.api.add_repo("repo1", "repos/repo1-bin/pisi-index.xml.bz2")
        pisi.api.update_repo("repo1")

        pisi.api.install(["osman"])
        pisi.api.install(["annebenpaketoldum"])
        before =  pisi.api.list_installed()
        pisi.api.remove_repo("repo1")

        pisi.api.add_repo("repo2", "repos/repo2-bin/pisi-index.xml.bz2")
        pisi.api.update_repo("repo2")
        pisi.api.upgrade()
        after= pisi.api.list_installed()
        flag = set(before) == set(after)
        if not flag:
            pisi.api.remove(["annebenpaketoldum"])
            pisi.api.remove(["osman"])
            pisi.api.remove_repo("repo2")
            assert flag
        flag = (3 == int( pisi.db.installdb.InstallDB().get_package("annebenpaketoldum").release))
        if not flag:
            pisi.api.remove(["annebenpaketoldum"])
            pisi.api.remove(["osman"])
            pisi.api.remove_repo("repo2")
            assert flag
        pisi.api.remove(["annebenpaketoldum"])
        pisi.api.remove(["osman"])
        pisi.api.remove_repo("repo2")
