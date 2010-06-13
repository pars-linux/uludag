sizeUnits = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
timeUnitsSingle = ['second', 'minute', 'hour', 'day']
timeUnitsPlural = ['seconds', 'minutes', 'hours', 'days']

def humanReadableSize(bytes):
    bytes = long(bytes)
    x = 0
    part = 0
    while bytes/1024>0:
	x += 1
	part = int((bytes % 1024)/1024.0*100)
	bytes >>= 10
    return '%d.%d %s' % (bytes, part, sizeUnits[x])

def humanReadableTime(seconds):
    if seconds>=24*60*60:
	v1=seconds/(24*60*60)
	v2=(seconds%(24*60*60))/(60*60)
	u1=3
	u2=2
    elif seconds>=60*60:
	v1=seconds/(60*60)
	v2=(seconds%(60*60))/(60)
	u1=2
	u2=1
    elif seconds>=60:
	v1=seconds/(60)
	v2=(seconds%(60))
	u1=1
	u2=0
    else:
	v1=0
	v2=seconds%(60)
	u1=1
	u2=0

	if(v1==1): u1 = timeUnitsSingle[u1]
	else: u1 = timeUnitsPlural[u1]
	if(v2==1): u2 = timeUnitsSingle[u2]
	else: u2 = timeUnitsPlural[u2]


    return '%d %s %d %s' % (v1,u1,v2,u2)
