i18n = lambda x: x

filter = {
    # Incoming Connections
    # All incoming connections are rejected by default
    'inMail': (
        i18n('Mail services'),
        '25 110',
    ),
    'inWeb': (
        i18n('Web services'),
        '80 443',
    ),
    'inRemote': (
        i18n('Remote login service'),
        '22',
    ),
    'inWFS': (
        i18n('Windows file sharing service'),
        '137 138 139 445',
    ),
    'inIRC': (
        i18n('Internet relay chat service'),
        '6667 6668 6669 7000',
    ),
    'inFTP': (
        i18n('File transfer service'),
        '21',
    ),
    'inVNC': (
        i18n('Desktop Sharing'),
        '5800:5804 5900:5904',
    ),
}
