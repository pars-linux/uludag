import os
import os.path

def list_translations(domain):
    localedir = "/usr/share/locale"
    langs = ["en"]
    for i in os.listdir(localedir):
        if os.access(os.path.join(localedir, i, "LC_MESSAGES", "%s.mo" % domain), os.F_OK):
            langs.append(i)
    return langs

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
