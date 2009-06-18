#!/bin/bash

 for i in $( ls ../packages-stable/*.pisi); do
     pathfilename=${i##*/}
     echo $pathfilename
     ln -s $i $pathfilename
 done

