def dev2grub(dev):
    type = dev[0:2]
    disc = ord(dev[2:3]) - 97
    part = int(dev[3:]) - 1
    return "(%s%s,%s)" % (type, disc, part)

def grub2dev(gr):
    gr = gr[1:-1]
    type = gr[0:2]
    disc, part = gr[2:].split(",")
    disc = chr(int(disc) + 97)
    part = int(part) + 1
    return "%s%s%s" % (type, disc, part)

def parseGrubConfig(filename):
    lines = [i.strip() for i in file(filename) if not i.startswith("#") and i.strip()]

    options = {}
    entries = []
    entry = {}

    for i in lines:
        if i.find(" ") == -1:
            label = i
            data = ""
        else:
            label = i[0:i.find(" ")].rstrip(" =")
            data = i[i.find(" ") + 1:].lstrip(" =")

        if label == "title":
            if entry:
                entries.append(entry)
                entry = {}
            entry["title"] = data
        elif not entry:
            options[label] = options.get(label, []) + [data]
        elif entry:
            entry[label] = entry.get(label, []) + [data]

    entries.append(entry)

    return options, entries


def grubToString(opts, entries):
    s = ""

    for label, data in opts.iteritems():
        for i in data:
            s += "%s %s\n" % (label, i)

    s += "\n"

    for entry in entries:
        s += "title %s\n" % entry["title"]
        if "map" in entry:
            for i in entry["map"]:
                s += "map %s\n" % i
        for label, data in entry.iteritems():
            if label not in ["title", "map"]:
                for i in data:
                    s += "%s %s\n" % (label,i)
        s += "\n"
    return s
