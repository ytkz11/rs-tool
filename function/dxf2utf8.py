#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/1/3 20:32
# @File : RestoreShp.py

import dbf
from io import StringIO

import dbf
import pandas as pd






if __name__ == '__main__':
    # 使用函数
    input_dbf = r'C:\Users\Administrator\Documents\WeChat Files\wxid_ejyl8luu57t121\FileStorage\File\2024-09\Fisheries_20190927\2\Fisheries_20190927.dbf'
    import dbfread

    # 指定编码为 GBK (如果文件是用 GBK 编码)
    table = dbfread.DBF(input_dbf, encoding='gbk')
    for record in table:
        print(record)

    # 调用函数
    # convert_encoding(input_dbf, output_dbf)