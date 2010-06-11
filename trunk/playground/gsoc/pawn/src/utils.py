sizeUnits = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
timeUnits = ['sec', 'min', 'hr', 'day(s)']

def humanReadableSize(bytes):
    x = 0
    part = 0
    while bytes >= 1024:
	x += 1
	part = bytes & 0x3ff
	bytes >>= 10
    return '%d.%d %s' % (bytes, part, sizeUnits[x])

def humanReadableTime(seconds):
    if seconds>=24*60*60:
	v1=seconds/(24*60*60)
	v2=(seconds%(24*60*60))/(60*60)
	u1=timeUnits[3]
	u2=timeUnits[2]
    elif seconds>=60*60:
	v1=seconds/(60*60)
	v2=(seconds%(60*60))/(60)
	u1=timeUnits[2]
	u2=timeUnits[1]
    elif seconds>=60:
	v1=seconds/(60)
	v2=(seconds%(60))
	u1=timeUnits[1]
	u2=timeUnits[0]
    else:
	v1=0
	v2=seconds%(60)
	u1=timeUnits[1]
	u2=timeUnits[0]

    return '%d %s %d %s' % (v1,u1,v2,u2)