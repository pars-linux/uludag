# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../../uis/pspecWidget/sourceWidgetUI.ui'
#
# Created: Sal Eyl 4 22:38:24 2007
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


        SourceWidgetUILayout = QHBoxLayout(self,11,6,"SourceWidgetUILayout")

        self.gbGeneral = QGroupBox(self,"gbGeneral")
        self.gbGeneral.setFrameShape(QGroupBox.GroupBoxPanel)
        self.gbGeneral.setFrameShadow(QGroupBox.Sunken)
        self.gbGeneral.setAlignment(QGroupBox.WordBreak | QGroupBox.AlignCenter | QGroupBox.AlignBottom | QGroupBox.AlignTop)
        self.gbGeneral.setFlat(1)
        self.gbGeneral.setColumnLayout(0,Qt.Vertical)
        self.gbGeneral.layout().setSpacing(6)
        self.gbGeneral.layout().setMargin(11)
        gbGeneralLayout = QGridLayout(self.gbGeneral.layout())
        gbGeneralLayout.setAlignment(Qt.AlignTop)
        spacer4 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        gbGeneralLayout.addItem(spacer4,1,0)

        self.twSource = QTabWidget(self.gbGeneral,"twSource")
        self.twSource.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.twSource.sizePolicy().hasHeightForWidth()))

        self.archive = QWidget(self.twSource,"archive")
        archiveLayout = QGridLayout(self.archive,1,1,11,6,"archiveLayout")
        spacer8 = QSpacerItem(20,5,QSizePolicy.Minimum,QSizePolicy.Preferred)
        archiveLayout.addItem(spacer8,3,2)

        self.lblType = QLabel(self.archive,"lblType")

        archiveLayout.addWidget(self.lblType,2,0)

        self.lblSHA1 = QLabel(self.archive,"lblSHA1")

        archiveLayout.addWidget(self.lblSHA1,1,0)

        self.lblURI = QLabel(self.archive,"lblURI")

        archiveLayout.addWidget(self.lblURI,0,0)

        self.leURI = KLineEdit(self.archive,"leURI")

        archiveLayout.addWidget(self.leURI,0,2)

        self.cbType = KComboBox(0,self.archive,"cbType")

        archiveLayout.addWidget(self.cbType,2,2)
        spacer5_2 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        archiveLayout.addItem(spacer5_2,1,1)
        spacer5 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        archiveLayout.addItem(spacer5,0,1)
        spacer5_3 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        archiveLayout.addItem(spacer5_3,2,1)

        self.leSHA1 = KLineEdit(self.archive,"leSHA1")

        archiveLayout.addWidget(self.leSHA1,1,2)
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
        self.lvSummary.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred,0,0,self.lvSummary.sizePolicy().hasHeightForWidth()))
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

        gbGeneralLayout.addMultiCellWidget(self.twSource,2,2,0,1)

        layout11 = QGridLayout(None,1,1,0,6,"layout11")

        self.lblIsA = QLabel(self.gbGeneral,"lblIsA")

        layout11.addWidget(self.lblIsA,0,0)

        self.lePartOf = KLineEdit(self.gbGeneral,"lePartOf")

        layout11.addWidget(self.lePartOf,1,1)

        layout10 = QHBoxLayout(None,0,6,"layout10")

        self.leIsA = KLineEdit(self.gbGeneral,"leIsA")
        layout10.addWidget(self.leIsA)

        self.pbIsA = KPushButton(self.gbGeneral,"pbIsA")
        self.pbIsA.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.pbIsA.sizePolicy().hasHeightForWidth()))
        layout10.addWidget(self.pbIsA)

        layout11.addLayout(layout10,0,1)

        layout9 = QHBoxLayout(None,0,6,"layout9")

        self.lePackager = KLineEdit(self.gbGeneral,"lePackager")
        layout9.addWidget(self.lePackager)

        self.textLabel1 = QLabel(self.gbGeneral,"textLabel1")
        layout9.addWidget(self.textLabel1)

        self.leEmail = KLineEdit(self.gbGeneral,"leEmail")
        layout9.addWidget(self.leEmail)

        layout11.addLayout(layout9,2,1)

        self.lblPackager = QLabel(self.gbGeneral,"lblPackager")
        self.lblPackager.setFrameShape(QLabel.NoFrame)
        self.lblPackager.setFrameShadow(QLabel.Plain)

        layout11.addWidget(self.lblPackager,2,0)

        self.lblPartOf5 = QLabel(self.gbGeneral,"lblPartOf5")

        layout11.addWidget(self.lblPartOf5,1,0)

        gbGeneralLayout.addLayout(layout11,0,1)

        layout12 = QGridLayout(None,1,1,0,6,"layout12")

        self.leHomepage = KLineEdit(self.gbGeneral,"leHomepage")

        layout12.addMultiCellWidget(self.leHomepage,1,1,1,2)

        self.leLicense = KLineEdit(self.gbGeneral,"leLicense")

        layout12.addWidget(self.leLicense,2,1)
        spacer1_2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout12.addItem(spacer1_2,1,3)

        self.leName = KLineEdit(self.gbGeneral,"leName")

        layout12.addMultiCellWidget(self.leName,0,0,1,2)

        self.lblName = QLabel(self.gbGeneral,"lblName")

        layout12.addWidget(self.lblName,0,0)

        self.lblHomepage = QLabel(self.gbGeneral,"lblHomepage")

        layout12.addWidget(self.lblHomepage,1,0)
        spacer1 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout12.addItem(spacer1,0,3)

        self.pbLicense = KPushButton(self.gbGeneral,"pbLicense")

        layout12.addWidget(self.pbLicense,2,2)

        self.lblLicense = QLabel(self.gbGeneral,"lblLicense")

        layout12.addWidget(self.lblLicense,2,0)
        spacer1_3 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout12.addItem(spacer1_3,2,3)

        gbGeneralLayout.addLayout(layout12,0,0)
        SourceWidgetUILayout.addWidget(self.gbGeneral)

        self.languageChange()

        self.resize(QSize(622,307).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.leName,self.leHomepage)
        self.setTabOrder(self.leHomepage,self.leLicense)
        self.setTabOrder(self.leLicense,self.pbLicense)
        self.setTabOrder(self.pbLicense,self.leIsA)
        self.setTabOrder(self.leIsA,self.pbIsA)
        self.setTabOrder(self.pbIsA,self.lePartOf)
        self.setTabOrder(self.lePartOf,self.lePackager)
        self.setTabOrder(self.lePackager,self.leEmail)
        self.setTabOrder(self.leEmail,self.twSource)
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
        self.setTabOrder(self.pbBrowsePatch,self.pbAddBuildDep)
        self.setTabOrder(self.pbAddBuildDep,self.pbRemoveBuildDep)
        self.setTabOrder(self.pbRemoveBuildDep,self.pbBrowseBuildDep)
        self.setTabOrder(self.pbBrowseBuildDep,self.pbViewPatch)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.gbGeneral.setTitle(self.__tr("General"))
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
        self.lblIsA.setText(self.__tr("Is A:"))
        self.pbIsA.setText(QString.null)
        self.textLabel1.setText(self.__tr("E-mail:"))
        self.lblPackager.setText(self.__tr("Packager:"))
        self.lblPartOf5.setText(self.__tr("Part Of:"))
        self.lblName.setText(self.__tr("Name:"))
        self.lblHomepage.setText(self.__tr("Homepage:"))
        self.pbLicense.setText(QString.null)
        self.lblLicense.setText(self.__tr("License:"))


    def __tr(self,s,c = None):
        return qApp.translate("SourceWidgetUI",s,c)
