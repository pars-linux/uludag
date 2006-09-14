def get_localized_node(parent, name, lang="en"):
    """Returns tag data with selected xml:lang attribute"""
    for x in parent.tags():
        if x.name() == name and "xml:lang" in x.attributes() and x.getAttribute("xml:lang") == lang:
            if x.firstChild() and x.firstChild().type() == 3:
                return unicode(x.firstChild().data())
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

def build_advisory(tags, __tr):
    title = __tr("Pardus Linux Security Advisory")
    email = __tr("security@pardus.org.tr")
    web = __tr("http://security.pardus.org.tr")

    headers = [(__tr("ID"), tags["id"]),
               (__tr("Date"), tags["date"]),
               (__tr("Title"), tags["title"]),
               (__tr("Severity"), tags["severity"])]

    tpl = []
    tpl.append("-" * 72)
    tpl.append(justify("%s  %s" % (title, email), "  ", 72))
    tpl.append("-" * 72)
    tpl.extend(calign(headers))
    tpl.append("-" * 72)
    tpl.append("")

    tpl.append(__tr("Summary"))
    tpl.append("=" * len(__tr("Summary")))
    tpl.append(wwrap(tags["summary"]))
    tpl.append("")

    tpl.append(__tr("Description"))
    tpl.append("=" * len(__tr("Description")))
    tpl.append(wwrap(tags["description"]))
    tpl.append("")

    if tags["packages_up"]:
        tpl.append(__tr("These packages should be upgraded to specified releases:"))
        for p, r in tags["packages_up"]:
          tpl.append("  * %s-%s" % (p, r))
        tpl.append("")

    if tags["packages_rm"]:
        tpl.append(__tr("These packages should be removed from system:"))
        for p in tags["packages_rm"]:
          tpl.append("  * %s" % p)
        tpl.append("")

    if tags["references"]:
        tpl.append(__tr("References"))
        tpl.append("=" * len(__tr("References")))
        for ref, link in tags["references"]:
          tpl.append("  * " + wwrap("%s <%s>" % (ref, link), lpad=4, just=0).strip())
        tpl.append("")

    tpl.append("-" * 72)

    return "\n".join(tpl)
