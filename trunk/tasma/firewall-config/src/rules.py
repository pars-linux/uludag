from kdecore import i18n

filter = {
    'inMail': (
        '-A PARDUS-USER -p tcp -m multiport --dports 25,110 -j ACCEPT',
        i18n('Mail services'),
    ),
    'inWeb': (
        '-A PARDUS-USER -p tcp -m multiport --dports 80,443 -j ACCEPT',
        i18n('Web services'),
    ),
    'inRemote': (
        '-A PARDUS-USER -p tcp -m multiport --dports 22 -j ACCEPT',
        i18n('Remote login service'),
    ),
    'inWFS': (
        '-A PARDUS-USER -p tcp -m multiport --dports 445 -j ACCEPT',
        i18n('Windows file sharin service'),
    ),
    'inIRC': (
        '-A PARDUS-USER -p tcp -m multiport --dports 6667-6669 -j ACCEPT',
        i18n('Internet relay chat service'),
    ),
    'inFTP': (
        '-A PARDUS-USER -p tcp -m multiport --dports 21 -j ACCEPT',
        i18n('File transfer service'),
    )
}
