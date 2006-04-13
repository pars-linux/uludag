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


def addTCPFilter(id, chain='INPUT', src='', dst='', sport='', dport='', jump='ACCEPT', log=1):
    args = []
    if chain:
        args.append('-A %s' % chain)
    if src:
        args.append('--source %s' % src)
    if dst:
        args.append('--destination %s' % dst)
    if sport:
        args.append('--source-port %s' % sport)
    if dport:
        args.append('--destination-port %s' % dport)
    
    if log:
        run('/sbin/iptables -t filter -p tcp %s -j LOG --log-tcp-options --log-level 3' % ' '.join(args))

    if jump == 'REJECT':
        run('/sbin/iptables -t filter -p tcp %s -j REJECT --reject-with tcp-reset' % ' '.join(args))
    else:
        run('/sbin/iptables -t filter -p tcp %s -j %s' % (' '.join(args), jump))


def cleanTCPFilters():
    run('/sbin/iptables -t filter -F')
