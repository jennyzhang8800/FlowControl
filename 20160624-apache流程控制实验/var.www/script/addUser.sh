#!/bin/bash
user=$1
passwd=$2
filename=$3
cd /var/www/FlowControl/
echo `whoami`
htpasswd -b ${filename} ${user} ${passwd}
