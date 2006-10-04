def get_node_translations(parent, name):
    """Returns available translations of node."""
    langs = []
    for x in parent.tags():
        if x.name() == name and "xml:lang" in x.attributes():
            langs.append(x.getAttribute("xml:lang"))
    return langs

def get_localized_node(parent, name, lang="en"):
    """Returns tag with selected xml:lang attribute"""
    for x in parent.tags():
        if x.name() == name and "xml:lang" in x.attributes() and x.getAttribute("xml:lang") == lang:
            return x

def get_localized_data(parent, name, lang="en"):
    """Returns tag with selected xml:lang attribute"""
    for x in parent.tags():
        if x.name() == name and "xml:lang" in x.attributes() and x.getAttribute("xml:lang") == lang:
            if x.firstChild():
                return unicode(x.firstChild().data())
            else:
                return ""
