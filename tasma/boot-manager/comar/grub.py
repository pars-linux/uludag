def dev2grub(dev):
    type = dev[0:2]
    disc = ord(dev[2:3]) - 97
    part = int(dev[3:]) - 1
    return "%s%s,%s" % (type, disc, part)

def grub2dev(gr):
    type = gr[0:2]
    disc, part = gr[2:].split(",")
    disc = chr(int(disc) + 97)
    part = int(part) + 1
    return "%s%s%s" % (type, disc, part)

def parseGrubConfig(filename):
    options = {}
    entries = []
    entry = {}
    for i in file(filename):
        if i != "\n":
            label = i[0:i.find(" ")].rstrip(" =")
            data = i[i.find(" ") + 1:-1].lstrip(" =")
            if label == "title":
                entry["title"] = data
            elif label in ["root", "rootnoverify"]:
                entry[label] = data[data.find("(") + 1:-1]
            elif label in ["chainloader", "makeactive"]:
                entry[label] = True
            elif label in ["map", "hide", "unhide"]:
                entry[label] = entry.get(label, []) + [(data)]
            elif label == "kernel":
                kernelopts = data[data.find("(") + 1:].split(" ")
                entry["kernel"] = kernelopts[0][kernelopts[0].find(")") + 1:] 
                entry["opts"] = kernelopts[1:]
            elif label == "initrd":
                entry["initrd"] = data[data.find(")") + 1:]
            elif not entry and i.strip():
                options[i[0:i.find(" ")]] = i[i.find(" ") + 1:-1].lstrip(" =")
        elif i == "\n" and entry:
            entries.append(entry)
            entry = {}
    
    entries.append(entry)

    return options, entries


def grubToString(opts, entries):
    s = ""

    for label, data in opts.iteritems():
        s += "%s %s\n" % (label, data)

    s += "\n"

    for entry in entries:
        if "rootnoverify" in entry:
            s += "title %s\n" % entry["title"]
            for op in ["map", "hide", "unhide"]:
                if op in entry:
                    for i in entry[op]:
                        s += "%s %s\n" % (op, i)
            s += "rootnoverify (%s)\n" % entry["rootnoverify"]
            if "chainloader" in entry:
                s += "chainloader +1\n"
            if "makeactive" in entry:
                s += "makeactive\n"
        else:
            s += "title %s\n" % entry["title"]
            s += "root (%s)\n" % entry["root"]
            s += "kernel (%s)%s %s\n" % (entry["root"], entry["kernel"], " ".join(entry["opts"]))
            if "initrd" in entry:
                s += "initrd (%s)%s\n" % (entry["root"], entry["initrd"])
        s += "\n"
    return s
