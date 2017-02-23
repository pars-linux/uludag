#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Software magement module
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_software import Ui_widgetSoftware

# Helper modules
from lider.helpers import plugins
from lider.helpers import wrappers

# Repository dialog
from repository import DialogRepository


class WidgetModule(QtGui.QWidget, Ui_widgetSoftware, plugins.PluginWidget):
    """
        Software management UI.
    """
    def __init__(self, parent=None):
        """
            Constructor for main window.

            Arguments:
                parent: Parent object
        """
        plugins.PluginWidget.__init__(self)
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

        # Fine tune UI
        self.listRepositories.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # Popup for new items
        self.menu = wrappers.Menu(self)
        self.menu.newAction("Add Item", wrappers.Icon("add48"), self.__slot_repo_add)
        self.menu.newAction("Remove Item", wrappers.Icon("remove48"), self.__slot_repo_remove)

        # Days of week
        self.day_widgets = [
            self.checkMonday,
            self.checkTuesday,
            self.checkWednesday,
            self.checkThursday,
            self.checkFriday,
            self.checkSaturday,
            self.checkSunday
        ]

        # UI events
        self.connect(self.listRepositories, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__slot_list_menu)
        self.connect(self.listRepositories, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.__slot_list_click)

        self.connect(self.pushAddRepo, QtCore.SIGNAL("clicked()"), self.__slot_repo_add)
        self.connect(self.pushRemoveRepo, QtCore.SIGNAL("clicked()"), self.__slot_repo_remove)

    def set_item(self, item):
        """
            Sets directory item that is being worked on.
            Not required for global widgets.
        """
        pass

    # def showEvent(self, event):
    def showEvent(self):
        """
            Things to do before widget is shown.
        """
        #jid = "%s@%s" % (self.item.name, self.talk.domain)
        #self.talk.send_command(jid, "software.repositories")
        pass

    def get_type(self):
        """
            Widget type.

            Should return TYPE_GLOBAL or TYPE_SINGLE
        """
        return plugins.TYPE_SINGLE

    def get_classes(self):
        """
            Returns a list of policy class names.
        """
        return ["softwarePolicy"]

    def load_policy(self, policy):
        """
            Main window calls this method when policy is fetched from directory.
            Not required for global widgets.
        """
        # Repositories
        repositories = policy.get("softwareRepositories", [])
        self.listRepositories.clear()
        for repo in repositories:
            repo_name, repo_url = repo.split()
            self.__add_repo_item(repo_url, repo_name, False, True)
        # Auto update
        update_mode = policy.get("softwareUpdateMode", ["off"])[0]
        if update_mode in ["security", "full"]:
            self.groupUpdate.setChecked(True)
            if update_mode == "security":
                self.checkSecurity.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkSecurity.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.checkSecurity.setCheckState(QtCore.Qt.Unchecked)
            self.groupUpdate.setChecked(False)
        # Schedule
        for widget in self.day_widgets:
            widget.setCheckState(QtCore.Qt.Unchecked)

        schedule = policy.get("softwareUpdateSchedule", [""])[0]
        c_hour, c_min, c_days = self.__parse_cron(schedule)

        self.timeUpdate.setTime(QtCore.QTime(c_hour, c_min))

        for day in c_days:
            self.day_widgets[day].setCheckState(QtCore.Qt.Checked)

    def dump_policy(self):
        """
            Main window calls this method to get policy generated by UI.
            Not required for global widgets.
        """
        # Update schedule
        days = []
        for i, widget in enumerate(self.day_widgets):
            if widget.checkState() == QtCore.Qt.Checked:
                days.append(str(i))
        update_schedule = "%d %d * * %s" % (self.timeUpdate.time().minute(),
                                            self.timeUpdate.time().hour(),
                                            ",".join(days))
        # Update mode
        if self.groupUpdate.isChecked():
            if self.checkSecurity.checkState() == QtCore.Qt.Checked:
                update_mode = "security"
            else:
                update_mode = "full"
        else:
            update_mode = "off"
        # Repositories
        repositories = []
        for i in range(self.listRepositories.count()):
            item = self.listRepositories.item(i)
            repo_url = item.repo_url
            repo_name = item.repo_name
            repositories.append("%s %s" % (repo_name, repo_url))
        # New policy
        policy = {
            "softwareUpdateMode": [update_mode],
            "softwareUpdateSchedule": [update_schedule],
            "softwareRepositories": repositories,
        }
        return policy

    def talk_message(self, sender, command, arguments=None):
        """
            Main window calls this method when an XMPP message is received.
        """
        print command, arguments
        if command == "software.repositories":
            for repo_name, repo_url in arguments:
                self.__add_repo_item(repo_url, repo_name, False, True)

    def talk_status(self, sender, status):
        """
            Main window calls this method when an XMPP status is changed.
        """
        pass

    def __slot_list_menu(self, pos):
        """
            Triggered when user right clicks a repo item.
        """
        self.menu.exec_(self.listRepositories.mapToGlobal(pos))

    def __slot_list_click(self, item):
        """
            Triggered when user double clicks a repo item.
        """
        if item:
            dialog = DialogRepository(self)
            dialog.set_url(item.repo_url)
            dialog.set_name(item.repo_name)
            if dialog.exec_():
                item.repo_url = dialog.get_url()
                item.repo_name = dialog.get_name()
                item.setText("%s - %s" % (item.repo_name, item.repo_url))

    def __slot_repo_add(self):
        """
            Triggered when user wants to add a new repository.
        """
        dialog = DialogRepository(self)
        if dialog.exec_():
            repo_url = dialog.get_url()
            repo_name = dialog.get_name()
            self.__add_repo_item(repo_url, repo_name, False, True)

    def __slot_repo_remove(self):
        """
            Triggered when user wants to remove a repository.
        """
        item = self.listRepositories.currentItem()
        if item:
            self.listRepositories.takeItem(self.listRepositories.currentRow())

    def __add_repo_item(self, url, name, secure=False, checked=False):
        """
            Adds a new item to repository list.

            Arguments:
                url: Repository URL
                name: Repository name
                secure: if repository is signed
                checked: if repository is enabled
        """
        item = QtGui.QListWidgetItem(self.listRepositories)
        if secure:
            item.setIcon(wrappers.Icon("locked48"))
        else:
            item.setIcon(wrappers.Icon("unlocked48"))
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.UnChecked)
        item.setText("%s - %s" % (name, url))
        item.repo_url = url
        item.repo_name = name

    def __parse_cron(self, schedule):
        """
            Parses a cron date string.

            Arguments:
                schedule: CRON date
            Returns:
                (hour, minute, [days])
        """
        try:
            c_min, c_hour, c_day, c_month, c_dayofweek = schedule.split()
            c_min = int(c_min)
            c_hour = int(c_hour)
        except ValueError:
            return (0, 0, [])
        if c_dayofweek == "*":
            return (c_hour, c_min, [x for x in range(7)])
        else:
            days = []
            for day in c_dayofweek.split(","):
                if "-" in day:
                    try:
                        day = int(day)
                    except ValueError:
                        return (0, 0, [])
                    days.append(day)
                else:
                    try:
                        day = int(day)
                    except ValueError:
                        return (0, 0, [])
                    days.append(day)
            return (c_hour, c_min, days)
