#! /usr/bin/python
import sys
import time
import os
import json
def readFile(path):
    file_object = open(path)
    try:
        text = file_object.read()
    finally:
        file_object.close()
        return text

def checkLog(logFilePath,c_time,overtime):
    time_in_millisecond = overtime
#    cc_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    c_time = '2017-06-09 00:12:11'
    start_time = long(time.time()*1000)
    while True:
        inputFile=open(logFilePath)
        result={}
        result["new_change"]=[]
        for line in inputFile:
            log_time=line[:19]
            if log_time>c_time:
                result["new_change"].append(line)
        inputFile.close()
        if result["new_change"]:
            result["overtime"]="false"
            break
        elapsed =long(time.time()*1000)-start_time
        if elapsed >=time_in_millisecond:
            result["overtime"]="true"
            break
    result=json.dumps(result,indent =2)
    return result
    
def get_last_line(inputfile):
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    dat_file = open(inputfile, 'rb')
    last_line = ""
    if filesize > blocksize:
        maxseekpoint = (filesize // blocksize)
        dat_file.seek((maxseekpoint - 1) * blocksize)
    elif filesize:
        # maxseekpoint = blocksize % filesize
        dat_file.seek(0, 0)
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()
    # print "last line : ", last_line
#    dat_file.close()
    return last_line

if __name__ == '__main__':
    c_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    overtime  = int(sys.argv[1])


    path = '/home/jenny/Kepler-2.5/test/mongo-oplog.log'
    print checkLog(path,c_time,overtime)
