#!bin/bash -

####################
#               
#   解析jsonl檔  
#
####################

#################################################################
# 說明：grep尋找motif_dataset.jsonl裡符合"reported_family": "且任意
#      數量不包含"的字符，把相符的部分管線傳給下一個grep找出任意不包含
#      "結尾的字符，最後把相符的部分傳給malware_family_list
#################################################################
malware_family_list=$(grep -o '"reported_family": "[^"]*' motif_dataset.jsonl | grep -o '[^"]*$')

# malware_family以空白為分隔形成的陣列
malware_family=($malware_family_list)

# 取出md5的方式同上
malware_md5_list=$(grep -o '"md5": "[^"]*' motif_dataset.jsonl | grep -o '[^"]*$')
malware_md5=($malware_md5_list)


#######################
#               
#   計算每個家族的數量  
#
#######################

# 利用sort -u讓此陣列把相同的家族刪掉，tr為用後面的參數取代所有前面的參數
family_class=($(echo "${malware_family[@]}" | tr ' ' '\n' | sort -u | tr ' ' '\n'))
# 家族的總數：取出family_class的長度
length=${#family_class[*]}

# 宣告一個關聯式矩陣
declare -A family_count
# 利用family名稱為鍵值初始化關聯式矩陣
for ((i=0;i<$length;++i))
do
    family_count[${family_class[i]}]=0
done

# 遍歷每個病毒，來計算各家族的數量
for val in ${malware_family[@]}
do
    let family_count[$val]++
done


##########################
#               
#   把病毒歸類的各個資料夾  
#
##########################

# 我們只需選用數量大於20的家族，因次數量大於20才會建立資料夾
for val in ${family_class[@]}
do
    if ((${family_count[$val]} > 20))
    then
        mkdir ./malware/$val
        printf '%s %d\n' "$val" "${family_count[$val]}"
    fi
done

# 遍歷所有病毒，
# 把家族數量大於20的病毒複製一份到我們新建的家族資料夾
i=0
for val in ${malware_family[@]}
do 
    if ((${family_count[$val]} > 20))
    then 
        cp ./MOTIF_defanged/MOTIF_${malware_md5[i]} ./malware/$val/${malware_md5[i]}
    fi
    let i++
done