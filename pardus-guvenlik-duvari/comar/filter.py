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


def atoi(s):
    """String to integer"""
    t = ""
    for c in s.lstrip():
        if c in "0123456789":
            t += c
        else:
            break
    try:
        ret = int(t)
    except:
        ret = 0
    return ret


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
        if 1 < atoi(rules["sport"]) < 65535:
            args.append("--source-port %s" % rules["sport"])
        else:
            fail("Invalid source port")

    if "dport" in rules:
        if 1 < atoi(rules["dport"]) < 65535:
            args.append("--destination-port %s" % rules["dport"])
        else:
            fail("Invalid destination port")

    jump = rules.get("jump", "REJECT")
    if jump not in ["REJECT", "ALLOW", "DROP"]:
        fail("Invalid action")

    cmds = []
    cmds.append('/sbin/iptables -t filter %s -j LOG --log-tcp-options --log-level 3' % ' '.join(args))

    if jump == 'REJECT':
        cmds.append('/sbin/iptables -t filter %s -j REJECT --reject-with tcp-reset' % ' '.join(args))
    else:
        cmds.append('/sbin/iptables -t filter %s -j %s' % (' '.join(args), jump))

    return cmds


def setRule(**rule):
    """Append new firewall rule"""
    cmds = buildRule('A', rule)
    ret_log, ret_jmp = map(run, cmds)
    if ret_log != 0 or ret_jmp != 0:
        fail("Invalid command")

def unsetRule(no):
    """Remove given firewall rule"""
    rule = get_instance("no", no)
    cmds = buildRule('D', rule)
    ret_log, ret_jmp = map(run, cmds)
    if ret_log != 0 or ret_jmp != 0:
        fail("Invalid command")

def getRule(no):
    """Get details of given rule number"""
    return get_instance("no", no)

def listRules():
    """List rule numbers"""
    return instances("no")
