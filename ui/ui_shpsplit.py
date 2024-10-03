#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_shpsplit.py
# time: 2024/10/3 16:12
# 按属性分割shp
import os
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal
from function.tools import Tool
from function.shp2dxf_ezdxf_padding import Shp2DxfPadding
from resources.shpsplit import Ui_Form

class shpsplitWidget(QFrame, Ui_Form):
    error = pyqtSignal()

    def __init__(self, text, parent=None):
        super(shpsplitWidget, self).__init__(parent=parent)

        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

        self.tool = Tool()
        self.currentSheet = None
        self.signals()
        self.process_btn.setEnabled(False)

    def signals(self):
        """按钮触发， 主动调用"""
        self.shpsplit_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.shpsplit_filepath_line))
        self.shpsplit_filepath_line.textChanged.connect(self.suffix_info)

    def suffix_info(self):
        """检测后缀"""
        self.tool.get_suffix(self.shpsplit_filepath_line)
        if self.tool.suffix not in ['.shp']:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
        if os.path.exists(self.tool.path):
            self.read_file()
        else:
            self.shpsplit_header_box.setText("输入的文件不存在，请输入正确的shp文件路径")


    def read_file(self):
        """读取shp，写入combox列"""

        if self.tool.path:
            self.header_box_clear()
            if self.tool.suffix == ".shp":

                field_list = Shp2DxfPadding(self.tool.path).field
                self.shpsplit_header_box.addItems(field_list)
                self.process_btn.setEnabled(True)
        else:
            self.header_box_clear()
    def header_box_clear(self):
        """检查并清除header_combox"""
        if self.shpsplit_header_box.count() > 0:
            self.shpsplit_header_box.clear()
            self.shpsplit_header_box.setText("在上方输入正确shp文件，自动获取shp的字段")
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
            # 按钮不可用
            self.process_btn.setEnabled(False)
    def process(self):
        """处理"""

        if self.tool.path:
            # self.header_box_clear()
            if self.tool.suffix == ".shp":
                if os.path.exists(self.tool.path):
                    self.progressBar.start()
                    Shp2DxfPadding(self.tool.path).shp2dxf(self.shp2dxf_header_box.text())
                    self.progressBar.stop()
                else:
                    self.shpsplit_header_box.setText("输入的文件不存在，请输入正确的shp文件路径")
                    self.tool.show_error(self, "❗️文件错误", "文件不存在")




