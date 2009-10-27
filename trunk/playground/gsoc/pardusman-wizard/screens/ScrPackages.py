#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtWebKit,  QtGui, QtCore, uic
from repo_utils import RepoUtils

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        uic.loadUi("screens/screenPackages.ui", self)
    
        self.checkedPackages = {}
        self.checkedComponents = []
        self.dependencies = []

        self.connect(self.treeComponents, QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'), self.checkComponent)
        self.connect(self.webView, QtCore.SIGNAL('titleChanged(const QString&)'), self.checkPackage)

        self.desc = "Add user"
    
    def getDepends(self,  package):
        deps = []
        
        depList = self.repo.pdb.get_package(package).packageDependencies
        
        for dep in depList:
            deps.append(dep.package)
        
        return deps
    
    def calculateDeps(self):
        self.dependencies = []
        
        for package in self.checkedPackages.iterkeys():
            for dep in self.checkedPackages[package]:
                if not dep in self.checkedPackages.keys() and not dep in self.dependencies:
                    self.dependencies.append(dep)
    
    def calculateSize(self):
        total = 0
        calculatedPackages = self.checkedPackages.keys()
        calculatedDeps = self.dependencies
        levels = {}

        if self.checkedComponents.__len__() > 0:
            for component in self.checkedComponents:
                for package in self.repo.cdb.get_packages(component):
                    if not package in calculatedPackages:
                        calculatedPackages.append(package)
            
#            for package in packages:
#                if self.systemType == "install":
#                    total += self.repo.pdb.get_package(package).packageSize
#                elif self.systemType == "live":
#                    total += self.repo.pdb.get_package(package).installedSize
#                if package in calculatedPackages:
#                    calculatedPackages.remove(package)
        
        if calculatedPackages.__len__() > 0:
            for package in calculatedPackages:
                    if self.systemType == "install":
                        total += self.repo.pdb.get_package(package).packageSize
                        if package in calculatedDeps:
                            calculatedPackages.remove(package)
                    elif self.systemType == "live":
                        total += self.repo.pdb.get_package(package).installedSize
                        if package in calculatedDeps:
                            calculatedPackages.remove(package)
        
        if calculatedDeps.__len__() > 0:
            for package in calculatedDeps:
                if self.systemType == "install":
                    total += self.repo.pdb.get_package(package).packageSize
                elif self.systemType == "live":
                    total += self.repo.pdb.get_package(package).installedSize

        if self.systemType == "install":
            sizeType = "package"
        elif self.systemType == "live":
            sizeType = "installed"
            
        size,  unit = self.humanReadableSize(total)
        
        self.label.setText("There is %s component, %s selected package and %s dependencies. Total %s size is %.2f %s" %
                            (self.checkedComponents.__len__(), 
                             self.checkedPackages.keys().__len__(),
                             self.dependencies.__len__(),
                             sizeType, 
                             size,
                             unit))
    
    def humanReadableSize(self,  size):
        symbols, depth = [' B', 'KB', 'MB', 'GB'], 0
    
        while size > 1000 and depth < 3:
            size = float(size / 1024)
            depth += 1

        return size, symbols[depth]
    
    def checkPackage(self,  package):
        package = str(package).replace("#", "")
        
        if not package == "":
            if package in self.checkedPackages.keys():
                self.checkedPackages.__delitem__(str(package))
            else:
                self.checkedPackages[str(package)] = []

                for dep in self.getDepends(package):
                    self.checkedPackages[str(package)].append(dep)
        
        self.calculateDeps()
        self.calculateSize()

    def checkComponent(self,  item,  column):
        if item.checkState(column) == 2 and not item.text(column) in self.checkedComponents:
            self.checkedComponents.append(str(item.text(column)))
            self.calculateSize()
        elif item.checkState(column) == 0 and item.text(column) in self.checkedComponents:
            self.checkedComponents.remove(str(item.text(column)))
            self.calculateSize()
        self.fillPackages(str(item.text(column)))

    def takeList(self):
        self.repo = RepoUtils("/tmp/pw_tmp",  self.repo_uri)
        self.mainList = self.repo.getPackageList() # list = {"component":[pack1, pack2,...,packn]}
    
    def fillPackages(self,  component):
        packages = []
        
        for componentName in self.mainList.keys():
            if componentName.__contains__(component):
                packages.extend(self.mainList[componentName])

        self.webView.setHtml(QtCore.QString("""
        <html>
        <head>
        <link href="layout.css" rel="stylesheet" type="text/css" />
        <script type="text/javascript">
        function changeTitle (msg) {
            if (document.title == msg) {
                document.title = "#" + msg;
            } else {
                document.title = msg;
            }
        }
        </script>
        <body>
        %s
        </body>
        </html>
        """ % self.packageDivs(packages)))

    def packageDivs(self,  packages):
        index = 0
        titleStyle = ""
        style = ""
        
        packageDivs = []
        
        template = """
        <!-- package start -->
        <div>
        <!-- checkbox --> %s <!-- checkbox -->
        <div class="package_title" style="%s" id="package_t%d" onclick="showHideContent(this)">
        <b>%s</b><br><span style="color:#303030">%s</span><br>
        </div>
        </div><br />
        <!-- package end -->
        """
        
        for package in packages:
            app = self.repo.pdb.get_package(package)
            
            if index % 2 == 0:
                style = "background-color:#FFA50C;"
            else:
                style = "background-color:#FEE0A5"
            titleStyle = style

            if app.name in self.checkedPackages.keys():
                checkState = "checked"
            else:
                checkState = ""

            curindex = index + 1

            checkbox = """<div class="checkboks" style="float: left; %s" id="checkboks_t%d"><input type="checkbox" %s onclick=" changeTitle('%s')" name="%s" id="checkboks%d"></div>""" % (titleStyle,curindex,checkState,app.name,app.name,curindex)

            packageDivs.append(template % (checkbox, titleStyle, curindex, app.name, app.summary))
            index += 1
        
        return "\n".join(packageDivs)
    
    def fillComponents(self):
        items = []
        topItems = {0:self.treeComponents}
        
        cList = self.mainList.keys()
        clist = cList.sort()
        
        level = 0
        
        # there is no component.xml in desktop component. so add it hardcoded.
        desktop = QtGui.QTreeWidgetItem(self.treeComponents,  ["desktop"])
        
        for component in cList:
            level = component.count(".")

            if component.startswith("desktop"):
                item = QtGui.QTreeWidgetItem(desktop,  [component])
                item.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
                item.setCheckState(0,  QtCore.Qt.Unchecked)
                topItems[level + 1] = item
            else:
                item = QtGui.QTreeWidgetItem(topItems[level],  [component])
                if not level == 0:
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
                    item.setCheckState(0,  QtCore.Qt.Unchecked)
                topItems[level + 1] = item
