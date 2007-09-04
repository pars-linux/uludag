# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../../uis/pspecWidget/sourceWidgetUI.ui'
#
# Created: Pzt Eyl 3 17:41:34 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdeui import *



class SourceWidgetUI(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("SourceWidgetUI")


        SourceWidgetUILayout = QGridLayout(self,1,1,11,6,"SourceWidgetUILayout")

        self.gbGeneral = QGroupBox(self,"gbGeneral")
        self.gbGeneral.setFrameShape(QGroupBox.GroupBoxPanel)
        self.gbGeneral.setFrameShadow(QGroupBox.Sunken)
        self.gbGeneral.setAlignment(QGroupBox.WordBreak | QGroupBox.AlignCenter | QGroupBox.AlignBottom | QGroupBox.AlignTop)
        self.gbGeneral.setFlat(1)
        self.gbGeneral.setColumnLayout(0,Qt.Vertical)
        self.gbGeneral.layout().setSpacing(6)
        self.gbGeneral.layout().setMargin(11)
        gbGeneralLayout = QVBoxLayout(self.gbGeneral.layout())
        gbGeneralLayout.setAlignment(Qt.AlignTop)

        layout11 = QGridLayout(None,1,1,0,6,"layout11")

        self.lblName = QLabel(self.gbGeneral,"lblName")

        layout11.addWidget(self.lblName,0,0)
        spacer1 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout11.addItem(spacer1,0,2)

        layout12 = QHBoxLayout(None,0,6,"layout12")

        self.leLicense = KLineEdit(self.gbGeneral,"leLicense")
        layout12.addWidget(self.leLicense)

        self.pbLicense = KPushButton(self.gbGeneral,"pbLicense")
        layout12.addWidget(self.pbLicense)

        layout11.addLayout(layout12,2,1)

        self.lblLicense = QLabel(self.gbGeneral,"lblLicense")

        layout11.addWidget(self.lblLicense,2,0)

        layout11_2 = QHBoxLayout(None,0,6,"layout11_2")

        self.leIsA = KLineEdit(self.gbGeneral,"leIsA")
        layout11_2.addWidget(self.leIsA)

        self.pbIsA = KPushButton(self.gbGeneral,"pbIsA")
        self.pbIsA.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.pbIsA.sizePolicy().hasHeightForWidth()))
        layout11_2.addWidget(self.pbIsA)

        layout11.addLayout(layout11_2,0,4)

        self.leName = KLineEdit(self.gbGeneral,"leName")

        layout11.addWidget(self.leName,0,1)

        self.lblPackager = QLabel(self.gbGeneral,"lblPackager")
        self.lblPackager.setFrameShape(QLabel.NoFrame)
        self.lblPackager.setFrameShadow(QLabel.Plain)

        layout11.addWidget(self.lblPackager,2,3)
        spacer1_2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout11.addItem(spacer1_2,1,2)

        self.leHomepage = KLineEdit(self.gbGeneral,"leHomepage")

        layout11.addWidget(self.leHomepage,1,1)

        self.lePartOf = KLineEdit(self.gbGeneral,"lePartOf")

        layout11.addWidget(self.lePartOf,1,4)
        spacer1_3 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout11.addItem(spacer1_3,2,2)

        self.lblIsA = QLabel(self.gbGeneral,"lblIsA")

        layout11.addWidget(self.lblIsA,0,3)

        self.lblPartOf5 = QLabel(self.gbGeneral,"lblPartOf5")

        layout11.addWidget(self.lblPartOf5,1,3)

        self.lblHomepage = QLabel(self.gbGeneral,"lblHomepage")

        layout11.addWidget(self.lblHomepage,1,0)

        layout10 = QHBoxLayout(None,0,6,"layout10")

        self.lePackager = KLineEdit(self.gbGeneral,"lePackager")
        layout10.addWidget(self.lePackager)

        self.pbPackager = KPushButton(self.gbGeneral,"pbPackager")
        layout10.addWidget(self.pbPackager)

        layout11.addLayout(layout10,2,4)
        gbGeneralLayout.addLayout(layout11)
        spacer4 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        gbGeneralLayout.addItem(spacer4)

        layout30 = QHBoxLayout(None,0,6,"layout30")

        self.twSource = QTabWidget(self.gbGeneral,"twSource")

        self.archive = QWidget(self.twSource,"archive")
        archiveLayout = QVBoxLayout(self.archive,11,6,"archiveLayout")

        layout72 = QGridLayout(None,1,1,0,10,"layout72")

        self.lblType = QLabel(self.archive,"lblType")

        layout72.addWidget(self.lblType,2,0)

        self.lblSHA1 = QLabel(self.archive,"lblSHA1")

        layout72.addWidget(self.lblSHA1,1,0)

        self.lblURI = QLabel(self.archive,"lblURI")

        layout72.addWidget(self.lblURI,0,0)

        self.leURI = KLineEdit(self.archive,"leURI")

        layout72.addWidget(self.leURI,0,2)

        self.cbType = KComboBox(0,self.archive,"cbType")

        layout72.addWidget(self.cbType,2,2)
        spacer5_2 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout72.addItem(spacer5_2,1,1)
        spacer5 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout72.addItem(spacer5,0,1)
        spacer5_3 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout72.addItem(spacer5_3,2,1)

        self.leSHA1 = KLineEdit(self.archive,"leSHA1")

        layout72.addWidget(self.leSHA1,1,2)
        archiveLayout.addLayout(layout72)
        spacer8 = QSpacerItem(20,5,QSizePolicy.Minimum,QSizePolicy.Minimum)
        archiveLayout.addItem(spacer8)
        self.twSource.insertTab(self.archive,QString.fromLatin1(""))

        self.TabPage = QWidget(self.twSource,"TabPage")
        TabPageLayout = QHBoxLayout(self.TabPage,11,6,"TabPageLayout")

        self.lvSummary = KListView(self.TabPage,"lvSummary")
        self.lvSummary.addColumn(self.__tr("Language"))
        self.lvSummary.header().setClickEnabled(0,self.lvSummary.header().count() - 1)
        self.lvSummary.addColumn(self.__tr("Summary"))
        self.lvSummary.header().setClickEnabled(0,self.lvSummary.header().count() - 1)
        self.lvSummary.addColumn(self.__tr("Description"))
        self.lvSummary.header().setClickEnabled(0,self.lvSummary.header().count() - 1)
        self.lvSummary.setAllColumnsShowFocus(1)
        self.lvSummary.setResizeMode(KListView.LastColumn)
        TabPageLayout.addWidget(self.lvSummary)

        layout15_2 = QVBoxLayout(None,0,6,"layout15_2")

        self.pbAddSummary = KPushButton(self.TabPage,"pbAddSummary")
        layout15_2.addWidget(self.pbAddSummary)

        self.pbRemoveSummary = KPushButton(self.TabPage,"pbRemoveSummary")
        layout15_2.addWidget(self.pbRemoveSummary)
        spacer9_3_2 = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout15_2.addItem(spacer9_3_2)

        self.pbBrowseSummary = KPushButton(self.TabPage,"pbBrowseSummary")
        layout15_2.addWidget(self.pbBrowseSummary)
        TabPageLayout.addLayout(layout15_2)
        self.twSource.insertTab(self.TabPage,QString.fromLatin1(""))

        self.TabPage_2 = QWidget(self.twSource,"TabPage_2")
        TabPageLayout_2 = QHBoxLayout(self.TabPage_2,11,6,"TabPageLayout_2")

        self.lvBuildDep = KListView(self.TabPage_2,"lvBuildDep")
        self.lvBuildDep.addColumn(self.__tr("Condition"))
        self.lvBuildDep.header().setClickEnabled(0,self.lvBuildDep.header().count() - 1)
        self.lvBuildDep.addColumn(self.__tr("Dependency"))
        self.lvBuildDep.header().setClickEnabled(0,self.lvBuildDep.header().count() - 1)
        self.lvBuildDep.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred,0,0,self.lvBuildDep.sizePolicy().hasHeightForWidth()))
        self.lvBuildDep.setAllColumnsShowFocus(1)
        self.lvBuildDep.setResizeMode(KListView.LastColumn)
        TabPageLayout_2.addWidget(self.lvBuildDep)

        layout15_2_2 = QVBoxLayout(None,0,6,"layout15_2_2")

        self.pbAddBuildDep = KPushButton(self.TabPage_2,"pbAddBuildDep")
        layout15_2_2.addWidget(self.pbAddBuildDep)

        self.pbRemoveBuildDep = KPushButton(self.TabPage_2,"pbRemoveBuildDep")
        layout15_2_2.addWidget(self.pbRemoveBuildDep)
        spacer9_3_2_2 = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout15_2_2.addItem(spacer9_3_2_2)

        self.pbBrowseBuildDep = KPushButton(self.TabPage_2,"pbBrowseBuildDep")
        layout15_2_2.addWidget(self.pbBrowseBuildDep)
        TabPageLayout_2.addLayout(layout15_2_2)
        self.twSource.insertTab(self.TabPage_2,QString.fromLatin1(""))

        self.TabPage_3 = QWidget(self.twSource,"TabPage_3")
        TabPageLayout_3 = QHBoxLayout(self.TabPage_3,11,6,"TabPageLayout_3")

        self.lvPatches = KListView(self.TabPage_3,"lvPatches")
        self.lvPatches.addColumn(self.__tr("Level"))
        self.lvPatches.header().setClickEnabled(0,self.lvPatches.header().count() - 1)
        self.lvPatches.addColumn(self.__tr("Compression Type"))
        self.lvPatches.header().setClickEnabled(0,self.lvPatches.header().count() - 1)
        self.lvPatches.addColumn(self.__tr("Patch"))
        self.lvPatches.header().setClickEnabled(0,self.lvPatches.header().count() - 1)
        self.lvPatches.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred,0,0,self.lvPatches.sizePolicy().hasHeightForWidth()))
        self.lvPatches.setAllColumnsShowFocus(1)
        self.lvPatches.setResizeMode(KListView.LastColumn)
        TabPageLayout_3.addWidget(self.lvPatches)

        layout21 = QVBoxLayout(None,0,6,"layout21")

        self.pbAddPatch = KPushButton(self.TabPage_3,"pbAddPatch")
        layout21.addWidget(self.pbAddPatch)

        self.pbRemovePatch = KPushButton(self.TabPage_3,"pbRemovePatch")
        layout21.addWidget(self.pbRemovePatch)
        spacer9_3 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout21.addItem(spacer9_3)

        self.pbViewPatch = KPushButton(self.TabPage_3,"pbViewPatch")
        layout21.addWidget(self.pbViewPatch)

        self.pbBrowsePatch = KPushButton(self.TabPage_3,"pbBrowsePatch")
        layout21.addWidget(self.pbBrowsePatch)
        TabPageLayout_3.addLayout(layout21)
        self.twSource.insertTab(self.TabPage_3,QString.fromLatin1(""))
        layout30.addWidget(self.twSource)
        gbGeneralLayout.addLayout(layout30)

        SourceWidgetUILayout.addWidget(self.gbGeneral,0,0)

        self.languageChange()

        self.resize(QSize(667,340).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.leName,self.leIsA)
        self.setTabOrder(self.leIsA,self.pbIsA)
        self.setTabOrder(self.pbIsA,self.leHomepage)
        self.setTabOrder(self.leHomepage,self.lePartOf)
        self.setTabOrder(self.lePartOf,self.leLicense)
        self.setTabOrder(self.leLicense,self.pbLicense)
        self.setTabOrder(self.pbLicense,self.pbPackager)
        self.setTabOrder(self.pbPackager,self.twSource)
        self.setTabOrder(self.twSource,self.leURI)
        self.setTabOrder(self.leURI,self.cbType)
        self.setTabOrder(self.cbType,self.leSHA1)
        self.setTabOrder(self.leSHA1,self.lvSummary)
        self.setTabOrder(self.lvSummary,self.pbAddSummary)
        self.setTabOrder(self.pbAddSummary,self.pbRemoveSummary)
        self.setTabOrder(self.pbRemoveSummary,self.pbBrowseSummary)
        self.setTabOrder(self.pbBrowseSummary,self.lvBuildDep)
        self.setTabOrder(self.lvBuildDep,self.lvPatches)
        self.setTabOrder(self.lvPatches,self.pbAddPatch)
        self.setTabOrder(self.pbAddPatch,self.pbRemovePatch)
        self.setTabOrder(self.pbRemovePatch,self.pbBrowsePatch)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.gbGeneral.setTitle(self.__tr("General"))
        self.lblName.setText(self.__tr("Name:"))
        self.pbLicense.setText(QString.null)
        self.lblLicense.setText(self.__tr("License:"))
        self.pbIsA.setText(QString.null)
        self.lblPackager.setText(self.__tr("Packager:"))
        self.lblIsA.setText(self.__tr("Is A:"))
        self.lblPartOf5.setText(self.__tr("Part Of:"))
        self.lblHomepage.setText(self.__tr("Homepage:"))
        self.pbPackager.setText(QString.null)
        self.lblType.setText(self.__tr("Type:"))
        self.lblSHA1.setText(self.__tr("SHA1:"))
        self.lblURI.setText(self.__tr("URI:"))
        self.cbType.clear()
        self.cbType.insertItem(self.__tr("targz"))
        self.cbType.insertItem(self.__tr("tarbz2"))
        self.cbType.insertItem(self.__tr("gzip"))
        self.cbType.insertItem(self.__tr("zip"))
        self.cbType.insertItem(self.__tr("tar"))
        self.cbType.insertItem(self.__tr("tarlzma"))
        self.cbType.insertItem(self.__tr("binary"))
        self.twSource.changeTab(self.archive,self.__tr("Archive"))
        self.lvSummary.header().setLabel(0,self.__tr("Language"))
        self.lvSummary.header().setLabel(1,self.__tr("Summary"))
        self.lvSummary.header().setLabel(2,self.__tr("Description"))
        self.pbAddSummary.setText(QString.null)
        self.pbRemoveSummary.setText(QString.null)
        self.pbBrowseSummary.setText(QString.null)
        self.twSource.changeTab(self.TabPage,self.__tr("Summary && Description"))
        self.lvBuildDep.header().setLabel(0,self.__tr("Condition"))
        self.lvBuildDep.header().setLabel(1,self.__tr("Dependency"))
        self.pbAddBuildDep.setText(QString.null)
        self.pbRemoveBuildDep.setText(QString.null)
        self.pbBrowseBuildDep.setText(QString.null)
        self.twSource.changeTab(self.TabPage_2,self.__tr("Build Dependencies"))
        self.lvPatches.header().setLabel(0,self.__tr("Level"))
        self.lvPatches.header().setLabel(1,self.__tr("Compression Type"))
        self.lvPatches.header().setLabel(2,self.__tr("Patch"))
        self.pbAddPatch.setText(QString.null)
        self.pbRemovePatch.setText(QString.null)
        self.pbViewPatch.setText(QString.null)
        self.pbBrowsePatch.setText(QString.null)
        self.twSource.changeTab(self.TabPage_3,self.__tr("Patches"))


    def __tr(self,s,c = None):
        return qApp.translate("SourceWidgetUI",s,c)
