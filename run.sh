#!/bin/bash

start_()
{
    cd $(pwd);
    nohup gunicorn ops_mail.wsgi:application -b 0.0.0.0:8002 -t 60  -w 2  > /data/code/ops_mail/logs/ops_mail.log 2>&1 &
    tail -f /data/code/ops_mail/logs/ops_mail.log
}


stop_()
{
    ps ax | grep 'gunicorn ops_mail.wsgi:application' | grep -v 'grep' | sed 's/^\s*//g' | cut -d ' ' -f 1 | xargs -I{} kill {}
}

restart()
{
    stop_
    start_
}

help_()
{
    echo ''
    echo 'usage:'
    echo '      ./start.sh            start the program'
    echo '      ./start.sh stop       stop the program'
    echo '      ./start.sh restart    restart the program'
    echo ''
}

main()
{
    argu=$1
    if [ "$argu" = "start" ]||[ "$argu" = "" ]; then
        start_
    elif [ "$argu" = "stop" ]; then
        stop_
    elif [ "$argu" = "restart" ]; then
        restart
    else
        help_
    fi
}

main $1
