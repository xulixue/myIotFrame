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
    CheckProcess "sudo python2 blueScan.py"
    CheckQQ_RET=$?  
    if [ $CheckQQ_RET -eq 1 ]
    echo "不知道如果执行这里了说明什么。"
    then
    echo "没有找到上面的进程，将执行下面的动作..."
    echo "杀死所有残留"
    sudo sh killProByName.sh "python2 blueScan.py"
    #killall -9 blueScan.py    #注意，killall -9 python2 blueScan.py的话会杀掉所有带有python2的进程，
                               #相当于 killall -9 python2 和 killall -9 blueScan.py
    echo "关闭系统蓝牙！"
    sudo sh turnOff_bluetooth.sh &
    sleep 2
    echo "打开系统蓝牙！"
    sudo sh turnOn_bluetooth.sh &
    sleep 2
    sudo service bluetooth start
    sudo systemctl start bluetooth
    sleep 1
    sudo python2 blueScan.py
    echo "执行了一次" >> bluetooth_sta.log
    fi
    sleep 1
done 
