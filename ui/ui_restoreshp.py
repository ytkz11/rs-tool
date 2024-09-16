#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ui_restoreshp.py
# time: 2024/9/16 23:12
# shp修复
import os
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal
from function.tools import Tool
from function.RestoreShp import RestoreShp
from resources.restoreshp import Ui_Form

class restore_shpWidget(QFrame, Ui_Form):
    error = pyqtSignal()

    def __init__(self, text, parent=None):
        super(restore_shpWidget, self).__init__(parent=parent)

        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

        self.tool = Tool()
        self.currentSheet = None
        self.signals()
        self.restoreshp_process_btn.setEnabled(False)
    def signals(self):
        """按钮触发， 主动调用"""
        self.restoreshp_filepath_btn.clicked.connect(lambda: self.tool.handle_path(self.restoreshp_filepath_line))
        self.restoreshp_filepath_line.textChanged.connect(self.suffix_info)

    def suffix_info(self):
        """检测后缀"""
        self.tool.get_suffix(self.restoreshp_filepath_line)
        if self.tool.suffix not in ['.shp']:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
        if os.path.exists(self.tool.path):
            self.restoreshp_process_btn.setEnabled(True)
        else:
            self.tool.show_error(self, "❗️文件错误", "文件后缀错误")
            # 按钮不可用
            self.restoreshp_process_btn.setEnabled(False)
    def process(self):
        """处理"""

        if self.tool.path:
            if self.tool.suffix == ".shp":
                if os.path.exists(self.tool.path):

                    temp_output = os.path.join(os.path.dirname(self.tool.path), "out")
                    RestoreShp(self.tool.path, temp_output).restore_shp()

                else:
                    self.restoreshp_process_btn.setText("请输入正确的shp文件路径，再点击")
                    self.tool.show_error(self, "❗️文件错误", "文件不存在")
            else:
                self.tool.show_error(self, "❗️文件错误", "文件后缀错误")


