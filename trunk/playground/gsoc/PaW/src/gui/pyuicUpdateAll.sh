# ahmet alp balkan

for f in ./widget*.ui
    do pyuic4 $f -o `basename $f ui`py
    echo $f
done
date
