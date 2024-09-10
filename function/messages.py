# -*- coding: utf-8 -*-

from enum import Enum


class Content(Enum):

    SHP2DXF_TITLE = "📣 SHP TO DXF 使用须知"
    SHP2DXF_CONTENT = """📢 字段只支持英文、数字⌛，
                        📢 输出文件保存在输入文件相同的文件夹下
                        📢 选择分类的字段
                        """

    SHP2DXF_ORIGIN_TITLE = "📣 SHP TO DXF 使用须知"
    SHP2DXF_ORIGIN_CONTENT = """
                        📢 输出文件保存在输入文件相同的文件夹下
                        📢 保存所有的字段
                        """
    SHP2KML_TITLE = "📣 SHP TO KML使用须知"
    SHP2KML_CONTENT = """
                        📢 输出文件保存在输入文件相同的文件夹下
                        📢 将所有属性都保留到KML中
                        """