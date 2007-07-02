import registry
import os.path
import ConfigParser

from bookmark import *

class UserMigration:
    def __init__(self, partition, parttype, userdir):
        self.partition = partition
        self.parttype = parttype
        self.userdir = userdir
        self.sources = {}
        self.destinations = {}
        self.options = {"Bookmarks":"true", "IEBookmarks":"true", "FFBookmarks":"true"}
        
        # Collect Information:
        if parttype in ["Windows Vista", "Windows XP"]:
            self.collectWindowsInformation()
        self.collectLocalInformation()
    
    def collectWindowsInformation(self):
        # Find user directories using registry:
        hive = registry.Hive(os.path.join(self.userdir, "NTUSER.DAT"))
        key = hive.getKey("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders")
        valuedict = key.valueDict()
        for field, value in valuedict.iteritems():
            if field in ["AppData", "Cache", "Cookies", "Desktop", "Favorites", "Fonts",
                         "History", "My Music", "My Pictures", "My Video", "Personal"]:
                if value.find("C:\\") != -1:
                    value = value.replace("C:\\", "")
                    value = value.replace("\\", "/")
                    value = os.path.join(self.partition, value)
                    if os.path.isdir(value):
                        self.sources[field + " Path"] = value
        
        # Search for programs:
        if self.sources.has_key("AppData Path"):
            # Firefox:
            possiblepath = os.path.join(self.sources["AppData Path"], "Mozilla/Firefox")
            profilepath = self.getMozillaProfile(possiblepath)
            if profilepath != "":
                self.sources["Firefox Profile Path"] = profilepath
            # Thunderbird:
            possiblepath = os.path.join(self.sources["AppData Path"], "Thunderbird")
            profilepath = self.getMozillaProfile(possiblepath)
            if profilepath != "":
                self.sources["Thunderbird Profile Path"] = profilepath
    
    def collectLocalInformation(self):
        # Firefox
        profilepath = self.getMozillaProfile(os.path.expanduser("~/.mozilla/firefox/"))
        if profilepath != "":
            self.destinations["Firefox Profile Path"] = profilepath
            
    def getMozillaProfile(self, ffpath):
        try:
            parser = ConfigParser.ConfigParser()
            inifile = os.path.join(ffpath,"profiles.ini")
            if not os.path.isfile(inifile):
                return ""
            parser.readfp(open(inifile))
            # Find Default Profile:
            if parser.has_section("Profile1"):
                sections = parser.sections()
                for section in sections:
                    if parser.has_option(section, "Default") and parser.get(section, "Default"):
                        profilename = section
            else:
                if parser.has_section("Profile0"):
                    profilename = "Profile0"
            # Get Profile Path:
            if parser.has_option(profilename, "Path"):
                if parser.has_option(profilename, "IsRelative") and parser.get(profilename, "IsRelative"):
                    possibledir = os.path.join(ffpath, parser.get(profilename, "Path"))
                    if os.path.isdir(possibledir):
                        return possibledir
                else:
                    return parser.get(profilename, "Path")
        except:
            print "WARNING: Mozilla profile cannot be detected!"
            return ""
        
    def migrate(self):
        # Copy Bookmarks:
        if self.options.has_key("Bookmarks") and self.options["Bookmarks"]:
            bm = Bookmark()
            # Load IE Bookmarks:
            if self.options.has_key("IEBookmarks") and self.options["IEBookmarks"] and self.sources.has_key("Favorites Path"):
                bm.getIEBookmarks(self.sources["Favorites Path"])
                print "Internet Explorer bookmarks loaded."
            # Load FF Bookmarks:
            if self.options.has_key("FFBookmarks") and self.options["FFBookmarks"] and self.sources.has_key("Firefox Profile Path"):
                possiblefile = os.path.join(self.sources["Firefox Profile Path"], "bookmarks.html")
                if os.path.isfile(possiblefile):
                    bm.getFFBookmarks(possiblefile)
                    print "Firefox bookmarks loaded."
            # Save FF Bookmarks:
            if self.destinations.has_key("Firefox Profile Path"):
                lockfile = os.path.join(self.destinations["Firefox Profile Path"], "lock")
                if not os.path.lexists(lockfile):
                    possiblefile = os.path.join(self.destinations["Firefox Profile Path"], "bookmarks.html")
                    if os.path.isfile(possiblefile):
                        bm.setFFBookmarks(possiblefile)
                        print "Firefox bookmarks saved."
                    else:
                        print "WARNING: Firefox bookmarks file cannot be found."
                else:
                    print "WARNING: Firefox is in use. Bookmarks cannot be saved."
