i18n = lambda x: x

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
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 25,110 -j ACCEPT'],
        i18n('Mail services'),
    ),
    'inWeb': (
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 80,443 -j ACCEPT'],
        i18n('Web services'),
    ),
    'inRemote': (
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 22 -j ACCEPT'],
        i18n('Remote login service'),
    ),
    'inWFS': (
        [
            '-A PARDUS-IN-USER -p udp -m multiport --dports 137:139,445 -j ACCEPT',
            '-A PARDUS-IN-USER -p tcp -m multiport --dports 137:139,445 -j ACCEPT',
            '-A PARDUS-IN-USER -p udp -m multiport --sports 137:139,445 -j ACCEPT',
        ],
        i18n('Windows file sharing service'),
    ),
    'inIRC': (
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 6667:6669 -j ACCEPT'],
        i18n('Internet relay chat service'),
    ),
    'inFTP': (
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 21 -j ACCEPT'],
        i18n('File transfer service'),
    ),
}
