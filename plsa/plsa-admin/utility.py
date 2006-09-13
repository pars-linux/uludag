def localized_node(parent, name, lang="en"):
    """Returns tag data with selected xml:lang attribute"""
    node = [x for x in parent.tags() if x.name() == name and "xml:lang" in x.attributes() and x.getAttribute("xml:lang") == lang][0]
    if node.firstChild():
        return node.firstChild().data()
    else:
        return ""

def justify(text, delim=" ", width=72):
    words = text.split(delim)
    space = width - len(text)
    while space > 0:
        p = space % (len(words) - 1) + 1
        words[p * -1 + 1] += " "
        space -= 1
    return delim.join(words)

def wwrap(text, width=72, lpad=0, rpad=0, just=True):
    width -= rpad
    words = text.split()
    sel = [" " * lpad]
    for w in words:
        if len(sel[-1]) + len(w) <= width:
            sel[-1] += "%s " % w
        else:
            if just:
                sel[-1] = " " * lpad + justify(sel[-1][lpad:-1], " ", width - lpad)
            sel.append("%s%s " % (" " * lpad, w))
    return "\n".join(sel)

def calign(lst, width=72):
    t = []
    m = max(map(lambda x: len(x[0]), lst))
    for h, c in lst:
        h = h.rjust(m + 2)
        t.append("%s: %s" % (h, wwrap(c, width, len(h) + 2).strip()))
    return t

def gen_advisory(headers, tags):
    tpl = []
    tpl.append("-" * 72)
    tpl.append(justify("Pardus Linux Security Advisory  %s" % tags["date"], "  ", 72))
    tpl.append("-" * 72)
    tpl.extend(calign(headers))
    tpl.append("-" * 72)
    tpl.append("")

    tpl.append("Summary")
    tpl.append("=" * len("Summary"))
    tpl.append(wwrap(tags["summary"]))
    tpl.append("")

    tpl.append("Description")
    tpl.append("=" * len("Description"))
    tpl.append(wwrap(tags["description"]))
    tpl.append("")

    if len(tags.get("packages_up", [])):
        tpl.append("These packages should be upgraded to specified releases:")
        for p, r in tags["packages_up"]:
          tpl.append("  * %s r%s" % (p, r))
        tpl.append("")

    if len(tags.get("packages_rm", [])):
        tpl.append("These packages should be removed from system:")
        for p in tags["packages_rm"]:
          tpl.append("  * %s" % p)
        tpl.append("")

    if len(tags.get("references", [])):
        tpl.append("References")
        tpl.append("=" * len("References"))
        for ref, link in tags["references"]:
          tpl.append("  * " + wwrap("%s <%s>" % (ref, link), lpad=4, just=0).strip())
        tpl.append("")

    tpl.append("-" * 72)

    return "\r\n".join(tpl)
