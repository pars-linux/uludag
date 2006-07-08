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
            elif label == "root":
                entry["root"] = data[data.find("(") + 1:-1]
            elif label == "rootnoverify":
                entry["root"] = data[data.find("(") + 1:-1]
                entry["foreign"] = entry.get("foreign", []) + ["noverify"]
            elif label == "chainloader":
                entry["foreign"] = entry.get("foreign", []) + ["chainloader"]
            elif label == "makeactive":
                entry["foreign"] = entry.get("foreign", []) + ["makeactive"]
            elif label == "kernel":
                kernelopts = data[data.find("(") + 1:].split(" ")
                entry["kernel"] = kernelopts[0][kernelopts[0].find(")") + 1:] 
                entry["opts"] = kernelopts[1:]
            elif not entry and i.strip():
                options[i[0:i.find(" ")]] = i[i.find(" ") + 1:-1].lstrip(" =")
        elif i == "\n" and entry:
            entries.append(entry)
            entry = {}
    
    entries.append(entry)

    return options, entries
