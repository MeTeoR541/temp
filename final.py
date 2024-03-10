import os
import numpy
import cv2
from os import listdir

#將file stream轉換為圖片
def hex_dump(file, width, family_name, idx):
    #將bytes轉換為2d array
    buf = numpy.fromfile(file, numpy.byte)
    val = len(buf) % width
    if val != 0:
        buf = numpy.append(buf, numpy.zeros(width - val))
    img = buf.reshape((-1, width))

    #將Array轉為圖片後儲存
    family_path = "./image/" + family_name
    if idx == 0:
        os.mkdir(family_path)
    cv2.imwrite(family_path + "/" + family_name + "_" + str(idx) + ".png", img)

#幫圖片建立新資料夾
os.mkdir("./images")

#尋訪malware資料夾
file_list = listdir("./malware")
for family_name in file_list:
    family_path = "./malware/" + family_name
    sibling_list = listdir(family_path)
    #尋訪這個family中的malware
    for idx, sibling in enumerate(sibling_list):
        file_name = family_path + "/" + sibling
        #設定寬度
        size = os.path.getsize(file_name)
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
        #轉換為圖片
        file = open(file_name, 'rb')
        hex_dump(file, width, family_name, idx)
        file.close()
