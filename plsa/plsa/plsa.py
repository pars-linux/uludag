from pisi.pxml.xmlfile import XmlFile
import pisi.pxml.autoxml as autoxml

__metaclass__ = autoxml.autoxml

class Package:
    t_Name = [autoxml.String, autoxml.mandatory]
    t_Reporsitory = [autoxml.String, autoxml.mandatory]
    t_Release = [autoxml.String, autoxml.mandatory]

class Reference:
    t_Name = [autoxml.String, autoxml.mandatory]
    t_Link = [autoxml.String, autoxml.mandatory]

class Advisory:
    a_Id = [autoxml.String, autoxml.mandatory]
    t_Title = [autoxml.LocalText, autoxml.mandatory]
    t_ReleaseDate = [autoxml.String, autoxml.mandatory]
    t_Description = [autoxml.LocalText, autoxml.mandatory]
    t_Packages = [[Package], autoxml.mandatory]
    t_References = [[Reference], autoxml.optional]

class PLSAFile(XmlFile):
    __metaclass__ = autoxml.autoxml

    tag = "PLS"

    t_Advisories = [[Advisory], autoxml.optional, "Advisory"]
