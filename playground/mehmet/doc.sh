#!/bin/bash

# This script does svn chekout or update for the given projects to its
# directory and creates html doc files. Then moves these html files to
# the given directory.

# download below files to the workspace
# svn export http://svn.pardus.org.tr/uludag/trunk/playground/mehmet/templates
# svn export http://svn.pardus.org.tr/uludag/trunk/playground/mehmet/static

#### SETTINGS ######
#
# CHANGE THIS

# html files, index.html vs., will be moved there
moveDir="/home/mehmet/yy/projects"
####################


if [ ! -d $moveDir ]
then
    mkdir $moveDir
fi

# base url for projects
baseUrl="http://svn.pardus.org.tr/uludag/trunk/kde/"

#projects=("disk-manager" "user-manager")
projects=("disk-manager")

projectSubDir="/manager"

# this script's directory. svn checkout/update will be made here.
rootDir=`pwd`

for project in "${projects[@]}"
do
    cd $rootDir

    if [ ! -d $rootDir/templates/ ]
    then
        echo "Error: No templates directory found!"
        exit 1
    fi

    if [ ! -d $rootDir/static/ ]
    then
        echo "Error: No static directory found!"
        exit 1
    fi

    if [ ! -d $project ]
    then
        svn co $baseUrl$project
    else
        cd $project
        currentRevision=`svn info | grep "Revision:" | cut -d: -f2`
        svn up
        newRevision=`svn info | grep "Revision:" | cut -d: -f2`
        if [ $newRevision -eq $currentRevision ]
        then
            echo "aynii"
            exit 0
        fi
        cd ..
    fi

    if [ -d $project ]
    then
        cd $project$projectSubDir
        python setup.py build
        cd doc
        cp $rootDir/templates/* *_templates
        cp $rootDir/static/* *_static
        make html
        echo $?
        # is it enough to move just html dir?
        if [ ! -d $moveDir/$project ]
        then
            mkdir $moveDir/$project
        else
            rm -rf $moveDir/$project/*
        fi
        mv *_build/html/* $moveDir/$project
    fi

done
