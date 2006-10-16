from dcopext import DCOPClient, DCOPObj
from kdecore import KURL
from qt import QString


def qstr(text):
    return QString(unicode(text))


def openComposer(to='', cc='', bcc='', subject='', message=''):
    interfaces = [('kmail', 'default'),
                  ('kontact', 'KMailIface')]

    client = DCOPClient()
    client.attach()

    done = False
    for app, part in interfaces:
        obj = DCOPObj(app, client, part)
        try:
            obj.openComposer(to, cc, bcc, qstr(subject), qstr(message), False, KURL())
            done = True
            break
        except TypeError:
            pass

    return done
