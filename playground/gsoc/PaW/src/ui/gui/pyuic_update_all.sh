for f in ./*.ui
    do pyuic4 $f -o `basename $f ui`py
    echo $f
done
date