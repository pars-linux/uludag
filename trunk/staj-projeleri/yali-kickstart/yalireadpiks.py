import piksemel
import sys

class yaliKickstartData:
    language=None
    keyData=None
    rootPassword=None
    hostname=None
    users=[]
    partitioning=[]

class yaliUser:
    autologin=None
    username=None
    realname=None
    password=None
    groups=[]
    
class yaliPartition:
    partitionType=None
    format=None
    ratio=None
    disk=None
    fsType=None
    mountPoint=None
    
    
doc=piksemel.parse(argv[1])


data=yaliKickstartData()
data.language=doc.getTagData("language")
data.keyData=doc.getTagData("keymap")
data.rootPassword=doc.getTagData("root_password")
data.hostname=doc.getTagData("hostname")

usrsTag=doc.getTag("users")

for p in usrsTag.tags(): #for each "user" tag
    info=yaliUser()
    info.autologin=p.getAttribute("autologin")
    info.username=p.getTagData("username")
    info.realname=p.getTagData("realname")
    info.password=p.getTagData("password")
    info.groups=p.getTagData("groups").split(",")
    data.users.append(info)
    
partitioning=doc.getTag("partitioning")
partitioningType=partitioning.getAttribute("partitioning_type")

for q in partitioning.tags():
    partinfo=yaliPartition()
    partinfo.partitionType=q.getAttribute("partition_type")
    partinfo.format=q.getAttribute("format")
    partinfo.ratio=q.getAttribute("ratio")
    partinfo.fsType=q.getAttribute("fs_type")
    partinfo.mountPoint=q.getAttribute("mountpoint")
    partinfo.disk=q.firstChild().data()
    data.partitioning.append(partinfo)

