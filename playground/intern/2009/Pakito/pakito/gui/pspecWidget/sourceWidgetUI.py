# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pakito/gui/pspecWidget/sourceWidgetUI.ui'
#
# Created: Sal Ağu 5 10:45:06 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
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
        gbGeneralLayout.addItem(spacer4,3,3)

        self.lblName = QLabel(self.gbGeneral,"lblName")

        gbGeneralLayout.addWidget(self.lblName,0,0)
        spacer1 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        gbGeneralLayout.addItem(spacer1,0,3)

        self.lblLicense = QLabel(self.gbGeneral,"lblLicense")

        gbGeneralLayout.addWidget(self.lblLicense,2,0)

        self.leName = KLineEdit(self.gbGeneral,"leName")

        gbGeneralLayout.addMultiCellWidget(self.leName,0,0,1,2)
        spacer1_2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        gbGeneralLayout.addItem(spacer1_2,1,3)

        self.leHomepage = KLineEdit(self.gbGeneral,"leHomepage")

        gbGeneralLayout.addMultiCellWidget(self.leHomepage,1,1,1,2)

        self.lePartOf = KLineEdit(self.gbGeneral,"lePartOf")

        gbGeneralLayout.addMultiCellWidget(self.lePartOf,1,1,5,6)
        spacer1_3 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        gbGeneralLayout.addItem(spacer1_3,2,3)

        self.lblIsA = QLabel(self.gbGeneral,"lblIsA")

        gbGeneralLayout.addWidget(self.lblIsA,0,4)

        self.lblPartOf5 = QLabel(self.gbGeneral,"lblPartOf5")

        gbGeneralLayout.addWidget(self.lblPartOf5,1,4)

        self.lblHomepage = QLabel(self.gbGeneral,"lblHomepage")

        gbGeneralLayout.addWidget(self.lblHomepage,1,0)

        self.leLicense = KLineEdit(self.gbGeneral,"leLicense")

        gbGeneralLayout.addWidget(self.leLicense,2,1)

        self.pbLicense = KPushButton(self.gbGeneral,"pbLicense")

        gbGeneralLayout.addWidget(self.pbLicense,2,2)

        self.pbIsA = KPushButton(self.gbGeneral,"pbIsA")
        self.pbIsA.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.pbIsA.sizePolicy().hasHeightForWidth()))

        gbGeneralLayout.addWidget(self.pbIsA,0,6)

        self.leIsA = KLineEdit(self.gbGeneral,"leIsA")

        gbGeneralLayout.addWidget(self.leIsA,0,5)

        self.lblPackager = QLabel(self.gbGeneral,"lblPackager")
        self.lblPackager.setFrameShape(QLabel.NoFrame)
        self.lblPackager.setFrameShadow(QLabel.Plain)

        gbGeneralLayout.addWidget(self.lblPackager,2,4)

        layout4 = QHBoxLayout(None,0,6,"layout4")

        self.lePackager = KLineEdit(self.gbGeneral,"lePackager")
        layout4.addWidget(self.lePackager)

        self.lblPackager_2 = QLabel(self.gbGeneral,"lblPackager_2")
        self.lblPackager_2.setFrameShape(QLabel.NoFrame)
        self.lblPackager_2.setFrameShadow(QLabel.Plain)
        layout4.addWidget(self.lblPackager_2)

        self.leEmail = KLineEdit(self.gbGeneral,"leEmail")
        layout4.addWidget(self.leEmail)

        gbGeneralLayout.addMultiCellLayout(layout4,2,2,5,6)

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
        self.lvSummary.addColumn(i18n("Language"))
        self.lvSummary.header().setClickEnabled(0,self.lvSummary.header().count() - 1)
        self.lvSummary.addColumn(i18n("Summary"))
        self.lvSummary.header().setClickEnabled(0,self.lvSummary.header().count() - 1)
        self.lvSummary.addColumn(i18n("Description"))
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
        self.lvBuildDep.addColumn(i18n("Condition"))
        self.lvBuildDep.header().setClickEnabled(0,self.lvBuildDep.header().count() - 1)
        self.lvBuildDep.addColumn(i18n("Dependency"))
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
        self.lvPatches.addColumn(i18n("Level"))
        self.lvPatches.header().setClickEnabled(0,self.lvPatches.header().count() - 1)
        self.lvPatches.addColumn(i18n("Compression Type"))
        self.lvPatches.header().setClickEnabled(0,self.lvPatches.header().count() - 1)
        self.lvPatches.addColumn(i18n("Patch"))
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

        gbGeneralLayout.addMultiCellWidget(self.twSource,4,4,0,6)
        SourceWidgetUILayout.addWidget(self.gbGeneral)

        self.languageChange()

        self.resize(QSize(907,358).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.leName,self.leHomepage)
        self.setTabOrder(self.leHomepage,self.leLicense)
        self.setTabOrder(self.leLicense,self.pbLicense)
        self.setTabOrder(self.pbLicense,self.leIsA)
        self.setTabOrder(self.leIsA,self.pbIsA)
        self.setTabOrder(self.pbIsA,self.lePartOf)
        self.setTabOrder(self.lePartOf,self.lePackager)
        self.setTabOrder(self.lePackager,self.twSource)
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
        self.setCaption(i18n("Form1"))
        self.gbGeneral.setTitle(i18n("General"))
        self.lblName.setText(i18n("Name:"))
        self.lblLicense.setText(i18n("License:"))
        self.lblIsA.setText(i18n("Is A:"))
        self.lblPartOf5.setText(i18n("Part Of:"))
        self.lblHomepage.setText(i18n("Homepage:"))
        self.pbLicense.setText(QString.null)
        QToolTip.add(self.pbLicense,i18n("Add a common license"))
        self.pbIsA.setText(QString.null)
        QToolTip.add(self.pbIsA,i18n("Choose a category"))
        self.lblPackager.setText(i18n("Packager:"))
        self.lblPackager_2.setText(i18n("E-Mail:"))
        self.lblType.setText(i18n("Type:"))
        self.lblSHA1.setText(i18n("SHA1:"))
        self.lblURI.setText(i18n("URI:"))
        self.cbType.clear()
        self.cbType.insertItem(i18n("targz"))
        self.cbType.insertItem(i18n("tarbz2"))
        self.cbType.insertItem(i18n("gzip"))
        self.cbType.insertItem(i18n("zip"))
        self.cbType.insertItem(i18n("tar"))
        self.cbType.insertItem(i18n("tarlzma"))
        self.cbType.insertItem(i18n("binary"))
        self.twSource.changeTab(self.archive,i18n("Archive"))
        self.lvSummary.header().setLabel(0,i18n("Language"))
        self.lvSummary.header().setLabel(1,i18n("Summary"))
        self.lvSummary.header().setLabel(2,i18n("Description"))
        self.pbAddSummary.setText(QString.null)
        QToolTip.add(self.pbAddSummary,i18n("Add new summary/description"))
        self.pbRemoveSummary.setText(QString.null)
        QToolTip.add(self.pbRemoveSummary,i18n("Remove selected summary/description"))
        self.pbBrowseSummary.setText(QString.null)
        QToolTip.add(self.pbBrowseSummary,i18n("Edit summary/description"))
        self.twSource.changeTab(self.TabPage,i18n("Summary && Description"))
        self.lvBuildDep.header().setLabel(0,i18n("Condition"))
        self.lvBuildDep.header().setLabel(1,i18n("Dependency"))
        self.pbAddBuildDep.setText(QString.null)
        QToolTip.add(self.pbAddBuildDep,i18n("Add build dependency"))
        self.pbRemoveBuildDep.setText(QString.null)
        QToolTip.add(self.pbRemoveBuildDep,i18n("Remove build dependency"))
        self.pbBrowseBuildDep.setText(QString.null)
        QToolTip.add(self.pbBrowseBuildDep,i18n("Edit build dependency"))
        self.twSource.changeTab(self.TabPage_2,i18n("Build Dependencies"))
        self.lvPatches.header().setLabel(0,i18n("Level"))
        self.lvPatches.header().setLabel(1,i18n("Compression Type"))
        self.lvPatches.header().setLabel(2,i18n("Patch"))
        self.pbAddPatch.setText(QString.null)
        QToolTip.add(self.pbAddPatch,i18n("Add patch"))
        self.pbRemovePatch.setText(QString.null)
        QToolTip.add(self.pbRemovePatch,i18n("Remove patch"))
        self.pbViewPatch.setText(QString.null)
        QToolTip.add(self.pbViewPatch,i18n("Open patch file"))
        self.pbBrowsePatch.setText(QString.null)
        QToolTip.add(self.pbBrowsePatch,i18n("Edit patch entry"))
        self.twSource.changeTab(self.TabPage_3,i18n("Patches"))

