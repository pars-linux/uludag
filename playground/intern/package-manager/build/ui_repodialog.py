# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/repodialog.ui'
#
# Created: Mon Jul  4 14:25:13 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

import gettext
__trans = gettext.translation('package-manager', fallback=True)
i18n = __trans.ugettext
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RepoDialog(object):
    def setupUi(self, RepoDialog):
        RepoDialog.setObjectName(_fromUtf8("RepoDialog"))
        RepoDialog.resize(373, 168)
        RepoDialog.setMinimumSize(QtCore.QSize(373, 168))
        RepoDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(RepoDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textLabel1 = QtGui.QLabel(RepoDialog)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName(_fromUtf8("textLabel1"))
        self.gridLayout.addWidget(self.textLabel1, 0, 0, 1, 2)
        self.repoName = QtGui.QLineEdit(RepoDialog)
        self.repoName.setObjectName(_fromUtf8("repoName"))
        self.gridLayout.addWidget(self.repoName, 1, 0, 1, 2)
        self.label = QtGui.QLabel(RepoDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.repoAddress = QtGui.QComboBox(RepoDialog)
        self.repoAddress.setEditable(True)
        self.repoAddress.setObjectName(_fromUtf8("repoAddress"))
        self.repoAddress.addItem(_fromUtf8(""))
        self.repoAddress.setItemText(0, _fromUtf8(""))
        self.gridLayout.addWidget(self.repoAddress, 3, 0, 1, 1)
        self.browseButton = QtGui.QPushButton(RepoDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browseButton.sizePolicy().hasHeightForWidth())
        self.browseButton.setSizePolicy(sizePolicy)
        self.browseButton.setMinimumSize(QtCore.QSize(20, 27))
        self.browseButton.setMaximumSize(QtCore.QSize(20, 27))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.gridLayout.addWidget(self.browseButton, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(17, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RepoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)

        self.retranslateUi(RepoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RepoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RepoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RepoDialog)

    def retranslateUi(self, RepoDialog):
        RepoDialog.setWindowTitle(i18n("Add New Repository"))
        self.textLabel1.setToolTip(i18n("Name of the repository, e.g <b>pardus-devel</b>"))
        self.textLabel1.setText(i18n("Repository Name"))
        self.label.setText(i18n("Repository Address"))
        self.browseButton.setToolTip(i18n("Add Local Repository\n"
"You can use your removable devices."))
        self.browseButton.setText(i18n("..."))

