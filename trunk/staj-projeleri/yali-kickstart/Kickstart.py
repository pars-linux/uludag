#!/usr/bin/python
#

import re
import sys
from yalireadpiks import *
sys.path.append("/home/zeynep/svn/uludag/yali/yali")
from localedata import *
correctData=yaliKickstartData()

class userErrors:
    def __init__(self):
        self.Empty=False
        self.Uname=False
        self.Rname=False
        self.Password=False
class partitionErrors:
    def __init__(self):
        self.PartitionType=False
        self.Format=False
        self.Disk=False
        self.FsType=False
        self.MountPoint=False
class errors:
    def __init__(self):
        self.Keymap=False
        self.Lang=False
        self.Root=False
        self.Users=False
        self.Empty=False
        self.Disk=False
        self.Root=False
        self.TotalRatio=False
class userFunctions:
    def __init__(self,username):
        self.username=username
    def checkAutologin(self):
        for currentUser in correctData.users:
            if(currentUser.autologin=="yes"):
                return True
        return False

    def checkValidity(self):
        if self.username and re.search("[0-9a-zA-Z.?!_-]",self.username):
            return True
        return False

    def checkName(self):
        for usr in correctData.users:
            if(usr.username==self.username):
                return True
        return False
class otherFunctions:
    def __init__(self,key):
        self.key=key
    
    def checkKeymap(self):
        for element in yaliKickStart().KeymapXList:
            if element==self.key:
                return True
        return False       
        
class partitionFunctions:
    def __init__(self,fs,disk):
        self.fs=fs
        self.disk=disk
    def checkFileSystem(self):
        for element in yaliKickStart().fileSystems:
            if element==self.fs:
                return True
        return False
    def checkFileSystem2(self):
        for element in yaliKickStart().fileSystems2:
            if element == self.fs:
                return True
        return False
    def checkDiskSyntax(self):
        return re.match("[h,s]d(\D{1})[1-9]$",self.disk) 

