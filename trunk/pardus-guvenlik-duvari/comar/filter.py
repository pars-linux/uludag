import subprocess

def run(*cmd):
    """Run a command without running a shell"""
    if len(cmd) == 1:
        if isinstance(cmd[0], basestring):
            return subprocess.call(cmd[0].split())
        else:
            return subprocess.call(cmd[0])
    else:
        return subprocess.call(cmd)


def buildRule(action='A', rules={}):
    """Generate IPTables command from given rule"""
    args = []

    if action == "A":
        args.append("-A %s" % rules.get("chain", "INPUT"))
    else:
        args.append("-D %s" % rules.get("chain", "INPUT"))
        
    args.append("--protocol %s" % rules.get("protocol", "tcp"))

    if "src" in rules:
        args.append("--source %s" % rules["src"])
        
    if "dst" in rules:
        args.append("--destination %s" % rules["dst"])

    # FIXME: not all protocols allow these parameters
    if "sport" in rules:
        args.append("--source-port %s" % rules["sport"])

    if "dport" in rules:
        args.append("--destination-port %s" % rules["dport"])

    cmds = []
    cmds.append('/sbin/iptables -t filter %s -j LOG --log-tcp-options --log-level 3' % ' '.join(args))

    if rules.get("jump", "REJECT") == 'REJECT':
        cmds.append('/sbin/iptables -t filter %s -j REJECT --reject-with tcp-reset' % ' '.join(args))
    else:
        cmds.append('/sbin/iptables -t filter tcp %s -j %s' % (' '.join(args), rules.get("jump", "REJECT")))

    return cmds


def setRule(**rules):
    """Append new firewall rule"""
    for cmd in buildRule('A', rules):
        ret = run(cmd)


def unsetRule(no):
    """Remove given firewall rule"""
    d = get_instance("no", no)
    
    for cmd in buildRule('D', d):
        run(cmd)

def getRule(no):
    """Get details of given rule number"""
    return get_instance("no", no)

def listRules():
    """List rule numbers"""
    return instances("no")
