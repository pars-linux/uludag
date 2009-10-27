named_rules = {
    'inMail': '-p tcp -m multiport --dports 25,110',
    'inWeb': '-p tcp -m multiport --dports 80,443',
    'inRemote': '-p tcp -m multiport --dports 22',
    'inWFS': '-p tcp -m multiport --dports 445',
    'inIRC': '-p tcp -m multiport --dports 6667-6669',
    'inFTP': '-p tcp -m multiport --dports 21',
}
