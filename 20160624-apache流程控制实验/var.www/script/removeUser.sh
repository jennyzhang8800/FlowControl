#!/bin/bash
user=$1
filename=$2
cd /var/www/FlowControl/
htpasswd -D ${filename} ${user}
