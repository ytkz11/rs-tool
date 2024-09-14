#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2024/09/14 19:12
# @File : transfer_project.py

import dbf
from osgeo import ogr, gdal, osr
import os
# 将矢量文件投影转换为 WGS84 坐标系并解决中文乱码问题


def convert_shapefile_and_extract_attributes(input_shp):
    """
    读取shapefile，转换坐标系为WGS84，并提取属性表数据为字典列表。

    :param input_shp: 输入的shapefile路径。
    :param save_folder: 保存转换后的shapefile的文件夹路径。
    :param target_crs: 目标坐标系的EPSG代码，默认为4326 (WGS84)。
    :return: 包含属性表数据的字典列表。
    """
    # 注册所有驱动
    ogr.RegisterAll()

    # 打开源shapefile
    data = ogr.Open(input_shp)
    if data is None:
        print(f"无法打开文件：{input_shp}")
        return None

    # 获取第一个图层
    layer = data.GetLayer()
    if layer is None:
        print("没有找到有效的图层")
        return None

    # 初始化属性表数据列表
    features_dict = []

    # 遍历每个要素
    for feature in layer:
        # 创建新字典来保存属性
        feature_dict = {}

        # 获取并保存属性值
        for i in range(feature.GetFieldCount()):
            field_name = layer.GetLayerDefn().GetFieldDefn(i).GetName()
            field_value = feature.GetFieldAsString(i)
            feature_dict[field_name] = field_value
        # 将属性字典添加到列表
        features_dict.append(feature_dict)

    # 关闭数据源
    data.Destroy()

    return features_dict

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
            table.append(data_dict)  # 创建一个新的空记录
def VectorTranslate(
        shapeFilePath,
        saveFolderPath,
        format="GeoJSON",
        accessMode=None,
        dstSrsESPG=4326,
        selectFields=None,
        geometryType="POLYGON",
        dim="XY",
):
    """
    转换矢量文件，包括坐标系、名称、格式、字段、类型、纬度等，并解决中文乱码问题。
    :param shapeFilePath: 要转换的矢量文件路径
    :param saveFolderPath: 生成矢量文件保存目录
    :param format: 输出矢量文件格式，建议使用 GeoJSON 或其他支持 UTF-8 的格式
    :param accessMode: None 表示创建，'update', 'append', 'overwrite' 等
    :param dstSrsESPG: 目标坐标系 EPSG 代码，4326 是 WGS84 地理坐标系
    :param selectFields: 要保留的字段列表，如果全保留则为 None
    :param geometryType: 几何类型，例如 "POLYGON", "POINT" 等
    :param dim: 输出矢量文件坐标纬度，通常使用 "XY"
    :return: 输出文件的路径
    """
    print("开始转为wgs84坐标系")

    # dbffile = os.path.splitext(shapeFilePath)[0] + '.dbf'
    # table = dbfread.DBF(dbffile, encoding='gbk')
    # for record in table:
    #     print(record)
    if not os.path.exists(saveFolderPath):
        os.makedirs(saveFolderPath)

    ogr.RegisterAll()

    # 确保文件名和内容编码为 UTF-8

    # gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    # gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    data = ogr.Open(shapeFilePath)
    layer = data.GetLayer()

    # 手动处理属性字段编码
    for feature in layer:
        for i in range(feature.GetFieldCount()):
            field_value = feature.GetFieldAsString(i)
            print(field_value)

    spatial = layer.GetSpatialRef()
    layerName = layer.GetName()
    data.Destroy()

    # 定义目标坐标系
    dstSRS = osr.SpatialReference()
    dstSRS.ImportFromEPSG(int(dstSrsESPG))

    # 设置保存文件路径和文件名
    if format == "GeoJSON":
        destDataName = layerName + ".geojson"
        destDataPath = os.path.join(saveFolderPath, destDataName)
    elif format == "ESRI Shapefile":
        destDataName = layerName + "_temp.shp"
        destDataPath = os.path.join(saveFolderPath, destDataName)
    else:
        print("不支持该格式！")
        return

    # 矢量转换选项，确保指定输出文件的编码为 UTF-8
    options = gdal.VectorTranslateOptions(
        format=format,
        srcSRS=spatial,
        dstSRS=dstSRS,
        reproject=True,
        selectFields=selectFields,
        layerName=layerName,
        geometryType=geometryType,
        dim=dim,

    )

    # 执行矢量转换
    gdal.VectorTranslate(
        destDataPath,
        srcDS=shapeFilePath,
        options=options
    )

    return destDataPath


def tif_reproject(file):
    ds = gdal.Open(file)
    gdal.Warp('1.tif', ds, dstSRS='EPSG:4326', targetAlignedPixels=True)


def transform_coordinate_and_recreate_new_dbf(input_shp, save_folder):
    temp_file_1 = VectorTranslate(
        input_shp,
        save_folder,
        format="ESRI Shapefile",
        accessMode=None,
        dstSrsESPG=4326,
        selectFields=None,
        geometryType="POLYGON",
        dim="XY",
    )
    attributes = convert_shapefile_and_extract_attributes(temp_file_1)
    print("开始转为WGS84坐标系")
    print(attributes)

    new_dbf_file = os.path.splitext(temp_file_1)[0] + "_new.dbf"
    write_dict_to_new_dbf(new_dbf_file, attributes)

    origin_dbf_file = os.path.splitext(temp_file_1)[0] + ".dbf"
    os.remove(origin_dbf_file)
    os.rename(new_dbf_file, origin_dbf_file)

    return temp_file_1  # 返回新的shapefile路径

# 示例调用
if __name__ == "__main__":
    input_shp = r'D:\temp\out\test\Fisheries_20190927.shp'
    save_folder = r'D:\temp\out\test'
    transform_coordinate_and_recreate_new_dbf(input_shp, save_folder)

