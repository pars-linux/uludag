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
        '25, 110',
    ),
    'inWeb': (
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 80,443 -j ACCEPT'],
        i18n('Web services'),
        '80, 443',
    ),
    'inRemote': (
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 22 -j ACCEPT'],
        i18n('Remote login service'),
        '22',
    ),
    'inWFS': (
        [
            '-A PARDUS-IN-USER -p udp -m multiport --dports 137:139,445 -j ACCEPT',
            '-A PARDUS-IN-USER -p tcp -m multiport --dports 137:139,445 -j ACCEPT',
            '-A PARDUS-IN-USER -p udp -m multiport --sports 137:139,445 -j ACCEPT',
        ],
        i18n('Windows file sharing service'),
        '137, 138, 139, 445',
    ),
    'inIRC': (
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 6667:6669 -j ACCEPT'],
        i18n('Internet relay chat service'),
        '6667, 6668, 6669',
    ),
    'inFTP': (
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 21 -j ACCEPT'],
        i18n('File transfer service'),
        '21',
    ),
    'inVNC': (
        ['-A PARDUS-IN-USER -p tcp -m multiport --dports 5800:5804,5900:5904 -j ACCEPT'],
        i18n('Desktop Sharing'),
        '5800:5804,5900:5904',
    ),
}
