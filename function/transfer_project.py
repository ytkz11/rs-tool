#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2023/12/22 15:12 
# @File : transfer_project.py
from osgeo import ogr, gdal
from osgeo import osr
import os

# 将矢量文件投影转换为 WGS84 坐标系并解决中文乱码问题
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
        where="1=1",
        accessMode='overwrite',
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


if __name__ == '__main__':
    shapeFilePath = r'D:/temp/out/Fisheries_20190927.shp'
    saveFolderPath = r'D:/temp/out/84'

    # 使用修改后的函数并指定源文件编码为 GBK
    VectorTranslate(
        shapeFilePath,
        saveFolderPath,
        format="ESRI Shapefile",
        accessMode=None,
        dstSrsESPG=4326,
        selectFields=None,
        geometryType="POLYGON",
        dim="XY",
    )
