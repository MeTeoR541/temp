import requests
import time
import json
import os
from os import listdir

#REST API server
REST_url = "http://loaclhost:8090/tasks/"

#api_token in cuckoo.conf
header = {"Authorization": "Bearer LCHGGYA-mHKzIouVMCV40Q"}
CREATE = "create/file"
REPORT = "report/"
first = True
start_id = 1

os.mkdir("./json_file")

#最外層迴圈遍歷病毒家族的資料夾
file_list = listdir("./malware")
for family_name in file_list:
    family_path = "./malware/" + family_name
    SAMPLE_files = listdir(family_path)
    first = True
    #遍歷家族資料夾下的病毒    
    for sample in SAMPLE_files:
        file_path = family_path + "/" + sample
        file = open(file_path, "rb")
        files = {"file": ("temp_file_name", file)}

        #發送 POST request 給 http://loaclhost:8090/tasks/create/file 來上傳病毒到 cuckoo 裡
        #parameters 需要一個識別的 header 還有病毒檔案；選用: timeoust 120s
        r = requests.post(REST_url + CREATE, headers=header, files=files, timeout=120)

        #提取回傳值的 json 型式並取出 task_id 標籤下的資訊
        task_id = r.json()["task_id"]

        #設定當前家族第一個病毒的 task_id，作為下載 report 的起始編號 
        if first:
            start_id = task_id
            first = False

        #避免一次丟太多病毒導致電腦當機，休息 10s 再上傳下一個病毒
        time.sleep(10)

    task_id += 1

    #遍歷當前家族的第一個病毒到最後一個
    for i in range(start_id, task_id):

        #先確認分析是否完成再丟 request 去取 report
        #發送 GET request 給 http://loaclhost:8090/tasks/view/<task_id> 來取得目前分析的進度
        r = requests.get(REST_url + "view/" + str(i), headers=header)

        #提取回傳值的 json 型式並取出 task 類別下 status 的資訊
        check = r.json()["task"]["status"]

        #如果未完成分析，停留在這層迴圈等待分析結束
        while "reported" != check:
            r = requests.get(REST_url + "view/" + str(i), headers=header)
            check = r.json()["task"]["status"]

        #發送 GET request 給 http://loaclhost:8090/tasks/report/<task_id>/json 來取得報告資訊    
        r = requests.get(REST_url + REPORT + str(i) + "/json", headers=header)
        family_path = "./json_file/" + family_name
        if i == start_id:
            os.mkdir(family_path)
        save = open(family_path + "/" + str(i) + ".json", "w")

        #以 json 型式儲存報告
        json.dump(r.json(), save)
        print(str(i) + " is completed")