#!/bin/bash

for i in `cat /home/pardusman/internal/trunk/testler/surum_ici_testler/2008/20090608/ack`
 do
     if [ ! -e $i ]; then
         echo $i
         cp ../packages-test/$i . || exit 1
     fi
 done

