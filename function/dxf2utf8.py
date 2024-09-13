#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2024/9/13 17:46 
# @File : dxf2utf8.py 
'''

'''
import dbf
import pandas as pd

# 读取.dbf文件
table = dbf.Table(r'D:\temp\out\84\Fisheries_20190927.dbf')
table.open()
records = [r.field_dict for r in table]
table.close()

# 将记录转换为DataFrame并保存为CSV
df = pd.DataFrame(records)
df.to_csv('temp.csv', index=False, encoding='utf-8')

# 重新从CSV读取并转换回.dbf
df = pd.read_csv('temp.csv')
new_table = dbf.Table('D:\temp\out\84\Fisheries_201909271.dbf', df.columns.str.replace('.', ''))
new_table.open(mode=dbf.WN)
for i, row in df.iterrows():
    new_table.append(row.values.tolist())
new_table.close()

