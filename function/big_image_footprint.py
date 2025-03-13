#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2025/3/10 16:12 
# @File : big_image_footprint.py

import rasterio
from rasterio.windows import Window
from rasterio.features import geometry_mask
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
import numpy as np
from osgeo import ogr, osr
from tqdm import tqdm
import math, os
import matplotlib.pyplot as plt


def plot_footprint(footprint, title="Raster Footprint"):
    """使用 matplotlib 绘制足迹多边形"""
    fig, ax = plt.subplots(figsize=(10, 10))
    if isinstance(footprint, Polygon):
        footprint = MultiPolygon([footprint])
    for geom in footprint.geoms:
        if isinstance(geom, Polygon):
            x, y = geom.exterior.xy
            ax.plot(x, y, 'k-', linewidth=2)
            ax.fill(x, y, alpha=0.2, color='blue')
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(title)
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.grid(True)
    plt.show()


def get_valid_footprint(block, nodata_value, transform, window):
    """计算单个块的有效数据足迹，处理不同类型的nodata值"""

    if np.issubdtype(block.dtype, np.floating):
        if nodata_value is None:
            mask = ~np.isnan(block)
        else:
            mask = ~np.isclose(block, nodata_value, equal_nan=True)
    else:
        # 对于整数类型，直接比较
        if nodata_value is None:
            mask = block != 0  # 如果nodata为None，默认使用0作为无效值
        else:
            mask = block != nodata_value

    if not np.any(mask):
        return None

    shapes = rasterio.features.shapes(
        mask.astype(np.uint8),
        mask=mask,
        transform=transform
    )
    polygons = [Polygon(geom['coordinates'][0]) for geom, value in shapes if value == 1]
    return unary_union(polygons) if polygons else None


def save_footprint_to_file(footprint, output_path, format='shp', crs=None):
    """
    使用 ogr 将足迹保存为 shapefile 或 geopackage 文件

    参数:
    footprint: Shapely Polygon 或 MultiPolygon 对象
    output_path: 输出文件路径（包括扩展名）
    format: 文件格式，'shp' 或 'gpkg'，默认为 'shp'
    crs: 坐标参考系（osgeo.osr.SpatialReference 对象），如果为 None 则使用默认 WGS84
    """
    # 设置驱动
    if format.lower() == 'shp':
        driver_name = 'ESRI Shapefile'
        if not output_path.lower().endswith('.shp'):
            output_path += '.shp'
    elif format.lower() == 'gpkg':
        driver_name = 'GPKG'
        if not output_path.lower().endswith('.gpkg'):
            output_path += '.gpkg'
    else:
        raise ValueError("Format must be 'shp' or 'gpkg'")

    # 创建 OGR 驱动
    driver = ogr.GetDriverByName(driver_name)
    if driver is None:
        raise ValueError(f"OGR driver '{driver_name}' not available.")

    # 如果文件已存在，先删除
    if os.path.exists(output_path):
        driver.DeleteDataSource(output_path)

    # 创建数据源
    ds = driver.CreateDataSource(output_path)
    if ds is None:
        raise ValueError(f"Could not create output file: {output_path}")

    # 设置坐标系
    if crs is None:
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)  # 默认 WGS84
    else:
        srs = crs

    # 创建图层
    layer = ds.CreateLayer('footprint', srs, ogr.wkbMultiPolygon)
    if layer is None:
        raise ValueError("Could not create layer.")

    # 创建特征
    feature_defn = layer.GetLayerDefn()
    feature = ogr.Feature(feature_defn)

    # 将 Shapely 对象转换为 OGR 几何
    if isinstance(footprint, Polygon):
        footprint = MultiPolygon([footprint])  # 转换为 MultiPolygon
    geom = ogr.CreateGeometryFromWkb(footprint.wkb)
    feature.SetGeometry(geom)

    # 将特征写入图层
    layer.CreateFeature(feature)

    # 清理
    feature = None
    ds = None
    print(f"Footprint saved as {format}: {output_path}")


# 修改 calculate_large_raster_footprint 函数
def calculate_large_raster_footprint(input_path, block_size=512, overlap=50, save_path=None, save_format='shp'):
    """计算整个大影像的有效足迹，支持不同类型的nodata值，并可选保存为文件"""
    footprints = []
    if save_path is None:
        save_path = os.path.dirname(input_path)


    with rasterio.open(input_path) as src:
        nodata = src.nodata
        height, width = src.height, src.width
        total_blocks = math.ceil(height / block_size) * math.ceil(width / block_size)

        # 获取影像的 CRS
        raster_crs = src.crs
        if raster_crs:
            srs = osr.SpatialReference()
            srs.ImportFromWkt(raster_crs.wkt)
        else:
            srs = None

        with tqdm(total=total_blocks, desc="Calculating footprint") as pbar:
            for i in range(0, height, block_size):
                for j in range(0, width, block_size):
                    # 计算窗口大小并添加重叠
                    window_height = min(block_size + overlap, height - i)
                    window_width = min(block_size + overlap, width - j)
                    window = Window(j, i, window_width, window_height)

                    # 调整窗口以避免超出影像边界
                    if i + window_height > height:
                        window_height = height - i
                    if j + window_width > width:
                        window_width = width - j
                    window = Window(j, i, window_width, window_height)

                    window_transform = src.window_transform(window)
                    block = src.read(1, window=window)

                    footprint = get_valid_footprint(block, nodata, window_transform, window)
                    if footprint:
                        footprints.append(footprint)
                    pbar.update(1)

    if not footprints:
        raise ValueError("No valid data found in the image.")

    # 合并足迹并平滑边界
    final_footprint = unary_union(footprints)
    # 添加微小缓冲区以消除分块缝隙（单位取决于影像坐标系）
    final_footprint = final_footprint.buffer(0.1, join_style=2).buffer(-0.1, join_style=2)

    # 如果提供了保存路径，则保存足迹
    if save_path:
        save_file = os.path.join(save_path, os.path.splitext(os.path.basename(input_path))[0])
        save_footprint_to_file(final_footprint, save_file, format=save_format, crs=srs)

    return final_footprint


if __name__ == "__main__":
    input_raster =  r"D:\GF1_FengCheng_20220726_WGS84.tif"
    output_vector = r".\img"  # 不需要指定扩展名，会自动添加
    footprint = calculate_large_raster_footprint(
        input_raster,
        block_size=2000,
        overlap=50,
        save_path=output_vector,
        save_format='shp'  # 或 'shp'
    )
    plot_footprint(footprint, "Final Footprint")