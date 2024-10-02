# -*- coding: utf-8 -*-

from enum import Enum


class Content(Enum):
    ColorEnhancement_TITLE = "📣 植被色彩增强使用须知"
    ColorEnhancement_CONTENT = """
                        📢 批量处理输入文件夹下的影像
                        📢 输入影像为4波段，分别是蓝、绿、红、近红外波段
                        📢 阈值范围在0-1之间，一般使用0.3
                        📢 输入结果保存在  输入文件夹下
                        """
    SHP2DXF_TITLE = "📣 SHP TO DXF 使用须知"
    SHP2DXF_CONTENT = """📢 字段只支持英文、数字⌛，
                        📢 输出文件保存在输入文件相同的文件夹下
                        📢 选择分类的字段
                        """

    SHP2DXF_ORIGIN_TITLE = "📣 SHP TO DXF 使用须知"
    SHP2DXF_ORIGIN_CONTENT = """📢 输出文件保存在输入文件相同的文件夹下
                        📢 保存所有的字段
                        """
    SHP2KML_TITLE = "📣 SHP TO KML使用须知"
    SHP2KML_CONTENT = """📢 输出文件保存在输入文件相同的文件夹下
                        📢 将所有属性都保留到KML中
                        """

    RESTORESHP_TITLE = "📣SHP修复使用须知"
    RESTORESHP_CONTENT = """
                        📢 输出文件保存在输入文件相同的文件夹的out文件夹下
                        """
    PHOTOGPS_TITLE = "📣读取照片的地理信息，并保存为shp"
    PHOTOGPS_CONTENT = """
                        📢 照片必须为原图
                        📢 输出文件保存在输入文件夹下
                        📢 输出文件为shp格式
                        """