# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../../uis/pspecWidget/packageWidgetUI.ui'
#
# Created: Pzt Eyl 3 22:16:58 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdeui import *



class PackageWidgetUI(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("PackageWidgetUI")


        PackageWidgetUILayout = QHBoxLayout(self,11,6,"PackageWidgetUILayout")

        self.gbPackage = QGroupBox(self,"gbPackage")
        self.gbPackage.setAlignment(QGroupBox.AlignHCenter)
        self.gbPackage.setFlat(1)
        self.gbPackage.setColumnLayout(0,Qt.Vertical)
        self.gbPackage.layout().setSpacing(6)
        self.gbPackage.layout().setMargin(11)
        gbPackageLayout = QVBoxLayout(self.gbPackage.layout())
        gbPackageLayout.setAlignment(Qt.AlignTop)

        layout30 = QGridLayout(None,1,1,0,6,"layout30")

        self.lblName = QLabel(self.gbPackage,"lblName")

        layout30.addWidget(self.lblName,0,0)

        self.lblsA = QLabel(self.gbPackage,"lblsA")

        layout30.addWidget(self.lblsA,0,3)

        self.lblLicense = QLabel(self.gbPackage,"lblLicense")

        layout30.addWidget(self.lblLicense,1,0)

        self.leName = KLineEdit(self.gbPackage,"leName")

        layout30.addWidget(self.leName,0,1)

        layout12 = QHBoxLayout(None,0,6,"layout12")

        self.leLicense = KLineEdit(self.gbPackage,"leLicense")
        layout12.addWidget(self.leLicense)

        self.pbLicense = KPushButton(self.gbPackage,"pbLicense")
        layout12.addWidget(self.pbLicense)

        layout30.addLayout(layout12,1,1)
        spacer1_2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout30.addItem(spacer1_2,1,2)

        self.lblPartOf = QLabel(self.gbPackage,"lblPartOf")

        layout30.addWidget(self.lblPartOf,1,3)

        layout11 = QHBoxLayout(None,0,6,"layout11")

        self.leIsA = KLineEdit(self.gbPackage,"leIsA")
        layout11.addWidget(self.leIsA)

        self.pbIsA = KPushButton(self.gbPackage,"pbIsA")
        self.pbIsA.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.pbIsA.sizePolicy().hasHeightForWidth()))
        layout11.addWidget(self.pbIsA)

        layout30.addLayout(layout11,0,4)
        spacer1 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout30.addItem(spacer1,0,2)

        self.lePartOf = KLineEdit(self.gbPackage,"lePartOf")

        layout30.addWidget(self.lePartOf,1,4)
        gbPackageLayout.addLayout(layout30)
        spacer4 = QSpacerItem(20,2,QSizePolicy.Minimum,QSizePolicy.Fixed)
        gbPackageLayout.addItem(spacer4)

        self.twPackage = QTabWidget(self.gbPackage,"twPackage")

        self.TabPage = QWidget(self.twPackage,"TabPage")
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
        self.twPackage.insertTab(self.TabPage,QString.fromLatin1(""))

        self.TabPage_2 = QWidget(self.twPackage,"TabPage_2")
        TabPageLayout_2 = QHBoxLayout(self.TabPage_2,11,6,"TabPageLayout_2")

        self.lvRuntimeDep = KListView(self.TabPage_2,"lvRuntimeDep")
        self.lvRuntimeDep.addColumn(self.__tr("Condition"))
        self.lvRuntimeDep.header().setClickEnabled(0,self.lvRuntimeDep.header().count() - 1)
        self.lvRuntimeDep.addColumn(self.__tr("Dependency"))
        self.lvRuntimeDep.header().setClickEnabled(0,self.lvRuntimeDep.header().count() - 1)
        self.lvRuntimeDep.setAllColumnsShowFocus(1)
        self.lvRuntimeDep.setResizeMode(KListView.LastColumn)
        TabPageLayout_2.addWidget(self.lvRuntimeDep)

        layout21 = QVBoxLayout(None,0,6,"layout21")

        self.pbAddRuntimeDep = KPushButton(self.TabPage_2,"pbAddRuntimeDep")
        layout21.addWidget(self.pbAddRuntimeDep)

        self.pbRemoveRuntimeDep = KPushButton(self.TabPage_2,"pbRemoveRuntimeDep")
        layout21.addWidget(self.pbRemoveRuntimeDep)
        spacer9_2 = QSpacerItem(20,110,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout21.addItem(spacer9_2)

        self.pbBrowseRuntimeDep = KPushButton(self.TabPage_2,"pbBrowseRuntimeDep")
        layout21.addWidget(self.pbBrowseRuntimeDep)
        TabPageLayout_2.addLayout(layout21)
        self.twPackage.insertTab(self.TabPage_2,QString.fromLatin1(""))

        self.TabPage_3 = QWidget(self.twPackage,"TabPage_3")
        TabPageLayout_3 = QHBoxLayout(self.TabPage_3,11,6,"TabPageLayout_3")

        self.lvReplaces = KListView(self.TabPage_3,"lvReplaces")
        self.lvReplaces.addColumn(self.__tr("Condition"))
        self.lvReplaces.header().setClickEnabled(0,self.lvReplaces.header().count() - 1)
        self.lvReplaces.addColumn(self.__tr("Package"))
        self.lvReplaces.header().setClickEnabled(0,self.lvReplaces.header().count() - 1)
        self.lvReplaces.setAllColumnsShowFocus(1)
        self.lvReplaces.setResizeMode(KListView.LastColumn)
        TabPageLayout_3.addWidget(self.lvReplaces)

        layout22 = QVBoxLayout(None,0,6,"layout22")

        self.pbAddReplaces = KPushButton(self.TabPage_3,"pbAddReplaces")
        layout22.addWidget(self.pbAddReplaces)

        self.pbRemoveReplaces = KPushButton(self.TabPage_3,"pbRemoveReplaces")
        layout22.addWidget(self.pbRemoveReplaces)
        spacer9_2_2 = QSpacerItem(20,160,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout22.addItem(spacer9_2_2)

        self.pbBrowseReplaces = KPushButton(self.TabPage_3,"pbBrowseReplaces")
        layout22.addWidget(self.pbBrowseReplaces)
        TabPageLayout_3.addLayout(layout22)
        self.twPackage.insertTab(self.TabPage_3,QString.fromLatin1(""))

        self.TabPage_4 = QWidget(self.twPackage,"TabPage_4")
        TabPageLayout_4 = QHBoxLayout(self.TabPage_4,11,6,"TabPageLayout_4")

        self.lvFiles = KListView(self.TabPage_4,"lvFiles")
        self.lvFiles.addColumn(self.__tr("Type"))
        self.lvFiles.header().setClickEnabled(0,self.lvFiles.header().count() - 1)
        self.lvFiles.addColumn(self.__tr("Permanent?"))
        self.lvFiles.header().setClickEnabled(0,self.lvFiles.header().count() - 1)
        self.lvFiles.addColumn(self.__tr("Path"))
        self.lvFiles.header().setClickEnabled(0,self.lvFiles.header().count() - 1)
        self.lvFiles.setAllColumnsShowFocus(1)
        self.lvFiles.setResizeMode(KListView.LastColumn)
        TabPageLayout_4.addWidget(self.lvFiles)

        layout23 = QVBoxLayout(None,0,6,"layout23")

        self.pbAddFile = KPushButton(self.TabPage_4,"pbAddFile")
        layout23.addWidget(self.pbAddFile)

        self.pbRemoveFile = KPushButton(self.TabPage_4,"pbRemoveFile")
        layout23.addWidget(self.pbRemoveFile)
        spacer9_3 = QSpacerItem(20,120,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout23.addItem(spacer9_3)

        self.pbBrowseFile = KPushButton(self.TabPage_4,"pbBrowseFile")
        layout23.addWidget(self.pbBrowseFile)
        TabPageLayout_4.addLayout(layout23)
        self.twPackage.insertTab(self.TabPage_4,QString.fromLatin1(""))

        self.TabPage_5 = QWidget(self.twPackage,"TabPage_5")
        TabPageLayout_5 = QHBoxLayout(self.TabPage_5,11,6,"TabPageLayout_5")

        self.lvAdditionalFiles = KListView(self.TabPage_5,"lvAdditionalFiles")
        self.lvAdditionalFiles.addColumn(self.__tr("Owner"))
        self.lvAdditionalFiles.header().setClickEnabled(0,self.lvAdditionalFiles.header().count() - 1)
        self.lvAdditionalFiles.addColumn(self.__tr("Permission"))
        self.lvAdditionalFiles.header().setClickEnabled(0,self.lvAdditionalFiles.header().count() - 1)
        self.lvAdditionalFiles.addColumn(self.__tr("Target"))
        self.lvAdditionalFiles.header().setClickEnabled(0,self.lvAdditionalFiles.header().count() - 1)
        self.lvAdditionalFiles.addColumn(self.__tr("File"))
        self.lvAdditionalFiles.header().setClickEnabled(0,self.lvAdditionalFiles.header().count() - 1)
        self.lvAdditionalFiles.setAllColumnsShowFocus(1)
        self.lvAdditionalFiles.setResizeMode(KListView.LastColumn)
        TabPageLayout_5.addWidget(self.lvAdditionalFiles)

        layout27 = QVBoxLayout(None,0,6,"layout27")

        self.pbAddAdditional = KPushButton(self.TabPage_5,"pbAddAdditional")
        layout27.addWidget(self.pbAddAdditional)

        self.pbRemoveAdditional = KPushButton(self.TabPage_5,"pbRemoveAdditional")
        layout27.addWidget(self.pbRemoveAdditional)
        spacer9_3_2_2 = QSpacerItem(20,160,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout27.addItem(spacer9_3_2_2)

        self.pbViewAdditional = KPushButton(self.TabPage_5,"pbViewAdditional")
        layout27.addWidget(self.pbViewAdditional)

        self.pbBrowseAdditional = KPushButton(self.TabPage_5,"pbBrowseAdditional")
        layout27.addWidget(self.pbBrowseAdditional)
        TabPageLayout_5.addLayout(layout27)
        self.twPackage.insertTab(self.TabPage_5,QString.fromLatin1(""))

        self.TabPage_6 = QWidget(self.twPackage,"TabPage_6")
        TabPageLayout_6 = QHBoxLayout(self.TabPage_6,11,6,"TabPageLayout_6")

        self.lvConflicts = KListView(self.TabPage_6,"lvConflicts")
        self.lvConflicts.addColumn(self.__tr("Condition"))
        self.lvConflicts.header().setClickEnabled(0,self.lvConflicts.header().count() - 1)
        self.lvConflicts.addColumn(self.__tr("Package"))
        self.lvConflicts.header().setClickEnabled(0,self.lvConflicts.header().count() - 1)
        self.lvConflicts.setAllColumnsShowFocus(1)
        self.lvConflicts.setResizeMode(KListView.LastColumn)
        TabPageLayout_6.addWidget(self.lvConflicts)

        layout24 = QVBoxLayout(None,0,6,"layout24")

        self.pbAddConflict = KPushButton(self.TabPage_6,"pbAddConflict")
        layout24.addWidget(self.pbAddConflict)

        self.pbRemoveConflict = KPushButton(self.TabPage_6,"pbRemoveConflict")
        layout24.addWidget(self.pbRemoveConflict)
        spacer9_3_3 = QSpacerItem(20,120,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout24.addItem(spacer9_3_3)

        self.pbBrowseConflict = KPushButton(self.TabPage_6,"pbBrowseConflict")
        layout24.addWidget(self.pbBrowseConflict)
        TabPageLayout_6.addLayout(layout24)
        self.twPackage.insertTab(self.TabPage_6,QString.fromLatin1(""))

        self.TabPage_7 = QWidget(self.twPackage,"TabPage_7")
        TabPageLayout_7 = QGridLayout(self.TabPage_7,1,1,11,6,"TabPageLayout_7")

        self.lvCOMAR = KListView(self.TabPage_7,"lvCOMAR")
        self.lvCOMAR.addColumn(self.__tr("Provides"))
        self.lvCOMAR.header().setClickEnabled(0,self.lvCOMAR.header().count() - 1)
        self.lvCOMAR.addColumn(self.__tr("Script"))
        self.lvCOMAR.header().setClickEnabled(0,self.lvCOMAR.header().count() - 1)
        self.lvCOMAR.setAllColumnsShowFocus(1)
        self.lvCOMAR.setResizeMode(KListView.LastColumn)

        TabPageLayout_7.addWidget(self.lvCOMAR,0,0)

        layout28 = QVBoxLayout(None,0,6,"layout28")

        self.pbAddCOMAR = KPushButton(self.TabPage_7,"pbAddCOMAR")
        layout28.addWidget(self.pbAddCOMAR)

        self.pbRemoveCOMAR = KPushButton(self.TabPage_7,"pbRemoveCOMAR")
        layout28.addWidget(self.pbRemoveCOMAR)
        spacer9_3_2_2_2 = QSpacerItem(20,170,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout28.addItem(spacer9_3_2_2_2)

        self.pbViewCOMAR = KPushButton(self.TabPage_7,"pbViewCOMAR")
        layout28.addWidget(self.pbViewCOMAR)

        self.pbBrowseCOMAR = KPushButton(self.TabPage_7,"pbBrowseCOMAR")
        layout28.addWidget(self.pbBrowseCOMAR)

        TabPageLayout_7.addLayout(layout28,0,1)
        self.twPackage.insertTab(self.TabPage_7,QString.fromLatin1(""))
        gbPackageLayout.addWidget(self.twPackage)
        PackageWidgetUILayout.addWidget(self.gbPackage)

        self.languageChange()

        self.resize(QSize(689,440).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.gbPackage.setTitle(self.__tr("General"))
        self.lblName.setText(self.__tr("Name:"))
        self.lblsA.setText(self.__tr("Is A:"))
        self.lblLicense.setText(self.__tr("License:"))
        self.pbLicense.setText(QString.null)
        self.lblPartOf.setText(self.__tr("Part Of:"))
        self.pbIsA.setText(QString.null)
        self.lvSummary.header().setLabel(0,self.__tr("Language"))
        self.lvSummary.header().setLabel(1,self.__tr("Summary"))
        self.lvSummary.header().setLabel(2,self.__tr("Description"))
        self.pbAddSummary.setText(QString.null)
        self.pbRemoveSummary.setText(QString.null)
        self.pbBrowseSummary.setText(QString.null)
        self.twPackage.changeTab(self.TabPage,self.__tr("Summary && Description"))
        self.lvRuntimeDep.header().setLabel(0,self.__tr("Condition"))
        self.lvRuntimeDep.header().setLabel(1,self.__tr("Dependency"))
        self.pbAddRuntimeDep.setText(QString.null)
        self.pbRemoveRuntimeDep.setText(QString.null)
        self.pbBrowseRuntimeDep.setText(QString.null)
        self.twPackage.changeTab(self.TabPage_2,self.__tr("Runtime Dependencies"))
        self.lvReplaces.header().setLabel(0,self.__tr("Condition"))
        self.lvReplaces.header().setLabel(1,self.__tr("Package"))
        self.pbAddReplaces.setText(QString.null)
        self.pbRemoveReplaces.setText(QString.null)
        self.pbBrowseReplaces.setText(QString.null)
        self.twPackage.changeTab(self.TabPage_3,self.__tr("Replaces"))
        self.lvFiles.header().setLabel(0,self.__tr("Type"))
        self.lvFiles.header().setLabel(1,self.__tr("Permanent?"))
        self.lvFiles.header().setLabel(2,self.__tr("Path"))
        self.pbAddFile.setText(QString.null)
        self.pbRemoveFile.setText(QString.null)
        self.pbBrowseFile.setText(QString.null)
        self.twPackage.changeTab(self.TabPage_4,self.__tr("Files"))
        self.lvAdditionalFiles.header().setLabel(0,self.__tr("Owner"))
        self.lvAdditionalFiles.header().setLabel(1,self.__tr("Permission"))
        self.lvAdditionalFiles.header().setLabel(2,self.__tr("Target"))
        self.lvAdditionalFiles.header().setLabel(3,self.__tr("File"))
        self.pbAddAdditional.setText(QString.null)
        self.pbRemoveAdditional.setText(QString.null)
        self.pbViewAdditional.setText(QString.null)
        self.pbBrowseAdditional.setText(QString.null)
        self.twPackage.changeTab(self.TabPage_5,self.__tr("Additional Files"))
        self.lvConflicts.header().setLabel(0,self.__tr("Condition"))
        self.lvConflicts.header().setLabel(1,self.__tr("Package"))
        self.pbAddConflict.setText(QString.null)
        self.pbRemoveConflict.setText(QString.null)
        self.pbBrowseConflict.setText(QString.null)
        self.twPackage.changeTab(self.TabPage_6,self.__tr("Conflicts"))
        self.lvCOMAR.header().setLabel(0,self.__tr("Provides"))
        self.lvCOMAR.header().setLabel(1,self.__tr("Script"))
        self.pbAddCOMAR.setText(QString.null)
        self.pbRemoveCOMAR.setText(QString.null)
        self.pbViewCOMAR.setText(QString.null)
        self.pbBrowseCOMAR.setText(QString.null)
        self.twPackage.changeTab(self.TabPage_7,self.__tr("COMAR Scripts"))


    def __tr(self,s,c = None):
        return qApp.translate("PackageWidgetUI",s,c)
