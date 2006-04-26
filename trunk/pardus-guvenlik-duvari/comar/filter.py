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
    """Generate IPTables command from given rule description"""
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
    if "sport" in rules or "dport" in rules:
        args.append("--match multiport")
    if "sport" in rules:
        args.append("--source-ports %s" % rules["sport"])
    if "dport" in rules:
        args.append("--destination-ports %s" % rules["dport"])

    if "extra" in rules:
        args.append(rules["extra"])

    jump = rules.get("jump", "REJECT")
    if jump not in ["REJECT", "ACCEPT", "DROP"]:
        fail("Invalid action")

    cmds = []

    if rules.get("log", 1) == 1:
        cmds.append('/sbin/iptables -t filter %s -j LOG --log-tcp-options --log-level 3' % ' '.join(args))

    if jump == 'REJECT':
        cmds.append('/sbin/iptables -t filter %s -j REJECT --reject-with tcp-reset' % ' '.join(args))
    else:
        cmds.append('/sbin/iptables -t filter %s -j %s' % (' '.join(args), jump))

    return cmds

def getState():
    """Get FW state"""
    if "filter" in instances("name"):
        return get_instance("name", "filter")["state"]
    else:
        return "off"

def setState(name, state):
    """Set FW state"""
    if state not in ["on", "off"] or name != "filter":
        fail("Invalid state")
    if get_instance("name", "filter").get("state", "off") == state:
        return
    action = ["D", "A"][state == "on"]
    inst = map(atoi, instances("no"))
    inst.sort()
    inst = map(str, inst)
    for no in inst:
        rule = get_instance("no", no)
        cmds = buildRule(action, rule)
        for c in cmds:
            ret = run(c)

def setRule(**rule):
    """Append new firewall rule"""
    if getState() == "off":
        return
    cmds = buildRule('A', rule)
    for c in cmds:
        ret = run(c)
        if ret != 0:
            fail("Invalid command")

def unsetRule(no):
    """Remove given firewall rule"""
    if getState() == "off":
        return
    rule = get_instance("no", no)
    cmds = buildRule('D', rule)
    for c in cmds:
        ret = run(c)
        if ret != 0:
            fail("Invalid command")

def getRule(no):
    """Get details of given rule number"""
    return get_instance("no", no)

def listRules():
    """List rule numbers"""
    return instances("no")
