#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2024/1/3 20:32
# @File : RestoreShp.py

# 修复shp文件， shp文件中的几何数据和属性数据不一致
import os
import shutil
from struct import unpack
import dbf

class RestoreShp(object):
    def __init__(self, file, outpath=None):
        self.file = file
        self.outpath = outpath
        if self.outpath is None:
            self.outpath = os.path.dirname(self.file)
        if not os.path.exists(self.outpath):
            os.makedirs(self.outpath)
        if os.path.exists(self.file) is None:
            raise Exception('File does not exist')
        else:
            self.dbffile = os.path.splitext(self.file)[0] + '.dbf'

        self.outfile = [os.path.join(self.outpath, os.path.splitext(os.path.basename(self.file))[0] + '_restore.shp'),
                        os.path.join(self.outpath, os.path.splitext(os.path.basename(self.file))[0] + '_restore.dbf'),
                        os.path.join(self.outpath, os.path.splitext(os.path.basename(self.file))[0] + '_restore.shx'),
                        os.path.join(self.outpath, os.path.splitext(os.path.basename(self.file))[0] + '_restore.prj')]
        self.copyfile
    @property
    def copyfile(self):
        # 读取shp文件
        shutil.copyfile(self.file, self.outfile[0])
        shutil.copyfile(self.dbffile, self.outfile[1])
        shutil.copyfile(os.path.splitext(self.file)[0] + '.shx', self.outfile[2])

        try:
            shutil.copyfile(os.path.splitext(self.file)[0] + '.prj', self.outfile[3])
        except Exception as e:
            print(e)
        print('Copy the initial file to the output directory')

    def get_shp_shape_records(self):
        try:
            # First read the geometry data and attribute data of the original file, and return the number of geometric data
                self.shx = open("%s" % (self.outfile[2]), "rb")
                self.shx.seek(24)
                shxRecordLength = (unpack(">i", self.shx.read(4))[0] * 2) - 100
                self.numShapes = shxRecordLength // 8
                return self.numShapes
        except Exception as e:
            print(e)
    def get_dbf_shape_records(self):
        # db = dbf.Dbf(self.dbffile)
        with dbf.Table(self.outfile[1], codepage='utf8', default_data_types='enhanced') as table:
            pass
        return table
    def restore_shp(self):
        #  Number of records read from shp file

        shp_numrecords = self.get_shp_shape_records()
        #  Number of records read from dbf file
        table = self.get_dbf_shape_records()
        dbf_numrecords = len(table)


        # Check whether the number of shp and dbf records is equal
        if shp_numrecords != dbf_numrecords:
            num = shp_numrecords - dbf_numrecords
            if num > 0:
                print('The shp file has {} more records than the dbf file'.format(num))
                for i in range(num):
                    table.open(mode=dbf.READ_WRITE)
                    table.append()
                table.pack()

            else:
                print('The dbf file has {} more records than the shp file'.format(abs(num)))
                table.open(mode=dbf.READ_WRITE)
                for record in table[shp_numrecords:]:
                    dbf.delete(record)
                table.pack()

if __name__ == '__main__':
    file = input('Please enter the path of the shp file: ')
    outpath = input('Please enter the path of the output file: ')

    if os.path.exists(file) :
        record_num = RestoreShp(file, outpath).restore_shp()
        print('complete')
    else:
        print('File does not exist')
    input()

