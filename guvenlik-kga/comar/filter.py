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


def portsOk(p):
    """Check multiport format"""
    if p.count(",") + p.count(":") > 15:
        return 0
    l = p.split(",")
    for i in l:
        k = i.split(":")
        if len(k) > 2:
            return 0
        for j in k:
            if 0 > atoi(j) < 65535:
                return 0
    return 1


def buildRule(action="A", rules={}, bin="/sbin/iptables"):
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
        if not portsOk(rules["sport"]):
            fail("Invalid port")
        args.append("--source-ports %s" % rules["sport"])
    if "dport" in rules:
        if not portsOk(rules["dport"]):
            fail("Invalid port")
        args.append("--destination-ports %s" % rules["dport"])

    if "extra" in rules:
        args.append(rules["extra"])

    jump = rules.get("jump", "REJECT")
    if jump not in ["REJECT", "ACCEPT", "DROP"]:
        fail("Invalid action")

    cmds = []

    if rules.get("log", 1) == 1:
        cmds.append("%s -t filter %s -j LOG --log-tcp-options --log-level 3" % (bin, " ".join(args)))

    if jump == "REJECT" and rules.get("protocol", "tcp") == "tcp":
        cmds.append("%s -t filter %s -j REJECT --reject-with tcp-reset" % (bin, " ".join(args)))
    else:
        cmds.append("%s -t filter %s -j %s" % (bin, " ".join(args), jump))

    return cmds


def setRule(**rule):
    """Append new firewall rule"""
    if getState() == "off":
        return
    if "no" not in rule or rule["no"] in instances("no"):
        fail("Invalid rule no")
    cmds = buildRule("A", rule)
    for c in cmds:
        ret = run(c)
        if ret != 0:
            fail("Invalid command")
    return rule["no"]


def unsetRule(no):
    """Remove given firewall rule"""
    if getState() == "off":
        return
    rule = get_instance("no", no)
    cmds = buildRule("D", rule)
    for c in cmds:
        ret = run(c)
        if ret != 0:
            fail("Invalid command")


def getRules():
    """Get all rules"""
    inst = instances("no")
    inst.sort(key=atoi)
    rules = []
    for i in inst:
        rules.append(get_instance("no", i))
    return rules


def getState():
    """Get FW state"""
    state = get_profile("Net.Filter.setState")
    if state:
        return state["state"]
    return "off"


def setState(state):
    """Set FW state"""
    if state not in ["on", "off"]:
        fail("Invalid state")
    if getState() == state:
        return
    
    # What to do
    action = ["D", "A"][state == "on"]
    for rule in getRules():
        cmds = buildRule(action, rule)
        for c in cmds:
            ret = run(c)
