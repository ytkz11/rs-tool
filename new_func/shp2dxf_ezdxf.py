#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2024/8/28 下午5:23 
# @File : shp2dxf.py 
'''
初步完成
'''


import os
import ezdxf
from osgeo import ogr


class Shp2Dxf:
    def __init__(self, in_file):
        self.in_file = in_file
        self.out_file = os.path.splitext(in_file)[0] + '.dxf'

    def read_shp_by_ogr(self):
        ds = ogr.Open(self.in_file)
        shape = ds.GetLayer()
        attribute_names = []
        ldefn = shape.GetLayerDefn()

        geom_list = []
        for i in range(shape.GetFeatureCount()):
            feature = shape.GetFeature(i)
            geom = feature.GetGeometryRef()
            geom_list.append(geom.ExportToWkt())  # 将几何信息保存为WKT格式
        return geom_list

    def shp2dxf(self) -> None:
        # 读取Shapefile中的几何信息
        geom_list = self.read_shp_by_ogr()

        # 创建一个新的DXF文件
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()  # 获取模型空间

        # 将几何信息转换为DXF实体并添加到DXF文件中
        for geom_wkt in geom_list:
            geom = ogr.CreateGeometryFromWkt(geom_wkt)
            geom_type = geom.GetGeometryType()

            if geom_type == ogr.wkbPoint:  # 点类型
                x, y = geom.GetX(), geom.GetY()
                msp.add_point((x, y))
            elif geom_type == ogr.wkbLineString:  # 线类型
                points = geom.GetPoints()
                msp.add_lwpolyline(points)
            elif geom_type == ogr.wkbPolygon:  # 多边形类型
                ring = geom.GetGeometryRef(0)  # 获取多边形的外环
                points = ring.GetPoints()

                # 创建Hatch对象
                hatch = msp.add_hatch(color=7)  # 设置填充颜色，默认颜色为7（白色或黑色，取决于背景）

                # 添加路径
                path = hatch.paths.add_polyline_path(points, is_closed=True)

        # 保存DXF文件
        doc.saveas(self.out_file)
        print(f"Successfully converted {self.in_file} to {self.out_file}")

    def readdxf(self, file):
        doc = ezdxf.readfile(file)
        msp = doc.modelspace()
        for entity in msp:
            print(entity)

        for layer in doc.layers:
            print(layer.dxf.name)
        print()
if __name__ == '__main__':
    # in_file = r'd://temp/create_shp_by_fiona.shp'

    in_file = input("输入shp文件路径：")
    try:
        converter = Shp2Dxf(in_file)
        converter.shp2dxf()
        # converter.readdxf(converter.out_file)

        # converter.shp2dxf()
    except Exception as e:
        print(e)
    input("已完成")