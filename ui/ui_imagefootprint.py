#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_imagefootprint.py
# time: 2025/3/13 22:12
# 栅格影像的有效范围轮廓矢量生成
import os
from PyQt5.QtCore import pyqtSignal, QCoreApplication
from function.tools import Tool
from resources.imagefootprint import Ui_Form
from PyQt5.QtWidgets import QFrame
from function.big_image_footprint import calculate_large_raster_footprint

from osgeo import ogr

class imagefootprintWidget(QFrame, Ui_Form):
    error = pyqtSignal()

    def __init__(self, text, parent=None):
        super(imagefootprintWidget, self).__init__(parent=parent)

        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

        self.tool = Tool()
        self.currentSheet = None
        self.signals()

    def signals(self):
        """按钮触发， 主动调用"""
        self.imagefootprint_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.imagefootprint_filepath_line))
        self.imagefootprint_filepath_line.textChanged.connect(self.suffix_info)

    def suffix_info(self):
        """检测后缀"""
        self.tool.get_suffix(self.imagefootprint_filepath_line)
        if self.tool.suffix not in ['.tiff', '.tif','.TIF','.TIFF']:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
        if os.path.exists(self.tool.path):
            self.imagefootprint_process_btn.setEnabled(True)
        else:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
            # 按钮不可用
            self.imagefootprint_process_btn.setEnabled(False)
    def process(self):
        """处理"""


        if self.tool.path:
            if self.tool.suffix == ".tiff" or self.tool.suffix == ".tif" or self.tool.suffix == ".TIF" or self.tool.suffix == ".TIFF":
                if os.path.exists(self.tool.path):
                    self.imagefootprint_process_btn.setEnabled(False)
                    self.imagefootprint_process_btn.setText('正在提取影像轮廓')
                    self.progressBar.start()
                    out_PATH = os.path.dirname(self.tool.path)
                    calculate_large_raster_footprint(
                        self.tool.path,
                        block_size=2000,
                        overlap=50,
                        save_path=out_PATH,
                        save_format='shp'  # 或 'shp'
                    )
                    self.progressBar.stop()
                    self.imagefootprint_process_btn.setEnabled(True)
                    self.imagefootprint_process_btn.setText('完成轮廓提取')



                else:
                    self.imagefootprint_process_btn.setText("请输入正确的栅格文件路径，再点击")
                    self.tool.show_error(self, "❗️文件错误", "文件不存在")
            else:
                self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
