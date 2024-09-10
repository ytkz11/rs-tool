#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2024/9/6 下午2:47 
# @File : shp2dxf_ezdxf_padding.py 
'''

'''
import os.path
from function.shp2dxf_ezdxf import *
class Shp2DxfPadding(Shp2Dxf):
    def __init__(self,filename):
        super().__init__(filename)
        self.get_field_name()
    def get_field_name(self):
        ds = ogr.Open(self.in_file)
        layer = ds.GetLayer()
        layer_defn = layer.GetLayerDefn()
        field_contents = []
        # 遍历所有的字段
        for i in range(layer_defn.GetFieldCount()):
            fieldDefn = layer_defn.GetFieldDefn(i)
            field_contents.append(fieldDefn.GetName())
        self.field = field_contents
        # 关闭数据源
        ds = None

        self.field_contents = field_contents
    def read_shp_by_ogr(self, field_name=None, text=None):

            # 打开数据源
            ds = ogr.Open(self.in_file)
            if ds is None:
                print(f"无法打开文件 {self.in_file}")
                return None

            # 获取图层
            layer = ds.GetLayer()
            if layer is None:
                print("没有找到有效的图层")
                return None

            # 获取图层定义
            layer_defn = layer.GetLayerDefn()

            # 检查字段是否存在
            field_index = layer_defn.GetFieldIndex(field_name)
            if field_index == -1:
                print(f"字段 {field_name} 不存在于数据集中")
                return None


            geom_dict = {}
            # 遍历所有要素

            if text is None:
                # 保存某个字段下所有的值
                for i, feature in enumerate(layer):
                    # 获取指定字段的值
                    value = feature.GetField(field_index)

                    geom = feature.GetGeometryRef()
                    if isinstance(geom_dict.get(value), list):
                        geom_dict[value].append(geom.ExportToWkt())
                    else:
                        geom_dict[value] = [geom.ExportToWkt()]

            else:
                for i, feature in enumerate(layer):
                    # 获取指定字段的值
                    value = feature.GetField(field_index)

                    geom = feature.GetGeometryRef()
                    if value == text:
                        if isinstance(geom_dict.get(value), list):
                            geom_dict[value].append(geom.ExportToWkt())
                        else:
                            geom_dict[value] = [geom.ExportToWkt()]
            # 关闭数据源
            ds = None


            return geom_dict
    def shp2dxf(self,field = None,text=None) -> None:
        # 读取Shapefile中的几何信息
        geom_dict = self.read_shp_by_ogr(field_name = field)

        # 创建一个新的DXF文件
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()  # 获取模型空间
        total = 0
        for key in geom_dict:
            total += len(geom_dict[key])
        print("保存地址在{}".format(os.path.dirname(self.in_file)))
        i = 0
        for key in geom_dict:

            # 将几何信息转换为DXF实体并添加到DXF文件中
            for geom_wkt in geom_dict[key]:
                i+=1
                print("\r转换DXF: [{0:50s}] {1:.1f}%".format('#' * int(i /total * 50),
                                                                  i / total * 100), end="",
                      flush=True)
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
                    hatch = msp.add_hatch(color=5)  # 设置填充颜色，默认颜色为7（白色或黑色，取决于背景）

                    # 添加路径
                    path = hatch.paths.add_polyline_path(points, is_closed=True)

            # 保存DXF文件
            out_file = os.path.splitext(self.in_file)[0] + '_' +str(key) +'.dxf'
            doc.saveas(out_file)
            # 清空msp
            msp.delete_all_entities()



if __name__ == '__main__':

    in_file = r'C:\Users\Administrator\Desktop\TEMP\create_shp_by_fiona.shp'
    try:
        converter = Shp2DxfPadding(in_file)

        converter.shp2dxf('target')
    except Exception as e:
        print(e)
    input("已完成")