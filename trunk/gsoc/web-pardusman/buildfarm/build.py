# -*- coding: utf-8 -*-
#ifndef BUILD.PY
#define BUILD.PY
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
sys.path.insert(1,'/home/mycode/pardusman')

#set Django project environment
import settings
from django.core.management import setup_environ

setup_environ(settings)

from pardusman.wizard.models import Userlogs, buildfarm_queue, onprogress_queue, scheduled_distro

import time,os, threading, subprocess, tempfile



def make_image(project_file,work_dir,queue_object):
    process = subprocess.Popen(['/sbin/mkpardus','make',project_file,work_dir, \
            'file://'+ settings.REPOS_URL], stdout=subprocess.PIPE, stderr=subprocess.PIPE ) 

    stdout,stderr = process.communicate()


    logfile_name = tempfile.mkstemp(prefix='buildlog_',dir=os.path.join(settings.BUILD_LOGS))[1]
    logfile = file(logfile_name,'w+')
    logfile.write("\n#Standard Output\n\n")
    logfile.write(stdout)
    logfile.write("\n#Standard Error\n\n")
    logfile.write(stderr)
    logfile.close()
    os.chmod(logfile_name,655)
 

    return os.path.basename(logfile_name)


class Buildfarm(threading.Thread):
    def __init__(self,project_file,work_dir,queue_object):
        self.project_file = project_file
        self.work_dir = work_dir
        self.queue_object = queue_object
        threading.Thread.__init__(self)

    def run(self):

        log = make_image(self.project_file, self.work_dir,self.queue_object)


        sdo = scheduled_distro.objects.get(id=self.queue_object.id)


        for image_file in os.listdir(self.work_dir):

            for img in settings.IMAGE_FORMATS:
                if image_file.endswith(img):
                    self.queue_object.image_file = os.path.join(self.work_dir,image_file)
                    self.queue_object.status = 'Completed'
                    os.system("mv %s %s" % (self.queue_object.image_file, os.path.join(settings.BUILDS_DIR,image_file)))
                    sdo.image_url = os.path.join(settings.BASE_PROJECTS_URL,"builds",image_file)
                    sdo.progress = "Success"
                    self.queue_object.save()


        sdo.log_url = os.path.join(settings.BASE_PROJECTS_URL,'logs',log)


        if self.queue_object.status == 'on progress':
            sdo.progress = "Failed"

        sdo.save()

        os.system("umount %s" %os.path.join(self.work_dir,"image/proc"))
        os.system("umount %s" %os.path.join(self.work_dir,"image/sys"))
        
        os.system("rm -rf %s" %self.work_dir)
        self.queue_object.delete()




#Add project to onprogress_queue

def build_engine_add(project):
    queue_item = onprogress_queue()
    queue_item.id = project.id

    tempdir = tempfile.mkdtemp(prefix='build_',dir=os.path.join(settings.BUILD_CACHE_DIR))
    try:
        os.mkdir(tempdir)
    except:
        pass

    queue_item.work_dir = tempdir
    queue_item.status = "on progress"

    sdo = scheduled_distro.objects.get(id=queue_item.id)
    sdo.progress = "building.."
    sdo.save()

    queue_item.save()
    build_thread = Buildfarm(project.project_file, tempdir,queue_item)
    build_thread.start()
    project.delete()


i=0
while True:
    print i
    i+=1

    if(onprogress_queue.objects.count() < settings.BUILD_LIMIT):

        if buildfarm_queue.objects.count() > 0:
            project = buildfarm_queue.objects.order_by('date')[0]
            build_engine_add(project)

    time.sleep(settings.TIME_INTERVAL)



