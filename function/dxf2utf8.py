#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dbf

def write_dict_to_new_dbf(dbf_path, data_dicts):
    """
    根据给定的字典列表创建一个新的.dbf文件并写入数据。

    :param dbf_path: 新.dbf文件的路径。
    :param data_dicts: 包含数据的字典列表，每个字典代表一行记录。
    :return: None
    """
    # 确定字段名和类型
    fields = []
    for key in data_dicts[0]:
        # 根据数据类型推测字段类型
        if isinstance(data_dicts[0][key], int):
            fields.append((key, 'N', 10, 0))  # 整数型，宽度为10，小数位为0
        elif isinstance(data_dicts[0][key], float):
            fields.append((key, 'F', 15, 3))  # 浮点型，宽度为15，小数位数为3
        else:
            fields.append((key, 'C', 50))  # 字符型，宽度为50

    # 生成字段定义字符串
    field_specs = []
    for field in fields:
        if field[1] == 'C':
            field_specs.append(f'{field[0]} {field[1]}({field[2]})')  # 字符型字段
        else:
            field_specs.append(f'{field[0]} {field[1]}({field[2]},{field[3]})')  # 数值型字段

    # 将字段定义合并成字符串
    field_specs_str = ';'.join(field_specs)

    # 创建新的.dbf文件
    with dbf.Table(dbf_path, codepage='cp936', field_specs=field_specs_str) as table:
        table.open(dbf.READ_WRITE)  # 打开表格进行写操作
        # 写入数据
        for data_dict in data_dicts:
            record = table.append(data_dict)  # 创建一个新的空记录
            # for field, value in data_dict.items():
            #     record[field] = value  # 设置每个字段的值
            # record.store()  # 存储记录
import dbfread

def read_dbf(dbf_path, encoding='GBK'):
    table = dbfread.DBF(dbf_path, encoding=encoding)
    for record in table:
        print(record)

# 使用方法
dbf_file = r'D:\gadm\东德西德\shp\berlin.dbf'
read_dbf(dbf_file, encoding='GBK')
import dbfread

def try_encoding(dbf_path, encodings=['GBK', 'GB18030', 'UTF-8']):
    for encoding in encodings:
        try:
            table = dbfread.DBF(dbf_path, encoding=encoding)
            for record in table:
                print(f"Encoding: {encoding}")
                print(record)
                return encoding
        except UnicodeDecodeError:
            continue
    return None

# 使用方法
dbf_file = r'C:\Users\Administrator\Documents\WeChat Files\wxid_ejyl8luu57t121\FileStorage\File\2024-09\Fisheries_20190927\1\Fisheries_20190927.dbf'
dbf_file = r'C:\Users\Administrator\Documents\WeChat Files\wxid_ejyl8luu57t121\FileStorage\File\2024-09\Fisheries_20190927\1\Exp.dbf'

correct_encoding = try_encoding(dbf_file)
if correct_encoding:
    print(f"Correct encoding is: {correct_encoding}")
else:
    print("No correct encoding found.")
if __name__ == "__main__":
    dbf_path = r'D:\temp\out\test\Fisheries_20190927113.dbf'
    data_dicts = [
        {'IDD': '1', 'NAME': '张三', 'AGE': 25.5},
        {'IDD': '2', 'NAME': '李四', 'AGE': 30.3433},
        {'IDD': '3', 'NAME': '王五', 'AGE': 35.5}
    ]
    write_dict_to_new_dbf(dbf_path, data_dicts)
    print("DBF 文件已创建并写入数据。")
