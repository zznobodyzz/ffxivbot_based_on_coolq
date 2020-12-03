# -*- coding: UTF-8 -*-

import sys
a = ('武器','头部','衣服','手部','腰带','裤子','鞋子','耳环','项链','手镯','戒指左','戒指右')
data = ''
with open('generate_db_example.txt', 'r', encoding = 'utf-8') as f:
    i = 0
    for line in f.readlines():
        l = line.replace('（', '(').replace('）', ')').strip('\n').split('	')
        data += "'%s':(" %(a[i])
        for ll in l:
            data += "'%s'," %(ll)
        data = data[:-1]
        data += '), \\\n'
        i += 1
    data += "'备注':() \\"
print(data)