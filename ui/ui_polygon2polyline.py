#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_polygon2polyline.py
# time: 2025/3/13 22:12
# 栅格影像的有效范围轮廓矢量生成
import os
from PyQt5.QtCore import pyqtSignal, QCoreApplication
from function.tools import Tool
from resources.shpPolygon2Polyline import Ui_Form
from PyQt5.QtWidgets import QFrame
from function.convert_polygon_to_line import polygons_to_lines

from osgeo import ogr

class polygon2polylineWidget(QFrame, Ui_Form):
    error = pyqtSignal()

    def __init__(self, text, parent=None):
        super(polygon2polylineWidget, self).__init__(parent=parent)

        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

        self.tool = Tool()
        self.currentSheet = None
        self.signals()

    def signals(self):
        """按钮触发， 主动调用"""
        self.Polygon2Polyline_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.Polygon2Polyline_filepath_line))
        self.Polygon2Polyline_filepath_line.textChanged.connect(self.suffix_info)

    def suffix_info(self):
        """检测后缀"""
        self.tool.get_suffix(self.Polygon2Polyline_filepath_line)
        if self.tool.suffix not in ['.shp']:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
        if os.path.exists(self.tool.path):
            self.Polygon2Polyline_process_btn.setEnabled(True)
        else:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
            # 按钮不可用
            self.Polygon2Polyline_process_btn.setEnabled(False)
    def process(self):
        """处理"""

        if self.tool.path:
            if self.tool.suffix == ".shp":
                if os.path.exists(self.tool.path):
                    self.progressBar.start()
                    out_file = self.tool.path.replace(".shp", "_lines.shp")
                    polygons_to_lines(self.tool.path, out_file)
                    self.progressBar.stop()


                else:
                    self.Polygon2Polyline_process_btn.setText("请输入正确的shp文件路径，再点击")
                    self.tool.show_error(self, "❗️文件错误", "文件不存在")
            else:
                self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
