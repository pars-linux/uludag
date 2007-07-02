import user_ui

import partition

class UserWidget(user_ui.UserWid):
    def __init__(self, parent):
        self.parent = parent
        user_ui.UserWid.__init__(self, parent)
        self.users = partition.allUsers()
        for user in self.users:
            part, parttype, username, userdir = user
            self.usersBox.insertItem(username + " - " + parttype + " (" + part + ")")
        if len(self.users) > 0:
            self.parent.setNextEnabled(self, True)
        else:
            self.parent.setNextEnabled(self, False)