class yaliKickStart(yaliKickstartData):    
    def __init__(self):
        self.KeymapXList=["us","ara","be","bg","es","hr","cz","dk","ee","fi","fr","de","gr","hu","is","it","jp","mkd","no","pl","pt","br","ru","srp","sk","si","se","trq","trf","ua","vn","gb"]
        self.fileSystems=["swap","ext3","ntfs","reiserf","xfs"]
        self.fileSystems2=["ext3","xfs"]
        self.defaultGroups=["audio","dialout","disk","pnp","pnpadmin","power","removable","users","video"]
        self.errorList=[]
        self.RatioList=[]
        self.data=main("/home/zeynep/Desktop/yali3.xml")
        self.total=0
    
    def checkRatio(self):
        for eachRatio in self.data.partitioning:
            self.RatioList.append(eachRatio.ratio)
        for i in self.RatioList:
            self.total+=int(i)
        if self.total==100:
            return True
        return False
   
    def checkAllOptions(self):
        error=errors()
        otherFunct=otherFunctions(self.data.keyData)
        
        ###language selection###
        
        
        if(locales.has_key(self.data.language)):
            correctData.language=self.data.language
        else:
            error.Lang=True
            self.errorList.append("Language Error: %s does not exist"%self.data.language)
            
            
         ###keymap selection###
        
        
        if(self.data.keyData):
            if (otherFunct.checkKeymap()):
                correctData.keyData=self.data.keyData
            else:
                error.Keymap=True
                self.errorList.append("Keymap Error: %s not valid "%self.data.language)
        else:
            if error.Lang!=True:
                for lang in getLangsWithKeymaps():
                    if(lang[0]==correctData.language):
                        if(correctData.language=="tr"):
                            correctData.keyData=lang[1][0].X
                        else:
                            correctData.keyData=lang[1].X
                        break
                else:
                    error.Keymap=True
                    self.errorList.append("Keymap Error: Cannot associate Keymap for %s"%self.data.language)
                        
                        
        ###root password selection###
        
        
        if(len(self.data.rootPassword)<4):
            error.Root=True
            self.errorList.append("Root Password Error : Password is too short")
        else:
            correctData.rootPassword=self.data.rootPassword
            
            
        ###hostname selection###
        
        
        if(self.data.hostname):
            correctData.hostname=self.data.hostname
        else:
            correctData.hostname="pardus"


        ###users selections###

    
        if(len(self.data.users)==0):
            error.Users=True
            self.errorList.append("User Error: No user entry")
        else:
            correctData.users=[]
            for user in self.data.users:
                userError=userErrors()
                checkFunctions=userFunctions(user.username)
                if(user.autologin=="yes" and checkFunctions.checkAutologin()==0):
                    user.autologin="yes"
                else:
                    user.autologin="no"
                if (user.username=="root" or checkFunctions.checkValidity()!=True or checkFunctions.checkName()==True):
                    userError.Uname=True
                    if (user.username and userError.Uname==True):
                        self.errorList.append("Username Error for %s : username already exist or not valid"%user.username)
                    else:
                        self.errorList.append("Username Error : no Entry")
                if not user.realname:
                    userError.Rname=True
                    if userError.Uname!=True:
                        self.errorList.append("Real name Error for %s: No entry"%user.username)
                if (len(user.password)<4 or user.username==user.password or user.realname==user.password):
                    userError.Password=True
                    if userError.Uname!=True:
                        self.errorList.append("Password Error for %s "%user.username)
                if len(user.groups)==0:
                    user.groups=self.defaultGroups            
                if(userError.Uname!=True and userError.Rname!=True and userError.Password!=True):
                    correctData.users.append(user)

        if (len(correctData.users)==0):
            error.Users=True
            self.errorList.append("User Error: No user added")
        
        
        ###partitioning selection###
        
        correctPart=yaliPartition()
        if(self.data.partitioningType=="auto" or self.data.partitioningType!="manuel"):
            correctData.partitioningType="auto"
            if(len(self.data.partitioning)!=1):
                error.Empty=True
                self.errorList.append("Auto Partitioning Error : No partition entry  or too many partition")
            else:
                PartiFunction=partitionFunctions(self.data.partitioning[0].fsType,self.data.partitioning[0].disk)
                print self.data.partitioning[0].disk
                if not PartiFunction.checkDiskSyntax():
                    error.Disk=True
                    self.errorList.append("Auto Partitioning Error : Wrong Disk Syntax")
                else:
                    correctPart.partitionType="pardus_root"
                    correctPart.format="true"
                    correctPart.ratio="100"
                    correctPart.disk=self.data.partitioning[0].disk
                    correctData.partitioning.append(correctPart)
                    
                             
        elif(self.data.partitioningType=="manuel"):
            correctData.partitioningType="manuel"
    
            if(len(self.data.partitioning)==0):
                error.Empty=True
                self.errorList.append("Manuel Partitioning Error : No partition entry ")
            else:
                for partitionRoot in self.data.partitioning:
                    if partitionRoot.partitionType=="pardus_root": #pardus_root is required
                        break
                else:
                    error.Root=True
                    self.errorList.append("Manuel Partitioning Error : \"pardus_root\" missing ")
                if(self.checkRatio()!=True):
                    error.TotalRatio=True
                    self.errorList.append(" Ratio Error : Total not equal to 100")
                else:    
                    if(error.Empty!=True and error.Root!=True):
                        for partition in self.data.partitioning:
                            errorPartition=partitionErrors()
                            functPart=partitionFunctions(partition.fsType,partition.disk)
                            if  not (partition.partitionType=="pardus_root" or partition.partitionType=="pardus_swap" or partition.partitionType=="pardus_home" or partition.partitionType=="other"):
                                errorPartition.PartitionType=True
                                self.errorList.append("Partition type Error :%s not valid"%partition.partitionType)
                            if(partition.format!="false"):
                                partition.format="true"
                            if not (functPart.checkDiskSyntax()):
                                errorPartition.Disk=True
                                self.errorList.append(" Disk Error for %s: %s not valid"%(partition.partitionType,partition.disk))
                            if (partition.partitionType!="other"):
                                if not (functPart.checkFileSystem2()):
                                    errorPartition.FsType=True
                                    self.errorList.append("File system Error for %s : %s not valid"%(partition.partitionType,partition.fsType))
                            else:
                                if not (functPart.checkFileSystem()):
                                    errorPartition.FsType=True
                                    self.errorList.append("File system Error for %s : %s not valid"%(partition.partitionType,partition.fsType))
                            if  partition.mountPoint!=None  and not(re.search("[a-zA-Z0-9]",partition.mountPoint)) :
                                errorPartition.MountPoint=True
                                self.errorList.append("Mountpoint Error for %s : %s not valid"%(partition.partitionType,partition.mountPoint))
                            if(errorPartition.PartitionType!=True and errorPartition.Disk!=True and errorPartition.FsType!=True and errorPartition.MountPoint!=True):
                                correctData.partitioning.append(partition)
        return self.errorList
    
    def checkFileValidity(self):
        correctData=None
        self.errorList=self.checkAllOptions()
        if(len(self.errorList)==0):
            return True
        return self.errorList
    def getValues(self):
        if self.checkFileValidity() == True:
            print self.errorList
            return correctData
        return self.errorList
    

