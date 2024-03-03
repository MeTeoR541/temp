import os
import numpy
import cv2
from os import listdir
def hex_dump(file, array, max_width):
    buf = file.read(max_width)     #read max_width bytes in a line for array row
    temp_array = numpy.zeros((1,max_width))
    while buf != b'':
        column = 0
        for i in buf:
            temp_array[0][column] = i
            column += 1
        buf = file.read(max_width)  
        array = numpy.concatenate((array,temp_array))      
    print(array)
    cv2.imshow('a',array)
    print(array)
    cv2.waitKey()
file_list = listdir("./malware")
for f in file_list:
    file = open("./malware/" + f,'rb')
    size = os.path.getsize("./malware/" + f)
    width = 0
    if size < 10000:
        width = 32
    elif size < 30000:
        width = 64
    elif size < 60000:
        width = 128
    elif size < 100000:
        width = 256
    elif size < 200000:
        width = 384
    elif size < 500000:
        width = 512
    elif size < 1000000:
        width = 768
    else:
        width = 1024
    number_array = numpy.zeros((1,width))
    hex_dump(file, number_array, width)