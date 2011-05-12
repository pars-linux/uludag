#!/bin/bash

#### SETTINGS ######
#
# CHANGE THIS

moveDir="/home/mehmet/Masaüstü/sphinx-structure"
####################

baseUrl="http://svn.pardus.org.tr/uludag/trunk/kde/"

#projects=("disk-manager" "user-manager")
projects=("disk-manager")

projectSubDir="/manager"
rootDir=`pwd`
for project in "${projects[@]}"
do
    if [ ! -d $project ]
    then
        echo "yok"
        cd $rootDir
        svn co $baseUrl$project

    fi

    if [ -d $project ]
    then
        svn up $baseUrl$project
        cd $project$projectSubDir
        python setup.py build
        cd doc
        cp $rootDir/templates/* *_templates
        cp $rootDir/static/* *_static
        make html
        # is it enough to move just html dir?
        echo $moveDir
        mv *_build $moveDir
    fi

done

