import subprocess

def run(*cmd):
    '''Run a command without running a shell'''
    if len(cmd) == 1:
        if isinstance(cmd[0], basestring):
            return subprocess.call(cmd[0].split())
        else:
            return subprocess.call(cmd[0])
    else:
        return subprocess.call(cmd)


def addRule(id, chain='INPUT', protocol='', src='', dst='', sport='', dport='', jump='ACCEPT'):
    args = []
    if chain: args.append('-A %s' % chain)
    if protocol: args.append('-p %s' % protocol)
    if src: args.append('--source %s' % src)
    if dst: args.append('--destination %s' % dst)
    if sport: args.append('--source-port %s' % sport)
    if dport: args.append('--destination-port %s' % dport)
    
    if jump in ['DROP', 'REJECT']:
        run('/sbin/iptables %s -j LOG --log-tcp-options --log-level 3' % ' '.join(args))

    if jump in ['ACCEPT', 'DROP']:
        run('/sbin/iptables %s -j %s' % (' '.join(args), dump))
    elif jump == 'REJECT':
        run('/sbin/iptables %s -j REJECT --reject-with tcp-reset' % ' '.join(args))


def cleanRules():
    run('/sbin/iptables -F')
