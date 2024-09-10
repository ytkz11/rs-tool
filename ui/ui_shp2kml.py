#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_shp2dxf.py
# time: 2024/9/7 16:12
# 不按属性分层，输出全部图形
import os
from PyQt5.QtCore import pyqtSignal, QCoreApplication
from function.tools import Tool
from resources.shpkml import Ui_Form
from PyQt5.QtWidgets import QFrame
from function.shp2kml_with_label import convert_to_kml



class shp2kmlWidget_origin(QFrame, Ui_Form):
    error = pyqtSignal()

    def __init__(self, text, parent=None):
        super(shp2kmlWidget_origin, self).__init__(parent=parent)

        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

        self.tool = Tool()
        self.currentSheet = None
        self.signals()

    def signals(self):
        """按钮触发， 主动调用"""
        self.shp2kml_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.shp2dxf_filepath_line))
        self.shp2kml_filepath_line.textChanged.connect(self.suffix_info)

    def suffix_info(self):
        """检测后缀"""
        self.tool.get_suffix(self.shp2kml_filepath_line)
        if self.tool.suffix not in ['.shp']:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
        if os.path.exists(self.tool.path):
            self.shp2kml_process_btn.setEnabled(True)
        else:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
            # 按钮不可用
            self.shp2kml_process_btn.setEnabled(False)
    def process(self):
        """处理"""

        if self.tool.path:
            if self.tool.suffix == ".shp":
                if os.path.exists(self.tool.path):
                    self.progressBar.start()
                    convert_to_kml(self.tool.path)
                    self.progressBar.stop()
                else:
                    self.shp2kml_process_btn.setText("请输入正确的shp文件路径，再点击")
                    self.tool.show_error(self, "❗️文件错误", "文件不存在")
            else:
                self.tool.show_error(self, "❗️文件错误", "文件后缀错误")

    #