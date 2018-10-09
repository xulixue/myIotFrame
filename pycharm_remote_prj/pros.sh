#!/bin/bash  
CheckProcess()  
{  
        if [ "$1" = ""];  
        then  
                return 1  
        fi  
  
    PROCESS_NUM=`ps -ef | grep "$1" | grep -v "grep" | wc -l`  
    if [ $PROCESS_NUM -eq 1 ];  
    then  
        return 0  
    else  
        return 1  
    fi      
}   
  
while [ 1 ] ; do  
    CheckProcess "./a.out"  
    CheckQQ_RET=$?  
    if [ $CheckQQ_RET -eq 1 ];  
    then  
     killall -9 a.out  
     exec ./a.out &  
    fi  
    sleep 1  
done 
