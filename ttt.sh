python3 compare.py | while read i1 n i2 n res; 
do 
    a1=$( basename $i1 )
    a2=$( basename $i2 )
    if [ $a1 != $a2 -a $res != "нет" ] 
    then
        mkdir $res/${a1}_${a2}
        cp $i1 $i2 $res/${a1}_${a2}/
    fi
done
