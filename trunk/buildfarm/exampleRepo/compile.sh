#!/bin/bash

rm -rf minime
mkdir minime
rm -f *.pisi 

for i in a b c d e f
do
    pisi build $i/pspec.xml -D./minime
    pisi it $i*.pisi  -D./minime
done
