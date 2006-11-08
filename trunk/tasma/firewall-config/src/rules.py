from qt import *
from kdecore import *
from kdeui import *

profile = {
    'profile': 'pardus',
    'save_filter': 'PARDUS-IN-USER PARDUS-OUT-USER',
    'save_mangle': '',
    'save_nat': '',
    'save_raw': ''
}

filter = {
    # Incoming Connections
    # All incoming connections are rejected by default
    'inMail': (
        '-A PARDUS-IN-USER -p tcp -m multiport --dports 25,110 -j ACCEPT',
        i18n('Mail services'),
    ),
    'inWeb': (
        '-A PARDUS-IN-USER -p tcp -m multiport --dports 80,443 -j ACCEPT',
        i18n('Web services'),
    ),
    'inRemote': (
        '-A PARDUS-IN-USER -p tcp -m multiport --dports 22 -j ACCEPT',
        i18n('Remote login service'),
    ),
    'inWFS': (
        '-A PARDUS-IN-USER -p tcp -m multiport --dports 445 -j ACCEPT',
        i18n('Windows file sharing service'),
    ),
    'inIRC': (
        '-A PARDUS-IN-USER -p tcp -m multiport --dports 6667-6669 -j ACCEPT',
        i18n('Internet relay chat service'),
    ),
    'inFTP': (
        '-A PARDUS-IN-USER -p tcp -m multiport --dports 21 -j ACCEPT',
        i18n('File transfer service'),
    ),

    # Outgoing Connections
    # All outgoing connections are accepted by default
    'outMail': (
        '-A PARDUS-OUT-USER -p tcp -m multiport --dports 25,110 -j REJECT --reject-with icmp-port-unreachable',
        i18n('Mail services'),
    ),
}
