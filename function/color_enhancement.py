#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2024/7/3 下午1:49 
# @File : color_enhancement.py 
'''
色彩增强
'''
from osgeo import gdal
import numpy as np
import os
import shutil
import argparse

class ColorEnhancement:
    def __init__(self, file, output=None, value=0.3):
        self.file = file
        self.value = value
        self.output = output
        if output is None:
            self.output = os.path.dirname(self.file)
        if os.path.exists(self.output) == False:
            print('输出文件夹不存在，开始创建输出文件夹')
            os.makedirs(self.output)
        self.outfile = os.path.join(self.output, os.path.basename(os.path.splitext(self.file)[0] + '_color_enhancement.tif'))

        self.dataset = gdal.Open(self.file)
        self.rows = self.dataset.RasterYSize  # todo  图像宽度
        self.cols = self.dataset.RasterXSize  # todo  图像长度
        self.bands = self.dataset.RasterCount  # TODO 图像波段数量
        if self.bands >=3:
            self.image_setting()

    def image_setting(self):
        self.proj = self.dataset.GetProjection()  # todo 地图投影信息
        self.geotrans = self.dataset.GetGeoTransform()  # todo 仿射矩阵
        self.longitude = self.geotrans[0]  # todo 经度
        self.latitude = self.geotrans[3]  # todo 纬度
        self.pixelWidth = self.geotrans[1]  # todo x轴空间间隔
        self.pixelHeight = self.geotrans[5]
        self.getband1 = self.dataset.GetRasterBand(1).ReadAsArray()
        self.getband2 = self.dataset.GetRasterBand(2).ReadAsArray()
        self.getband3 = self.dataset.GetRasterBand(3).ReadAsArray()
        self.getband4 = self.dataset.GetRasterBand(4).ReadAsArray()

        Driver = self.dataset.GetDriver()
        geoTransform1 = self.dataset.GetGeoTransform()
        ListgeoTransform1 = list(geoTransform1)
        ListgeoTransform1[5] = ListgeoTransform1[5]
        newgeoTransform1 = tuple(ListgeoTransform1)
        proj1 = self.dataset.GetProjection()
        self.outDataset = Driver.Create(self.outfile, self.cols, self.rows, 4, gdal.GDT_Byte)
        self.outDataset.SetGeoTransform(newgeoTransform1)
        self.outDataset.SetProjection(proj1)

        origin_rpc_file = os.path.splitext(self.file)[0] + '.rpc'
        origin_rpb_file = os.path.splitext(self.file)[0] + '.rpb'

        if os.path.exists(origin_rpc_file):
            print('{}存在rpc文件'.format(self.file))
            self.out_rpc_file = os.path.splitext(self.outfile)[0] + '.rpc'
            print('复制rpc文件到输出路径')
            shutil.copy(origin_rpc_file, self.out_rpc_file)
        if os.path.exists(origin_rpb_file):
            self.out_rpb_file = os.path.splitext(self.outfile)[0] + '.rpb'
            print('复制rpb文件到输出路径')
            shutil.copy(origin_rpb_file, self.out_rpb_file)
    def NDVI(self):
        """
        Calculate ndvi index
        """
        b4 = self.getband4.astype(np.float32)
        b3 = self.getband3.astype(np.float32)
        return ( b4- b3)/(b4 +  b3)

    def vegetation_enhancement(self, ndvi):
        '''
        （B3 gt 0.2）*(b2*0.8+b4*0.2)+（B3 le 0.2）*b2
        :return:
        '''

        # ndwi = self.NDWI()

        arr_ = self.getband2.copy()
        mask = ndvi > 0.2
        arr_[mask] = self.getband2[mask] * self.value + self.getband4[mask] * (1- self.value)
        arr_[ndvi < 0.2] = self.getband2[ndvi < 0.2]
        return arr_


    def process(self):
        ndvi = self.NDVI()
        # ndwi = self.NDWI()
        for i in range(self.bands):
            if i == 1:
                data = self.vegetation_enhancement(ndvi)
                data_green = self.dataset.GetRasterBand(i + 1).ReadAsArray()
                data_uint8_green = linear_stretch(data_green, 2)
                data_uint8 = linear_stretch(data, 2)

                # data_uint8 = data_uint8_green
                mask = ndvi < 0.2
                data_uint8[mask] = data_uint8_green [mask]


            else:
                data = self.dataset.GetRasterBand(i+1).ReadAsArray()
                data_uint8 = linear_stretch(data,2)
            outband =  self.outDataset.GetRasterBand(i+1)
            outband.WriteArray(data_uint8)

def linear_stretch(data, num=1):
    # every band process linear stretch

    data_8bit = data
    data_8bit[data_8bit == -9999] = 0

    # 把数据中的nan转为某个具体数值，例如
    # data_8bit[np.isnan(data_8bit)] = 0
    d2 = np.percentile(data_8bit, num)
    u98 = np.percentile(data_8bit, 100 - num)

    maxout = 255
    minout = 0
    data_8bit_new = minout + ((data_8bit - d2) / (u98 - d2)) * (maxout - minout)
    data_8bit_new[data_8bit_new < minout] = minout
    data_8bit_new[data_8bit_new > maxout] = maxout
    data_8bit_new = data_8bit_new.astype(np.uint8)

    return data_8bit_new
def get_file_name(file_dir, type1):
    """
        搜索 后缀名为type的文件  不包括子目录的文件
        #
        """
    L = []
    if type(type1) == str:
        if len([type1]) == 1:
            filelist = os.listdir(file_dir)
            for file in filelist:
                if os.path.splitext(file)[1] == type1:
                    L.append(os.path.join(file_dir, file))
    if type(type1) != str:
        if len(type1) > 1:
            for i in range(len(type1)):
                filelist = os.listdir(file_dir)
                for file in filelist:
                    if os.path.splitext(file)[1] == type1[i]:
                        L.append(os.path.join(file_dir, file))
    return L
if __name__ == '__main__':

    input = r'X:\\GF2.tif'
    output = r'X:\\output'
    value = 0.5

    if os.path.isfile(input):
        print('输入为文件，进行单个文件色彩增加')

        A = ColorEnhancement(input, output, value)
        if A.bands >=3:
            a = A.process()
    else:
        print('输入为文件夹，进行批量色彩增加')
        print('检索该文件夹下的TIF、tif')
        tiflists = get_file_name(input, ['.tif','.tiff','.TIF','.TIFF'])
        print('该文件夹下有{}个tif'.format(len(tiflists)))
        i = 0
        for tif in tiflists:
            A = ColorEnhancement(tif, output, float(value))
            if A.bands >= 3:
                a = A.process()
            # else:
            #     print('{}波段数不足3个'.format(tif))
            i += 1
            print("\r批量色彩增加: [{0:50s}] {1:.1f}%".format('#' * int(i / len(tiflists) * 50),
                                                            i / len(tiflists) * 100), end="",
                  flush=True)
        print('完成色彩增加')

    # file = r'X:\LiuHuan\0703邓开元\测试数据\GF2_test.tif'
    # A = ColorEnhancement(file,0.5)
    # a = A.process()
    # print()
