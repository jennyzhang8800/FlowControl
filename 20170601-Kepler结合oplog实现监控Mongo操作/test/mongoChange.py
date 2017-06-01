#! /usr/bin/python

import os
def readFile(path):
    file_object = open(path)
    try:
        text = file_object.read()
    finally:
        file_object.close()
        return text

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
    dat_file.close()
    return last_line

if __name__ == '__main__':
    path = '/home/jenny/Kepler-2.5/test/mongo-oplog.log'
    #text = readFile(path)
    print get_last_line(path)
    
