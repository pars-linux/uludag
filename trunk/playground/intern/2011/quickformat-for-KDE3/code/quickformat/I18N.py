import gettext

__trans = gettext.translation("quickformat", fallback=True)

def i18n(*text):
    "Needs for internationalization"
    if len(text) == 1:
        return __trans.ugettext(text[0])
    ttt = unicode(__trans.ugettext(text[0]))
    for i in range(1,len(text)):
        ttt = ttt.replace('%%%d' % i, unicode(text[i]))
    return ttt

