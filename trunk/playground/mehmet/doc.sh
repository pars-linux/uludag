#!/bin/bash

# This script doesi an svn chekout or update for the given projects to its
# directory and creates html doc files. Then moves these html files to
# the given directory.


# base url for projects
baseUrl="http://svn.pardus.org.tr/uludag/trunk/kde/"

#projects=("disk-manager" "user-manager")
projects=("disk-manager")

projectSubDir="/manager"

# this script's directory. svn checkout/update will be made here.
rootDir=`pwd`


function showUsage {

    echo -e "\tUsage: `./doc.sh` options (-f -dDirectory)"
    echo -e "\twhere directory is destination directory for moving files: Default is \".output\""
    echo -e "\tand f option forces a rebuild even if there is no change in repository."

}


function checkTemplate {

    if [ ! -d $rootDir/templates/ ]
    then
        svn export http://svn.pardus.org.tr/uludag/trunk/playground/mehmet/templates
    fi

    if [ ! -d $rootDir/static/ ]
    then
        svn export http://svn.pardus.org.tr/uludag/trunk/playground/mehmet/static
    fi

}


function createDoc {

    checkTemplate

    for project in "${projects[@]}"
    do
        cd $rootDir

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
                if [ "$2" != "yes" ]
                then
                    echo -e "\tInformation: Revision is not changed, no build is needed!"
                    exit 0
                fi
            fi
            cd ..
        fi

        mvDir=$1
        if [ -d $project ]
        then
            cd $project$projectSubDir
            python setup.py build kde4
            cd doc
            cp $rootDir/templates/* *_templates
            cp $rootDir/static/* *_static
            make html
            # is it enough to move just html dir?
            if [ ! -d $mvDir/$project ]
            then
                mkdir $mvDir/$project
                if [ ! $? -eq 0 ]
                then
                    # user didn't write absolute path
                    echo -e "\tInformation: project path is converted!"
                    mvDir=$rootDir/$mvDir
                    mkdir $mvDir/$project
                fi
            else
                rm -rf $mvDir/$project/*
            fi
            mv *_build/html/* $mvDir/$project
        fi

    done

}


#NO_ARGS=0
#E_OPTERROR=85

mvDir="output"
wantForce="no"


while getopts ":d:f" Option
do
  case $Option in
    d ) mvDir=$OPTARG;;
    f ) wantForce="yes";;
    * ) showUsage;;
  esac
done


if [ ! -d $mvDir ]
then
    if [[ $mvDir != */* ]]
    then
        mvDir=$rootDir/$mvDir
        echo -e "Information: Path was coverted to absolute path!"
    fi
    mkdir $mvDir
    if [ ! $? -eq 0 ]
    then
        echo -e "\tError: Move directory couldn't be created!"
        exit 1
    fi
else
    if [[ $mvDir != */* ]]
    then
        mvDir=$rootDir/$mvDir
        echo -e "Information: Path was coverted to absolute path!"
    fi
fi


createDoc $mvDir $wantForce

exit 0

