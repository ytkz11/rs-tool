#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2025/4/17 22:34
# @File : remove_black_edges_border.py 
'''

'''
import sys


from osgeo import gdal
import numpy as np
import os

def remove_black_edges_border_only(input_path, output_path, block_size=2000, edge_width=100, min_neg_bands=2, progress_callback=None):
    """
    处理遥感影像边缘区域，将所有波段中对应位置满足条件的负值像素统一置为0。
    如果边缘区域某位置至少有指定数量波段（默认3个）为负值，则所有波段的该位置置为0。

    参数:
        input_path (str): 输入影像文件路径
        output_path (str): 输出影像文件路径
        block_size (int): 分块处理的大小（默认2000像素）
        edge_width (int): 处理的边界宽度（单位：像素，默认100）
        min_neg_bands (int): 最小负值波段数，触发置零的条件（默认3）
        progress_callback (callable, optional): 进度更新回调函数，接收百分比（0-100）

    返回:
        bool: 处理成功返回 True，否则抛出异常
    """
    # 打开输入影像（只读模式）
    ds = gdal.Open(input_path, gdal.GA_ReadOnly)
    if ds is None:
        raise FileNotFoundError(f"无法打开输入文件：{input_path}")

    cols = ds.RasterXSize
    rows = ds.RasterYSize
    bands = ds.RasterCount
    geotransform = ds.GetGeoTransform()
    projection = ds.GetProjection()
    dtype = ds.GetRasterBand(1).DataType

    # 检查波段数是否足够
    if bands < min_neg_bands:
        raise ValueError(f"波段数 ({bands}) 小于最小负值波段数 ({min_neg_bands})，无法满足条件")

    # 创建输出影像
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(output_path, cols, rows, bands, dtype)
    if out_ds is None:
        raise RuntimeError(f"无法创建输出文件：{output_path}")
    out_ds.SetGeoTransform(geotransform)
    out_ds.SetProjection(projection)

    # 计算总块数，用于进度更新
    total_blocks = ((rows + block_size - 1) // block_size) * ((cols + block_size - 1) // block_size)
    current_block = 0

    # 分块处理
    for y in range(0, rows, block_size):
        block_height = min(block_size, rows - y)
        for x in range(0, cols, block_size):
            block_width = min(block_size, cols - x)

            # 读取所有波段的当前块数据
            block_data = np.zeros((bands, block_height, block_width), dtype=np.float32)
            for band_idx in range(bands):
                in_band = ds.GetRasterBand(band_idx + 1)
                block_data[band_idx] = in_band.ReadAsArray(x, y, block_width, block_height).astype(np.float32)

            # 判断当前块是否在边缘区域
            is_border = (
                x < edge_width or  # 左边缘
                y < edge_width or  # 上边缘
                (x + block_width) > (cols - edge_width) or  # 右边缘
                (y + block_height) > (rows - edge_width)    # 下边缘
            )

            # 如果在边缘区域，处理负值
            if is_border:
                # 计算每个位置负值的波段数
                neg_count = np.sum(block_data < 0, axis=0)  # 沿波段轴统计负值数量
                # 创建掩膜：负值波段数 >= min_neg_bands
                neg_mask = neg_count >= min_neg_bands
                # 对所有波段应用掩膜
                block_data[:, neg_mask] = 0

            # 将处理后的数据写回每个波段
            for band_idx in range(bands):
                out_band = out_ds.GetRasterBand(band_idx + 1)
                out_band.WriteArray(block_data[band_idx], xoff=x, yoff=y)

            # 更新进度
            current_block += 1
            if progress_callback:
                progress_percent = int((current_block / total_blocks) * 100)
                try:
                    progress_callback(progress_percent)
                except Exception as e:
                    print(f"进度回调函数调用失败: {e}")

            print(f"处理块: x={x}, y={y}, 宽度={block_width}, 高度={block_height}, 是否边缘={is_border}")

    # 确保所有数据写入磁盘
    out_ds.FlushCache()

    # 关闭数据集并清理
    ds = None
    out_ds = None
    print(f"分块处理完成，输出文件保存在：{output_path}")
    return True


if __name__ == '__main__':
    A = Solution()
    a = A.function()
    print()
