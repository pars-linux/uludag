from string import ascii_letters, digits
from PyQt4 import QtGui


class Partitioning:
    def __init__(self, key, name):
        self.key = key
        self.name = name

    
class User:
    def __init__(self, username, realname, password, groups):
        self.username = username
        self.realname = realname
        self.password = password
        self.groups = groups
        self.autologin=False
    
    def __unicode__(self):
        return self.username
    
    def toString(self):
        return self.username

    def passwordIsValid(self):
        return True
    
    def usernameIsValid(self):
        """ Check if the given username is valid not """
        valid = ascii_letters + '_' + digits
        name = self.username
        
        if len(name)==0:
            return False
        
        if name[0] not in ascii_letters:
            return False
        
        for letter in name:
            if letter not in valid:
                return False
        
        return True

    def realnameIsValid(self):
        """ Check if the given Real Name is valid or not """
        not_allowed_chars = '\n' + ':'
        return '' == filter(lambda r: [x for x in not_allowed_chars if x == r], self.realname)
